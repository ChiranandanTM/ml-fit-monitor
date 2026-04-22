"""
Module 8: Experiment History and Persistence Engine

Stores and tracks ML experiment results across sessions.
Enables experiment comparison and historical trend analysis.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import os

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "experiments.db"


def init_experiment_db():
    """Initialize SQLite database for experiment tracking."""
    
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create experiments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiments (
            id TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            dataset_hash TEXT NOT NULL,
            dataset_name TEXT,
            dataset_shape TEXT NOT NULL,
            problem_type TEXT NOT NULL,
            overall_fit_status TEXT NOT NULL,
            best_model_name TEXT,
            best_model_train_score REAL,
            best_model_val_score REAL,
            best_model_gap REAL,
            best_model_generalization_score REAL,
            notes TEXT,
            tags TEXT
        )
    ''')
    
    # Create model_results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_results (
            id TEXT PRIMARY KEY,
            experiment_id TEXT NOT NULL,
            model_name TEXT NOT NULL,
            fit_status TEXT NOT NULL,
            train_score REAL,
            val_score REAL,
            gap REAL,
            cv_mean REAL,
            cv_std REAL,
            bias REAL,
            variance REAL,
            FOREIGN KEY (experiment_id) REFERENCES experiments(id)
        )
    ''')
    
    # Create hyperparameter_tuning table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hyperparameter_tuning (
            id TEXT PRIMARY KEY,
            experiment_id TEXT NOT NULL,
            model_name TEXT NOT NULL,
            fit_status TEXT NOT NULL,
            tuned BOOLEAN,
            baseline_train_score REAL,
            baseline_val_score REAL,
            baseline_gap REAL,
            tuned_train_score REAL,
            tuned_val_score REAL,
            tuned_gap REAL,
            train_improvement REAL,
            val_improvement REAL,
            gap_improvement REAL,
            best_params TEXT,
            FOREIGN KEY (experiment_id) REFERENCES experiments(id)
        )
    ''')
    
    # Create experiment_comparisons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiment_comparisons (
            id TEXT PRIMARY KEY,
            experiment_id_1 TEXT NOT NULL,
            experiment_id_2 TEXT NOT NULL,
            comparison_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            improvement_summary TEXT,
            FOREIGN KEY (experiment_id_1) REFERENCES experiments(id),
            FOREIGN KEY (experiment_id_2) REFERENCES experiments(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✓ Experiment database initialized at {DB_PATH}")


def compute_dataset_hash(df) -> str:
    """Compute hash of dataset for duplicate detection."""
    df_json = df.head(10).to_json()  # Use first 10 rows for quick hash
    return hashlib.md5(df_json.encode()).hexdigest()


def save_experiment(df, results: Dict, notes: str = "", tags: List[str] = None) -> str:
    """
    Save experiment results to database.
    
    Parameters:
    -----------
    df : DataFrame
        Original dataset
    results : dict
        Results from ml_pipeline.run_pipeline
    notes : str
        Optional notes about the experiment
    tags : list
        Optional tags for categorizing experiments
        
    Returns:
    --------
    str : Experiment ID
    """
    
    init_experiment_db()
    
    experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Save experiment metadata
        dataset_hash = compute_dataset_hash(df)
        summary = results.get("summary", {})
        
        cursor.execute('''
            INSERT INTO experiments (
                id, dataset_hash, dataset_name, dataset_shape, problem_type,
                overall_fit_status, best_model_name, best_model_train_score,
                best_model_val_score, best_model_gap, notes, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            experiment_id,
            dataset_hash,
            getattr(df, 'name', 'unknown'),
            json.dumps(list(df.shape)),
            summary.get("problem_type", "unknown"),
            summary.get("overall_fit_status", "unknown"),
            summary.get("best_model", ""),
            summary.get("best_model_train_score", 0),
            summary.get("best_model_val_score", 0),
            summary.get("best_model_gap", 0),
            notes,
            json.dumps(tags or [])
        ))
        
        # Save model results
        for model in results.get("models", []):
            model_id = f"{experiment_id}_{model.get('model', 'unknown').replace(' ', '_')}"
            
            cursor.execute('''
                INSERT INTO model_results (
                    id, experiment_id, model_name, fit_status, train_score,
                    val_score, gap, cv_mean, cv_std, bias, variance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                model_id,
                experiment_id,
                model.get("model", ""),
                model.get("fit_status", ""),
                model.get("train_score", 0),
                model.get("val_score", 0),
                model.get("gap", 0),
                model.get("cv_confidence_interval", {}).get("mean", 0),
                model.get("cv_confidence_interval", {}).get("std", 0),
                model.get("bias_variance", {}).get("bias", 0),
                model.get("bias_variance", {}).get("variance", 0)
            ))
        
        conn.commit()
        print(f"✓ Experiment {experiment_id} saved to database")
        return experiment_id
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Failed to save experiment: {str(e)}")
        raise
    finally:
        conn.close()


def get_experiment(experiment_id: str) -> Optional[Dict]:
    """Retrieve experiment results from database."""
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Get experiment metadata
        cursor.execute('SELECT * FROM experiments WHERE id = ?', (experiment_id,))
        exp_row = cursor.fetchone()
        
        if not exp_row:
            return None
        
        # Get model results
        cursor.execute('SELECT * FROM model_results WHERE experiment_id = ?', (experiment_id,))
        model_rows = cursor.fetchall()
        
        # Get hyperparameter tuning results
        cursor.execute('SELECT * FROM hyperparameter_tuning WHERE experiment_id = ?', (experiment_id,))
        tuning_rows = cursor.fetchall()
        
        experiment = {
            "id": exp_row[0],
            "timestamp": exp_row[1],
            "dataset_hash": exp_row[2],
            "dataset_shape": json.loads(exp_row[4]),
            "problem_type": exp_row[5],
            "overall_fit_status": exp_row[6],
            "best_model": exp_row[7],
            "notes": exp_row[11],
            "tags": json.loads(exp_row[12]),
            "models": [
                {
                    "model_name": row[2],
                    "fit_status": row[3],
                    "train_score": row[4],
                    "val_score": row[5],
                    "gap": row[6]
                } for row in model_rows
            ],
            "tuning_results": [
                {
                    "model_name": row[2],
                    "tuned": row[3],
                    "baseline_val_score": row[5],
                    "tuned_val_score": row[8],
                    "val_improvement": row[10]
                } for row in tuning_rows if row[3]  # Only tuned models
            ]
        }
        
        return experiment
        
    finally:
        conn.close()


def list_experiments(limit: int = 10, tags: List[str] = None) -> List[Dict]:
    """List recent experiments, optionally filtered by tags."""
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        if tags:
            # Filter by tags (simplified - check if tags JSON contains search strings)
            query = '''
                SELECT id, timestamp, overall_fit_status, best_model, tags
                FROM experiments
                ORDER BY timestamp DESC
                LIMIT ?
            '''
            cursor.execute(query, (limit,))
        else:
            query = '''
                SELECT id, timestamp, overall_fit_status, best_model, tags
                FROM experiments
                ORDER BY timestamp DESC
                LIMIT ?
            '''
            cursor.execute(query, (limit,))
        
        rows = cursor.fetchall()
        
        experiments = []
        for row in rows:
            exp_tags = json.loads(row[4])
            if tags and not any(t in exp_tags for t in tags):
                continue
                
            experiments.append({
                "id": row[0],
                "timestamp": row[1],
                "fit_status": row[2],
                "best_model": row[3],
                "tags": exp_tags
            })
        
        return experiments
        
    finally:
        conn.close()


def compare_experiments(exp_id_1: str, exp_id_2: str) -> Optional[Dict]:
    """
    Compare two experiments and generate improvement summary.
    
    Returns comparison metrics and recommendations.
    """
    
    exp1 = get_experiment(exp_id_1)
    exp2 = get_experiment(exp_id_2)
    
    if not exp1 or not exp2:
        return None
    
    comparison = {
        "exp1_id": exp_id_1,
        "exp2_id": exp_id_2,
        "exp1_timestamp": exp1["timestamp"],
        "exp2_timestamp": exp2["timestamp"],
        "exp1_status": exp1["overall_fit_status"],
        "exp2_status": exp2["overall_fit_status"],
        "status_improved": False,
        "best_model_1": exp1["best_model"],
        "best_model_2": exp2["best_model"],
        "model_changes": [],
        "overall_improvement_summary": ""
    }
    
    # Check if fit status improved
    status_progression = {
        "Underfitting": 0,
        "Overfitting": 1,
        "Good Fit": 2
    }
    
    status1_rank = status_progression.get(exp1["overall_fit_status"], -1)
    status2_rank = status_progression.get(exp2["overall_fit_status"], -1)
    
    comparison["status_improved"] = status2_rank > status1_rank
    
    # Compare model performance
    models1_dict = {m["model_name"]: m for m in exp1["models"]}
    models2_dict = {m["model_name"]: m for m in exp2["models"]}
    
    for model_name in models1_dict:
        if model_name in models2_dict:
            m1 = models1_dict[model_name]
            m2 = models2_dict[model_name]
            
            val_improvement = m2["val_score"] - m1["val_score"]
            gap_improvement = m1["gap"] - m2["gap"]
            
            comparison["model_changes"].append({
                "model": model_name,
                "exp1_val_score": m1["val_score"],
                "exp2_val_score": m2["val_score"],
                "val_improvement": val_improvement,
                "exp1_gap": m1["gap"],
                "exp2_gap": m2["gap"],
                "gap_improvement": gap_improvement
            })
    
    # Generate summary
    if comparison["status_improved"]:
        comparison["overall_improvement_summary"] = f"Status improved from {exp1['overall_fit_status']} to {exp2['overall_fit_status']}"
    else:
        comparison["overall_improvement_summary"] = f"Status unchanged or declined: {exp1['overall_fit_status']} → {exp2['overall_fit_status']}"
    
    return comparison


def save_experiment_comparison(exp_id_1: str, exp_id_2: str, comparison: Dict) -> str:
    """Save experiment comparison results to database."""
    
    init_experiment_db()
    
    comparison_id = f"cmp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO experiment_comparisons (
                id, experiment_id_1, experiment_id_2, improvement_summary
            ) VALUES (?, ?, ?, ?)
        ''', (
            comparison_id,
            exp_id_1,
            exp_id_2,
            json.dumps(comparison["overall_improvement_summary"])
        ))
        
        conn.commit()
        return comparison_id
        
    finally:
        conn.close()


def get_experiment_trends(window_size: int = 10) -> Dict:
    """Analyze trends in recent experiments."""
    
    recent_exps = list_experiments(limit=window_size)
    
    if not recent_exps:
        return {"message": "No experiments to analyze"}
    
    fit_status_counts = {}
    for exp in recent_exps:
        status = exp["fit_status"]
        fit_status_counts[status] = fit_status_counts.get(status, 0) + 1
    
    # Determine trend
    trend = "stable"
    if len(recent_exps) > 1:
        recent_status = recent_exps[0]["fit_status"]
        old_status = recent_exps[-1]["fit_status"]
        
        status_progression = {
            "Underfitting": 0,
            "Overfitting": 1,
            "Good Fit": 2
        }
        
        recent_rank = status_progression.get(recent_status, -1)
        old_rank = status_progression.get(old_status, -1)
        
        if recent_rank > old_rank:
            trend = "improving"
        elif recent_rank < old_rank:
            trend = "degrading"
    
    return {
        "total_experiments": len(recent_exps),
        "status_distribution": fit_status_counts,
        "trend": trend,
        "most_common_status": max(fit_status_counts, key=fit_status_counts.get),
        "recent_experiments": recent_exps
    }
