"""
Module: Real-Time Monitoring Dashboard

Track model performance over time
- Baseline model comparison
- Performance degradation detection
- Retraining recommendations
- Performance history tracking
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import sqlite3
import json


class ModelMonitor:
    """Monitor model performance and detect degradation."""
    
    def __init__(self, db_path: str = 'monitoring.db'):
        """
        Initialize model monitor.
        
        Parameters:
        -----------
        db_path : str
            Path to SQLite monitoring database
        """
        self.db_path = db_path
        self._init_monitoring_db()
    
    def _init_monitoring_db(self):
        """Initialize or connect to monitoring database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS baseline_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                baseline_score REAL NOT NULL,
                baseline_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                features_used TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                score REAL NOT NULL,
                samples_evaluated INTEGER,
                evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS degradation_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                alert_type TEXT,
                severity TEXT,
                degradation_pct REAL,
                alert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action_taken TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Monitoring database initialized: {self.db_path}")
    
    def set_baseline(
        self,
        model_name: str,
        baseline_score: float,
        features_used: List[str] = None,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """
        Set baseline for monitoring.
        
        Parameters:
        -----------
        model_name : str
            Model name
        baseline_score : float
            Baseline performance score
        features_used : list, optional
            Features used by model
        metadata : dict, optional
            Additional metadata
        
        Returns:
        --------
        dict : Baseline info
        """
        
        print(f"\n📍 Setting Baseline for {model_name}:")
        print(f"   Baseline Score: {baseline_score:.4f}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        features_json = json.dumps(features_used) if features_used else None
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute('''
            INSERT INTO baseline_models (model_name, baseline_score, features_used, metadata)
            VALUES (?, ?, ?, ?)
        ''', (model_name, baseline_score, features_json, metadata_json))
        
        baseline_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"   ✅ Baseline set (ID: {baseline_id})")
        
        return {
            'baseline_id': baseline_id,
            'model_name': model_name,
            'baseline_score': baseline_score,
            'set_date': datetime.now().isoformat()
        }
    
    def record_evaluation(
        self,
        model_name: str,
        score: float,
        samples_evaluated: int,
        status: str = 'OK',
        notes: str = None
    ) -> Dict[str, Any]:
        """
        Record model evaluation result.
        
        Parameters:
        -----------
        model_name : str
            Model name
        score : float
            Performance score
        samples_evaluated : int
            Number of samples evaluated
        status : str
            Status ('OK', 'WARNING', 'ALERT')
        notes : str, optional
            Notes about evaluation
        
        Returns:
        --------
        dict : Evaluation record
        """
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_history (model_name, score, samples_evaluated, status, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (model_name, score, samples_evaluated, status, notes))
        
        eval_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"📊 Recorded evaluation for {model_name}: {score:.4f} (Samples: {samples_evaluated})")
        
        return {
            'evaluation_id': eval_id,
            'model_name': model_name,
            'score': score,
            'samples_evaluated': samples_evaluated,
            'timestamp': datetime.now().isoformat()
        }
    
    def detect_degradation(
        self,
        model_name: str,
        current_score: float,
        degradation_threshold_pct: float = 5.0
    ) -> Dict[str, Any]:
        """
        Detect if model performance has degraded.
        
        Parameters:
        -----------
        model_name : str
            Model name
        current_score : float
            Current performance score
        degradation_threshold_pct : float
            Degradation percentage threshold
        
        Returns:
        --------
        dict : Degradation analysis
        """
        
        print(f"\n🔍 Degradation Detection for {model_name}:")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get baseline
        cursor.execute('''
            SELECT baseline_score FROM baseline_models
            WHERE model_name = ?
            ORDER BY baseline_date DESC
            LIMIT 1
        ''', (model_name,))
        
        baseline_row = cursor.fetchone()
        if not baseline_row:
            print(f"   ⚠️  No baseline found")
            conn.close()
            return {'error': 'No baseline set', 'model_name': model_name}
        
        baseline_score = baseline_row[0]
        degradation = ((baseline_score - current_score) / baseline_score) * 100
        
        print(f"   Baseline: {baseline_score:.4f}")
        print(f"   Current: {current_score:.4f}")
        print(f"   Degradation: {degradation:.2f}%")
        
        # Check if degradation exceeds threshold
        is_degraded = degradation > degradation_threshold_pct
        severity = 'CRITICAL' if degradation > 15 else 'HIGH' if degradation > 10 else 'MEDIUM'
        
        alert_data = {
            'model_name': model_name,
            'is_degraded': is_degraded,
            'degradation_pct': float(degradation),
            'baseline_score': float(baseline_score),
            'current_score': float(current_score),
            'severity': severity if is_degraded else 'OK',
            'exceeds_threshold': is_degraded
        }
        
        if is_degraded:
            print(f"   ⚠️  ALERT: {severity} degradation detected!")
            
            # Record alert
            cursor.execute('''
                INSERT INTO degradation_alerts (model_name, alert_type, severity, degradation_pct)
                VALUES (?, ?, ?, ?)
            ''', (model_name, 'DEGRADATION', severity, degradation))
            
            alert_data['recommendation'] = self._get_degradation_recommendation(degradation)
        else:
            print(f"   ✅ Performance acceptable")
            alert_data['recommendation'] = "Continue monitoring"
        
        conn.commit()
        conn.close()
        
        return alert_data
    
    def _get_degradation_recommendation(self, degradation_pct: float) -> str:
        """Get recommendation based on degradation severity."""
        if degradation_pct > 20:
            return "🔴 URGENT: Retrain model immediately. Data drift or concept drift likely."
        elif degradation_pct > 10:
            return "🟠 IMPORTANT: Plan model retraining soon. Consider investigating root cause."
        elif degradation_pct > 5:
            return "🟡 MODERATE: Monitor closely. May need retraining within 1-2 weeks."
        else:
            return "🟢 MINOR: Continue monitoring. No immediate action needed."
    
    def get_performance_history(
        self,
        model_name: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get performance history for a model.
        
        Parameters:
        -----------
        model_name : str
            Model name
        days : int
            Number of days to look back
        
        Returns:
        --------
        dict : Performance history
        """
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT score, samples_evaluated, evaluation_date, status, notes
            FROM performance_history
            WHERE model_name = ? AND evaluation_date > ?
            ORDER BY evaluation_date ASC
        ''', (model_name, cutoff_date.isoformat()))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        scores = []
        
        for row in rows:
            history.append({
                'score': float(row[0]),
                'samples': int(row[1]),
                'timestamp': row[2],
                'status': row[3],
                'notes': row[4]
            })
            scores.append(float(row[0]))
        
        # Calculate statistics
        if scores:
            avg_score = np.mean(scores)
            std_score = np.std(scores)
            min_score = np.min(scores)
            max_score = np.max(scores)
            trend = 'improving' if scores[-1] > scores[0] else 'degrading'
        else:
            avg_score = std_score = min_score = max_score = 0
            trend = 'unknown'
        
        print(f"\n📈 Performance History for {model_name} (last {days} days):")
        print(f"   Records: {len(history)}")
        print(f"   Avg Score: {avg_score:.4f}")
        print(f"   Trend: {trend}")
        
        return {
            'model_name': model_name,
            'records': history,
            'statistics': {
                'count': len(history),
                'average': float(avg_score),
                'std_dev': float(std_score),
                'min': float(min_score),
                'max': float(max_score),
                'trend': trend
            },
            'plot_data': [
                {'date': h['timestamp'], 'score': h['score']}
                for h in history
            ]
        }
    
    def get_retraining_recommendation(
        self,
        model_name: str,
        degradation_threshold_pct: float = 5.0
    ) -> Dict[str, Any]:
        """
        Get retraining recommendation.
        
        Parameters:
        -----------
        model_name : str
            Model name
        degradation_threshold_pct : float
            Degradation threshold
        
        Returns:
        --------
        dict : Retraining recommendation
        """
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest score and baseline
        cursor.execute('''
            SELECT score FROM performance_history
            WHERE model_name = ?
            ORDER BY evaluation_date DESC
            LIMIT 1
        ''', (model_name,))
        
        latest = cursor.fetchone()
        
        cursor.execute('''
            SELECT baseline_score FROM baseline_models
            WHERE model_name = ?
            ORDER BY baseline_date DESC
            LIMIT 1
        ''', (model_name,))
        
        baseline = cursor.fetchone()
        conn.close()
        
        if not latest or not baseline:
            return {'error': 'Insufficient data', 'recommendation': 'Set baseline and record evaluations first'}
        
        current_score = latest[0]
        baseline_score = baseline[0]
        degradation = ((baseline_score - current_score) / baseline_score) * 100
        
        # Recommend retraining if degradation exceeds threshold
        needs_retrain = degradation > degradation_threshold_pct
        
        recommendation = {
            'model_name': model_name,
            'needs_retraining': needs_retrain,
            'degradation_severity': degradation,
            'priority': (
                'CRITICAL' if degradation > 20 else
                'HIGH' if degradation > 10 else
                'MEDIUM' if degradation > 5 else
                'LOW'
            ),
            'suggested_action': self._get_degradation_recommendation(degradation),
            'retrain_frequency': self._calculate_retrain_frequency(degradation),
            'estimated_data_needed': self._estimate_data_for_retraining(degradation)
        }
        
        print(f"\n🔧 Retraining Recommendation for {model_name}:")
        print(f"   Needs Retraining: {'Yes' if needs_retrain else 'No'}")
        print(f"   Priority: {recommendation['priority']}")
        print(f"   Suggested Action: {recommendation['suggested_action']}")
        
        return recommendation
    
    def _calculate_retrain_frequency(self, degradation_pct: float) -> str:
        """Calculate recommended retraining frequency."""
        if degradation_pct > 15:
            return "Immediately"
        elif degradation_pct > 10:
            return "Within 3-7 days"
        elif degradation_pct > 5:
            return "Within 1-2 weeks"
        else:
            return "Monthly review recommended"
    
    def _estimate_data_for_retraining(self, degradation_pct: float) -> Dict[str, Any]:
        """Estimate data needed for retraining."""
        if degradation_pct > 15:
            return {
                'recommendation': 'Significant retraining required',
                'suggested_samples': '50-100% of original dataset',
                'tuning_scope': 'Full model retuning'
            }
        elif degradation_pct > 10:
            return {
                'recommendation': 'Major retraining with new data',
                'suggested_samples': '30-50% of original dataset',
                'tuning_scope': 'Some hyperparameter adjustment'
            }
        else:
            return {
                'recommendation': 'Incremental learning from new data',
                'suggested_samples': '10-20% of original dataset',
                'tuning_scope': 'Minimal changes needed'
            }
    
    def get_monitoring_dashboard(self, model_names: List[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive monitoring dashboard.
        
        Parameters:
        -----------
        model_names : list, optional
            List of models to monitor (all if None)
        
        Returns:
        --------
        dict : Dashboard data
        """
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all models if not specified
        if not model_names:
            cursor.execute('SELECT DISTINCT model_name FROM baseline_models')
            model_names = [row[0] for row in cursor.fetchall()]
        
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'models': {},
            'alerts': [],
            'summary': {}
        }
        
        total_models = len(model_names)
        degraded_models = 0
        
        for model in model_names:
            # Get latest metrics
            cursor.execute('''
                SELECT baseline_score FROM baseline_models
                WHERE model_name = ?
                ORDER BY baseline_date DESC
                LIMIT 1
            ''', (model,))
            baseline_row = cursor.fetchone()
            
            cursor.execute('''
                SELECT score FROM performance_history
                WHERE model_name = ?
                ORDER BY evaluation_date DESC
                LIMIT 1
            ''', (model,))
            latest_row = cursor.fetchone()
            
            if baseline_row and latest_row:
                baseline = baseline_row[0]
                latest = latest_row[0]
                degradation = ((baseline - latest) / baseline) * 100
                
                if degradation > 5:
                    degraded_models += 1
                
                dashboard['models'][model] = {
                    'baseline': float(baseline),
                    'current': float(latest),
                    'degradation_pct': float(degradation),
                    'status': 'ALERT' if degradation > 10 else 'WARNING' if degradation > 5 else 'OK'
                }
        
        dashboard['summary'] = {
            'total_models': total_models,
            'models_ok': total_models - degraded_models,
            'models_degraded': degraded_models,
            'health_percentage': ((total_models - degraded_models) / total_models * 100) if total_models > 0 else 0
        }
        
        conn.close()
        
        return dashboard
