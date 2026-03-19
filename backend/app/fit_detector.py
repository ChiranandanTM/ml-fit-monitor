"""
Module 3: Overfitting/Underfitting Detection Engine

Core Logic:
- Classification: Uses Accuracy scores (0-1 scale, higher is better)
- Regression: Uses R² scores (0-1 scale, higher is better)
- Generalization Gap = |train_score - val_score|
- Detects bias-variance trade-off and threshold-based classification
"""


def detect_fit_status(train_score, val_score, task_type):
    """
    Automatically detect overfitting, underfitting, or good fit.
    
    Parameters:
    -----------
    train_score : float
        Training set performance (accuracy for classification, R² for regression)
    val_score : float
        Validation set performance
    task_type : str
        'classification' or 'regression'
    
    Returns:
    --------
    str : One of ['Good Fit', 'Overfitting', 'Underfitting', 'Error']
    
    Mathematical Thresholds:
    - Good Fit: train ≥ 0.80 AND val ≥ 0.75 AND gap ≤ 0.08
    - Overfitting: (train - val > 0.15) AND train > 0.75
    - Underfitting: train < 0.65 OR val < 0.62
    """
    
    gap = abs(train_score - val_score)
    
    # Handle classification
    if task_type == "classification":
        print(f"    🔍 Classification Fit Detection:")
        print(f"       Train Accuracy: {train_score:.4f} ({train_score*100:.2f}%)")
        print(f"       Val Accuracy:   {val_score:.4f} ({val_score*100:.2f}%)")
        print(f"       Generalization Gap: {gap:.4f}")
        
        # DECISION 1: GOOD FIT
        # Criteria: Both scores high and well-balanced
        if train_score >= 0.80 and val_score >= 0.75 and gap <= 0.08:
            print(f"       ✅ DECISION: GOOD FIT")
            print(f"          Reason: High train ({train_score:.1%}) + High val ({val_score:.1%}) + Small gap ({gap:.1%})")
            return "Good Fit"
        
        if train_score >= 0.85 and val_score >= 0.75 and gap <= 0.12:
            print(f"       ✅ DECISION: GOOD FIT")
            print(f"          Reason: Very high scores with manageable gap")
            return "Good Fit"
        
        # DECISION 2: OVERFITTING
        # Criteria: High train, significant drop in validation
        if (train_score - val_score) > 0.15 and train_score > 0.75:
            print(f"       ⚠️  DECISION: OVERFITTING")
            print(f"          Reason: Large gap ({gap:.1%}) with high train score - memorization signal")
            return "Overfitting"
        
        if (train_score - val_score) > 0.20 and train_score > 0.65:
            print(f"       ⚠️  DECISION: OVERFITTING")
            print(f"          Reason: Very large train-val gap ({gap:.1%}) - severe overfitting")
            return "Overfitting"
        
        if train_score > 0.85 and val_score < 0.70 and gap >= 0.15:
            print(f"       ⚠️  DECISION: OVERFITTING")
            print(f"          Reason: Near-perfect training but poor generalization")
            return "Overfitting"
        
        # DECISION 3: UNDERFITTING
        # Criteria: Low scores indicating poor learning
        if val_score < 0.60:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Validation score too low ({val_score:.1%}) - poor generalization")
            return "Underfitting"
        
        if train_score < 0.62:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Training score too low ({train_score:.1%}) - weak learning")
            return "Underfitting"
        
        if train_score < 0.70 and val_score < 0.65:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Both scores below threshold - insufficient model capacity")
            return "Underfitting"
        
        # Default fallback
        if gap > 0.15:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Large gap with moderate training score suggests underfitting")
            return "Underfitting"
        
        print(f"       ❌ DECISION: UNDERFITTING (fallback)")
        print(f"          Reason: Scores not high enough for good fit classification")
        return "Underfitting"
    
    # Handle regression (R² scores)
    else:
        print(f"    🔍 Regression Fit Detection (R² basis):")
        print(f"       Train R²: {train_score:.4f}")
        print(f"       Val R²:   {val_score:.4f}")
        print(f"       Generalization Gap: {gap:.4f}")
        
        # DECISION 1: GOOD FIT
        # Criteria: High R² with balanced train-val
        if train_score >= 0.80 and val_score >= 0.75 and gap <= 0.10:
            print(f"       ✅ DECISION: GOOD FIT")
            print(f"          Reason: High R² ({train_score:.1%}) with good generalization")
            return "Good Fit"
        
        if train_score >= 0.85 and val_score >= 0.75 and gap <= 0.15:
            print(f"       ✅ DECISION: GOOD FIT")
            print(f"          Reason: Very high R² scores")
            return "Good Fit"
        
        # DECISION 2: OVERFITTING
        # Criteria: Good train R² but poor validation
        if (train_score - val_score) > 0.15 and train_score > 0.75:
            print(f"       ⚠️  DECISION: OVERFITTING")
            print(f"          Reason: Large R² gap ({gap:.1%}) - model overfitted to training")
            return "Overfitting"
        
        if train_score > 0.85 and val_score < 0.70 and gap >= 0.15:
            print(f"       ⚠️  DECISION: OVERFITTING")
            print(f"          Reason: Excellent train R² but poor validation")
            return "Overfitting"
        
        # DECISION 3: UNDERFITTING
        # Criteria: Low R² scores
        if val_score < 0.55:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Validation R² too low ({val_score:.1%}) - insufficient fit")
            return "Underfitting"
        
        if train_score < 0.60:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Training R² ({train_score:.1%}) too low - weak learning")
            return "Underfitting"
        
        if train_score < 0.70 and val_score < 0.65:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Both R² scores below threshold")
            return "Underfitting"
        
        # Default fallback
        if gap > 0.15:
            print(f"       ❌ DECISION: UNDERFITTING")
            print(f"          Reason: Large R² gap suggests underfitting")
            return "Underfitting"
        
        print(f"       ❌ DECISION: UNDERFITTING (fallback)")
        print(f"          Reason: Insufficient model performance")
        return "Underfitting"


def generate_fit_explanation(fit_status, train_score, val_score, bias, variance):
    """
    Generate human-readable explanation of fit status with bias-variance analysis.
    
    Returns:
    --------
    dict : Detailed explanation with recommendations
    """
    gap = abs(train_score - val_score)
    
    explanation = {
        "status": fit_status,
        "summary": "",
        "bias_variance_signal": "",
        "severity": "",
        "next_steps": []
    }
    
    if fit_status == "Good Fit":
        explanation["summary"] = (
            f"✅ Model is well-balanced with {train_score*100:.1f}% training and "
            f"{val_score*100:.1f}% validation performance. Model generalizes well."
        )
        explanation["bias_variance_signal"] = (
            f"Bias: {bias:.1%} (acceptable) | Variance: {variance:.1%} (minimal)"
        )
        explanation["severity"] = "NONE - Model ready for production"
        explanation["next_steps"] = [
            "Deploy model with confidence monitoring",
            "Set up data drift detection",
            "Plan periodic retraining schedule"
        ]
    
    elif fit_status == "Overfitting":
        explanation["summary"] = (
            f"⚠️ Model shows signs of OVERFITTING. Training performance ({train_score*100:.1f}%) "
            f"is much higher than validation ({val_score*100:.1f}%). Model may have memorized "
            f"training data and won't generalize well."
        )
        explanation["bias_variance_signal"] = (
            f"Bias: {bias:.1%} (low) | Variance: {variance:.1%} (HIGH)"
        )
        explanation["severity"] = "HIGH - Immediate action required"
        explanation["next_steps"] = [
            "Increase regularization (L1/L2 penalties)",
            "Reduce model complexity or feature count",
            "Collect more training data",
            "Apply dropout/early stopping (neural networks)",
            "Use cross-validation for robust tuning"
        ]
    
    elif fit_status == "Underfitting":
        explanation["summary"] = (
            f"❌ Model shows signs of UNDERFITTING. Both training ({train_score*100:.1f}%) and "
            f"validation ({val_score*100:.1f}%) scores are too low. Model lacks sufficient capacity."
        )
        explanation["bias_variance_signal"] = (
            f"Bias: {bias:.1%} (HIGH) | Variance: {variance:.1%} (low)"
        )
        explanation["severity"] = "CRITICAL - Model needs restructuring"
        explanation["next_steps"] = [
            "Increase model complexity (deeper network, more trees)",
            "Add more features or engineer new features",
            "Reduce regularization constraints",
            "Try more powerful algorithms (ensemble methods)",
            "Collect more training data"
        ]
    
    return explanation
