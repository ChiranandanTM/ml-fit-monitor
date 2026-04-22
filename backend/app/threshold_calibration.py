"""
Module 9: Automated Threshold Calibration Engine

Dynamically calibrates fit detection thresholds based on validation behavior.
Learns optimal thresholds from historical experiment data.
"""

import numpy as np
import sqlite3
from pathlib import Path
from typing import Dict, Tuple
import json

DB_PATH = Path(__file__).parent.parent.parent / "experiments.db"


class ThresholdCalibrator:
    """
    Calibrates fit detection thresholds based on validation data characteristics.
    Adapts thresholds for different dataset types and sizes.
    """
    
    # Default thresholds (from fit_detector.py)
    DEFAULT_THRESHOLDS = {
        "classification": {
            "good_fit_train_min": 0.80,
            "good_fit_val_min": 0.75,
            "good_fit_gap_max": 0.08,
            "good_fit_train_very_high": 0.85,
            "good_fit_gap_max_relaxed": 0.12,
            "overfit_gap_threshold": 0.15,
            "overfit_train_min": 0.75,
            "severe_overfit_gap": 0.20,
            "severe_overfit_train_min": 0.65,
            "underfit_val_max": 0.60,
            "underfit_train_max": 0.62,
            "underfit_both_max": 0.65,
            "large_gap_threshold": 0.15
        },
        "regression": {
            "good_fit_train_min": 0.70,
            "good_fit_val_min": 0.65,
            "good_fit_gap_max": 0.10,
            "good_fit_train_high": 0.80,
            "good_fit_gap_relaxed": 0.15,
            "overfit_gap_threshold": 0.20,
            "overfit_train_min": 0.65,
            "severe_overfit_gap": 0.30,
            "underfit_train_max": 0.55,
            "underfit_val_max": 0.50,
            "underfit_both_max": 0.55,
            "large_gap_threshold": 0.20
        }
    }
    
    def __init__(self, problem_type: str = "classification"):
        """
        Initialize calibrator with problem type.
        
        Parameters:
        -----------
        problem_type : str
            'classification' or 'regression'
        """
        self.problem_type = problem_type
        self.thresholds = self.DEFAULT_THRESHOLDS[problem_type].copy()
        self.calibration_history = []
    
    def calibrate_from_validation_behavior(self, 
                                          train_scores: np.ndarray,
                                          val_scores: np.ndarray,
                                          fit_statuses: np.ndarray) -> Dict:
        """
        Calibrate thresholds based on observed validation behavior.
        
        Uses empirical percentiles from observed data to adjust detection thresholds.
        
        Parameters:
        -----------
        train_scores : ndarray
            Array of training scores from multiple models
        val_scores : ndarray
            Array of validation scores from multiple models
        fit_statuses : ndarray
            Array of fit statuses from multiple models
            
        Returns:
        --------
        dict : Calibrated thresholds and calibration metrics
        """
        
        print(f"\n🎯 Threshold Calibration Engine")
        print(f"   Problem Type: {self.problem_type}")
        print(f"   Samples: {len(train_scores)}")
        
        # Compute gaps
        gaps = np.abs(train_scores - val_scores)
        
        # Analyze distribution of scores
        train_stats = {
            "mean": float(np.mean(train_scores)),
            "std": float(np.std(train_scores)),
            "min": float(np.min(train_scores)),
            "max": float(np.max(train_scores)),
            "25th_percentile": float(np.percentile(train_scores, 25)),
            "50th_percentile": float(np.percentile(train_scores, 50)),
            "75th_percentile": float(np.percentile(train_scores, 75))
        }
        
        val_stats = {
            "mean": float(np.mean(val_scores)),
            "std": float(np.std(val_scores)),
            "min": float(np.min(val_scores)),
            "max": float(np.max(val_scores)),
            "25th_percentile": float(np.percentile(val_scores, 25)),
            "50th_percentile": float(np.percentile(val_scores, 50)),
            "75th_percentile": float(np.percentile(val_scores, 75))
        }
        
        gap_stats = {
            "mean": float(np.mean(gaps)),
            "std": float(np.std(gaps)),
            "min": float(np.min(gaps)),
            "max": float(np.max(gaps)),
            "90th_percentile": float(np.percentile(gaps, 90))
        }
        
        print(f"\n   📊 Score Statistics:")
        print(f"   Train: μ={train_stats['mean']:.3f}, σ={train_stats['std']:.3f}")
        print(f"   Val:   μ={val_stats['mean']:.3f}, σ={val_stats['std']:.3f}")
        print(f"   Gap:   μ={gap_stats['mean']:.3f}, σ={gap_stats['std']:.3f}")
        
        # Segment by fit status
        good_fits = fit_statuses == "Good Fit"
        overfits = fit_statuses == "Overfitting"
        underfits = fit_statuses == "Underfitting"
        
        calibrated = self.thresholds.copy()
        adjustments = {}
        
        # Adjust Good Fit thresholds (conservative: use actual distribution)
        if np.sum(good_fits) > 0:
            good_fit_train_scores = train_scores[good_fits]
            good_fit_val_scores = val_scores[good_fits]
            good_fit_gaps = gaps[good_fits]
            
            # Set thresholds slightlybelow observed minimums for good fits
            min_good_train = float(np.min(good_fit_train_scores))
            min_good_val = float(np.min(good_fit_val_scores))
            max_good_gap = float(np.max(good_fit_gaps))
            
            # Adjust down by 5% for slight relaxation
            calibrated["good_fit_train_min"] = max(0.5, min_good_train - 0.05)
            calibrated["good_fit_val_min"] = max(0.4, min_good_val - 0.05)
            calibrated["good_fit_gap_max"] = max_good_gap + 0.02  # Small buffer
            
            adjustments["good_fit"] = {
                "old_train_min": self.thresholds["good_fit_train_min"],
                "new_train_min": calibrated["good_fit_train_min"],
                "old_gap_max": self.thresholds["good_fit_gap_max"],
                "new_gap_max": calibrated["good_fit_gap_max"]
            }
            
            print(f"\n   ✓ Good Fit thresholds calibrated")
            print(f"     Train min: {self.thresholds['good_fit_train_min']:.3f} → {calibrated['good_fit_train_min']:.3f}")
            print(f"     Gap max:   {self.thresholds['good_fit_gap_max']:.3f} → {calibrated['good_fit_gap_max']:.3f}")
        
        # Adjust Overfitting thresholds
        if np.sum(overfits) > 0:
            overfit_train = train_scores[overfits]
            overfit_val = val_scores[overfits]
            overfit_gaps = gaps[overfits]
            
            # Overfitting characterized by large train-val gap
            min_overfit_gap = float(np.min(overfit_gaps))
            
            # Set threshold at or slightly below minimum observed overfit gap
            calibrated["overfit_gap_threshold"] = max(0.05, min_overfit_gap - 0.02)
            
            adjustments["overfitting"] = {
                "old_gap_threshold": self.thresholds["overfit_gap_threshold"],
                "new_gap_threshold": calibrated["overfit_gap_threshold"]
            }
            
            print(f"\n   ✓ Overfitting thresholds calibrated")
            print(f"     Gap threshold: {self.thresholds['overfit_gap_threshold']:.3f} → {calibrated['overfit_gap_threshold']:.3f}")
        
        # Adjust Underfitting thresholds
        if np.sum(underfits) > 0:
            underfit_val = val_scores[underfits]
            underfit_train = train_scores[underfits]
            
            # Underfitting characterized by low validation scores
            max_underfit_val = float(np.max(underfit_val))
            max_underfit_train = float(np.max(underfit_train))
            
            # Set threshold at or slightly above maximum observed underfit score
            calibrated["underfit_val_max"] = max_underfit_val + 0.03
            calibrated["underfit_train_max"] = max_underfit_train + 0.03
            
            adjustments["underfitting"] = {
                "old_val_max": self.thresholds["underfit_val_max"],
                "new_val_max": calibrated["underfit_val_max"]
            }
            
            print(f"\n   ✓ Underfitting thresholds calibrated")
            print(f"     Val max: {self.thresholds['underfit_val_max']:.3f} → {calibrated['underfit_val_max']:.3f}")
        
        self.thresholds = calibrated
        
        return {
            "calibrated": True,
            "problem_type": self.problem_type,
            "train_statistics": train_stats,
            "val_statistics": val_stats,
            "gap_statistics": gap_stats,
            "original_thresholds": self.DEFAULT_THRESHOLDS[self.problem_type],
            "calibrated_thresholds": calibrated,
            "adjustments": adjustments
        }
    
    def calibrate_from_experiment_history(self, max_experiments: int = 50) -> Dict:
        """
        Calibrate thresholds from historical experiment data in database.
        
        Parameters:
        -----------
        max_experiments : int
            Maximum number of recent experiments to use for calibration
            
        Returns:
        --------
        dict : Calibration results
        """
        
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            
            # Retrieve recent model results
            query = '''
                SELECT mr.train_score, mr.val_score, mr.fit_status, e.problem_type
                FROM model_results mr
                JOIN experiments e ON mr.experiment_id = e.id
                WHERE e.problem_type = ?
                ORDER BY e.timestamp DESC
                LIMIT ?
            '''
            
            cursor.execute(query, (self.problem_type, max_experiments * 4))  # Get more to filter
            rows = cursor.fetchall()
            
            if not rows:
                print(f"   ⚠ No historical data for {self.problem_type}")
                return {"calibrated": False, "reason": "No historical data"}
            
            train_scores = np.array([r[0] for r in rows if r[0] is not None])
            val_scores = np.array([r[1] for r in rows if r[1] is not None])
            fit_statuses = np.array([r[2] for r in rows if r[2] is not None])
            
            if len(train_scores) < 10:
                print(f"   ⚠ Insufficient historical data ({len(train_scores)} samples)")
                return {"calibrated": False, "reason": "Insufficient data"}
            
            # Ensure same length
            min_len = min(len(train_scores), len(val_scores), len(fit_statuses))
            train_scores = train_scores[:min_len]
            val_scores = val_scores[:min_len]
            fit_statuses = fit_statuses[:min_len]
            
            print(f"   📚 Using {len(train_scores)} historical results for calibration")
            
            return self.calibrate_from_validation_behavior(train_scores, val_scores, fit_statuses)
            
        except Exception as e:
            print(f"   ✗ Calibration from history failed: {str(e)}")
            return {"calibrated": False, "reason": str(e)}
        finally:
            conn.close()
    
    def get_calibrated_threshold(self, threshold_name: str) -> float:
        """Get current calibrated value for a threshold."""
        return self.thresholds.get(threshold_name, self.DEFAULT_THRESHOLDS[self.problem_type].get(threshold_name, 0.5))
    
    def export_thresholds(self) -> Dict:
        """Export all calibrated thresholds."""
        return {
            "problem_type": self.problem_type,
            "thresholds": self.thresholds,
            "timestamp": str(np.datetime64('now'))
        }


def create_adaptive_fit_detector(problem_type: str, calibrate_from_history: bool = True):
    """
    Create a fit detector that uses calibrated thresholds.
    
    Parameters:
    -----------
    problem_type : str
        'classification' or 'regression'
    calibrate_from_history : bool
        Whether to calibrate from historical experiment data
        
    Returns:
    --------
    dict : Configuration for adaptive fit detection
    """
    
    calibrator = ThresholdCalibrator(problem_type)
    
    if calibrate_from_history:
        calibrator.calibrate_from_experiment_history()
    
    return {
        "problem_type": problem_type,
        "calibrator": calibrator,
        "thresholds": calibrator.export_thresholds()
    }
