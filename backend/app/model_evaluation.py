"""
Module: Advanced Model Evaluation

ROC Curves, Confusion Matrices, Classification Metrics
- ROC-AUC scores and curves
- Confusion matrices
- Precision, Recall, F1-Score
- Threshold optimization
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_curve, auc, confusion_matrix, classification_report,
    precision_recall_curve, f1_score, precision_score, recall_score,
    roc_auc_score
)
from sklearn.preprocessing import label_binarize
from typing import Dict, List, Tuple, Any, Optional


def calculate_classification_metrics(
    y_val: np.ndarray,
    y_pred: np.ndarray,
    y_pred_proba: Optional[np.ndarray] = None,
    model_name: str = "Model"
) -> Dict[str, Any]:
    """
    Calculate comprehensive classification metrics.
    
    Parameters:
    -----------
    y_val : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
    y_pred_proba : np.ndarray, optional
        Predicted probabilities (for ROC curve)
    model_name : str
        Name of model for logging
    
    Returns:
    --------
    dict : Comprehensive classification metrics
    """
    
    print(f"\n🎯 Classification Metrics for {model_name}:")
    
    # Confusion matrix
    cm = confusion_matrix(y_val, y_pred)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Basic metrics
    accuracy = (y_pred == y_val).mean()
    precision = precision_score(y_val, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_val, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_val, y_pred, average='weighted', zero_division=0)
    
    # ROC-AUC
    roc_auc = None
    roc_curve_data = None
    
    if y_pred_proba is not None and len(np.unique(y_val)) == 2:
        try:
            roc_auc = roc_auc_score(y_val, y_pred_proba[:, 1])
            fpr, tpr, thresholds = roc_curve(y_val, y_pred_proba[:, 1])
            roc_curve_data = {
                'fpr': fpr.tolist(),
                'tpr': tpr.tolist(),
                'thresholds': thresholds.tolist(),
                'auc': float(roc_auc)
            }
            print(f"   📊 ROC-AUC: {roc_auc:.4f}")
        except Exception as e:
            print(f"   ⚠️  ROC-AUC calculation failed: {str(e)}")
    
    # Precision-Recall curve
    pr_curve_data = None
    if y_pred_proba is not None and len(np.unique(y_val)) == 2:
        try:
            precision_curve, recall_curve, _ = precision_recall_curve(y_val, y_pred_proba[:, 1])
            pr_auc = auc(recall_curve, precision_curve)
            pr_curve_data = {
                'precision': precision_curve.tolist(),
                'recall': recall_curve.tolist(),
                'auc': float(pr_auc)
            }
        except Exception as e:
            print(f"   ⚠️  PR-AUC calculation failed: {str(e)}")
    
    # Classification report
    class_report = classification_report(y_val, y_pred, output_dict=True, zero_division=0)
    
    # Confusion matrix data for heatmap
    cm_data = {
        'confusion_matrix': cm.tolist(),
        'confusion_matrix_normalized': cm_normalized.tolist(),
        'shape': cm.shape
    }
    
    print(f"   ✅ Accuracy: {accuracy:.4f}")
    print(f"   ✅ Precision: {precision:.4f}")
    print(f"   ✅ Recall: {recall:.4f}")
    print(f"   ✅ F1-Score: {f1:.4f}")
    
    return {
        'model_name': model_name,
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'roc_auc': float(roc_auc) if roc_auc else None,
        'confusion_matrix': cm_data,
        'roc_curve': roc_curve_data,
        'pr_curve': pr_curve_data,
        'classification_report': class_report,
        'per_class_metrics': extract_per_class_metrics(class_report)
    }


def extract_per_class_metrics(class_report: Dict) -> List[Dict]:
    """Extract per-class precision, recall, f1 for visualization."""
    metrics = []
    for label, scores in class_report.items():
        if label not in ['accuracy', 'macro avg', 'weighted avg']:
            metrics.append({
                'class': str(label),
                'precision': float(scores.get('precision', 0)),
                'recall': float(scores.get('recall', 0)),
                'f1_score': float(scores.get('f1-score', 0)),
                'support': int(scores.get('support', 0))
            })
    return metrics


def find_optimal_threshold(
    y_val: np.ndarray,
    y_pred_proba: np.ndarray,
    metric: str = 'f1'
) -> Dict[str, Any]:
    """
    Find optimal classification threshold.
    
    Parameters:
    -----------
    y_val : np.ndarray
        True labels
    y_pred_proba : np.ndarray
        Predicted probabilities
    metric : str
        Metric to optimize ('f1', 'precision', 'recall', 'accuracy')
    
    Returns:
    --------
    dict : Optimal threshold info
    """
    
    if len(np.unique(y_val)) != 2:
        return {'error': 'Only binary classification supported'}
    
    thresholds = np.arange(0.1, 1.0, 0.05)
    scores = []
    
    for threshold in thresholds:
        y_pred_thresh = (y_pred_proba[:, 1] >= threshold).astype(int)
        
        if metric == 'f1':
            score = f1_score(y_val, y_pred_thresh, zero_division=0)
        elif metric == 'precision':
            score = precision_score(y_val, y_pred_thresh, zero_division=0)
        elif metric == 'recall':
            score = recall_score(y_val, y_pred_thresh, zero_division=0)
        else:  # accuracy
            score = (y_pred_thresh == y_val).mean()
        
        scores.append(score)
    
    optimal_idx = np.argmax(scores)
    optimal_threshold = thresholds[optimal_idx]
    
    return {
        'optimal_threshold': float(optimal_threshold),
        'optimal_score': float(scores[optimal_idx]),
        'metric': metric,
        'threshold_scores': [
            {'threshold': float(t), 'score': float(s)}
            for t, s in zip(thresholds, scores)
        ]
    }


def generate_classification_summary(
    metrics_per_model: Dict[str, Dict]
) -> Dict[str, Any]:
    """
    Generate summary of classification performance across models.
    
    Parameters:
    -----------
    metrics_per_model : dict
        Output from calculate_classification_metrics for multiple models
    
    Returns:
    --------
    dict : Summary with rankings and recommendations
    """
    
    # Rank models by F1-score
    rankings = []
    for model_name, metrics in metrics_per_model.items():
        rankings.append({
            'model': model_name,
            'f1_score': metrics['f1_score'],
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'roc_auc': metrics['roc_auc'] if metrics['roc_auc'] else 0
        })
    
    rankings = sorted(rankings, key=lambda x: x['f1_score'], reverse=True)
    
    return {
        'best_model': rankings[0]['model'] if rankings else None,
        'rankings': rankings,
        'average_f1': np.mean([r['f1_score'] for r in rankings]),
        'top_metric': max([r['f1_score'] for r in rankings]) if rankings else 0,
        'recommendation': f"Best model: {rankings[0]['model'] if rankings else 'N/A'} (F1: {rankings[0]['f1_score']:.3f})"
    }
