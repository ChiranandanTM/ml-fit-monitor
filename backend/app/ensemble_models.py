"""
Module: Ensemble Model Creation

Combine multiple models for improved performance
- Voting Classifier/Regressor
- Stacking Ensemble
- Blending strategies
- Ensemble performance analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier, VotingRegressor, StackingClassifier, StackingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any, Tuple, Optional


def create_voting_ensemble(
    models: Dict[str, Any],
    task_type: str = 'classification',
    voting: str = 'hard'
) -> Any:
    """
    Create voting ensemble from trained models.
    
    Parameters:
    -----------
    models : dict
        Trained models {'model_name': model_object}
    task_type : str
        'classification' or 'regression'
    voting : str
        'hard' or 'soft' for classification
    
    Returns:
    --------
    VotingClassifier or VotingRegressor : Trained ensemble
    """
    
    print(f"\n🎯 Creating Voting Ensemble ({voting} voting):")
    print(f"   Models included: {len(models)}")
    
    estimators = [(name, model) for name, model in models.items()]
    
    if task_type == 'classification':
        ensemble = VotingClassifier(estimators=estimators, voting=voting)
    else:
        ensemble = VotingRegressor(estimators=estimators)
    
    print(f"   ✅ Voting ensemble created")
    return ensemble


def create_stacking_ensemble(
    base_models: Dict[str, Any],
    meta_model: Optional[Any] = None,
    task_type: str = 'classification',
    cv: int = 5
) -> Any:
    """
    Create stacking ensemble using meta-learner.
    
    Parameters:
    -----------
    base_models : dict
        Base models {'name': model}
    meta_model : object, optional
        Meta-learner for combining predictions
    task_type : str
        'classification' or 'regression'
    cv : int
        Cross-validation folds
    
    Returns:
    --------
    StackingClassifier or StackingRegressor : Stacking ensemble
    """
    
    print(f"\n📚 Creating Stacking Ensemble (cv={cv}):")
    print(f"   Base models: {len(base_models)}")
    
    estimators = [(name, model) for name, model in base_models.items()]
    
    # Use default meta-learner if not provided
    if meta_model is None:
        if task_type == 'classification':
            meta_model = LogisticRegression(max_iter=1000)
        else:
            meta_model = Ridge()
        print(f"   Using default meta-learner")
    else:
        print(f"   Using custom meta-learner")
    
    if task_type == 'classification':
        ensemble = StackingClassifier(
            estimators=estimators,
            final_estimator=meta_model,
            cv=cv,
            stack_method='predict_proba'
        )
    else:
        ensemble = StackingRegressor(
            estimators=estimators,
            final_estimator=meta_model,
            cv=cv
        )
    
    print(f"   ✅ Stacking ensemble created")
    return ensemble


def evaluate_ensemble_performance(
    ensemble: Any,
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    y_train: np.ndarray,
    y_val: np.ndarray,
    individual_models: Dict[str, Any],
    task_type: str = 'classification'
) -> Dict[str, Any]:
    """
    Evaluate ensemble vs individual models.
    
    Parameters:
    -----------
    ensemble : object
        Trained ensemble
    X_train, X_val : pd.DataFrame
        Training and validation features
    y_train, y_val : np.ndarray
        Training and validation targets
    individual_models : dict
        Individual models for comparison
    task_type : str
        'classification' or 'regression'
    
    Returns:
    --------
    dict : Performance comparison
    """
    
    print(f"\n🔍 Ensemble Performance Analysis:")
    
    # Train ensemble
    print(f"   Training ensemble...")
    ensemble.fit(X_train, y_train)
    
    # Get ensemble scores
    ensemble_train_score = ensemble.score(X_train, y_train)
    ensemble_val_score = ensemble.score(X_val, y_val)
    ensemble_gap = abs(ensemble_train_score - ensemble_val_score)
    
    print(f"   Ensemble - Train: {ensemble_train_score:.4f}, Val: {ensemble_val_score:.4f}, Gap: {ensemble_gap:.4f}")
    
    # Compare with individual models
    comparison = {
        'ensemble': {
            'name': 'Ensemble',
            'train_score': float(ensemble_train_score),
            'val_score': float(ensemble_val_score),
            'gap': float(ensemble_gap),
            'improvement_over_best': 0.0
        },
        'individual_models': {}
    }
    
    best_val_score = 0
    for model_name, model in individual_models.items():
        train_score = model.score(X_train, y_train)
        val_score = model.score(X_val, y_val)
        gap = abs(train_score - val_score)
        
        best_val_score = max(best_val_score, val_score)
        
        comparison['individual_models'][model_name] = {
            'train_score': float(train_score),
            'val_score': float(val_score),
            'gap': float(gap)
        }
        
        print(f"   {model_name} - Train: {train_score:.4f}, Val: {val_score:.4f}, Gap: {gap:.4f}")
    
    # Calculate improvement
    if best_val_score > 0:
        improvement = ((ensemble_val_score - best_val_score) / best_val_score) * 100
        comparison['ensemble']['improvement_over_best'] = float(improvement)
        
        if improvement > 0:
            print(f"\n   ✅ Ensemble improves by {improvement:.2f}% over best individual model")
        else:
            print(f"\n   ⚠️  Ensemble performs {abs(improvement):.2f}% worse than best model")
    
    # Feature contributions (for stacking)
    if hasattr(ensemble, 'stack_method'):
        print(f"\n   📊 Using stack method: {ensemble.stack_method}")
    
    # Recommendations
    recommendations = []
    if ensemble_val_score > best_val_score:
        recommendations.append("✅ Use ensemble - it provides improvement")
    else:
        recommendations.append("⚠️  Best individual model may be sufficient")
    
    if ensemble_gap < 0.10:
        recommendations.append("✅ Good generalization - low train-val gap")
    else:
        recommendations.append("⚠️  Consider regularization - high generalization gap")
    
    comparison['recommendations'] = recommendations
    comparison['ensemble_object'] = ensemble
    
    return comparison


def get_ensemble_contribution_analysis(
    ensemble: Any,
    base_model_names: List[str]
) -> Dict[str, Any]:
    """
    Analyze contribution of each base model to ensemble.
    
    Parameters:
    -----------
    ensemble : object
        Trained ensemble
    base_model_names : list
        Names of base models
    
    Returns:
    --------
    dict : Contribution analysis
    """
    
    contributions = {}
    
    if hasattr(ensemble, 'estimators_'):
        print(f"\n📊 Base Model Contributions:")
        for name, estimator in zip(base_model_names, ensemble.estimators_):
            if hasattr(estimator, 'feature_importances_'):
                importance = estimator.feature_importances_.mean()
            else:
                importance = 0.5  # Default for linear models
            
            contributions[name] = float(importance)
            print(f"   {name}: {importance:.4f}")
    
    return {
        'model_contributions': contributions,
        'average_contribution': np.mean(list(contributions.values())) if contributions else 0
    }


def extract_ensemble_metadata(ensemble: Any) -> Dict[str, Any]:
    """
    Extract metadata and configuration from ensemble.
    
    Parameters:
    -----------
    ensemble : object
        Trained ensemble
    
    Returns:
    --------
    dict : Ensemble configuration
    """
    
    metadata = {
        'type': type(ensemble).__name__,
        'params': ensemble.get_params()
    }
    
    if hasattr(ensemble, 'estimators_'):
        metadata['num_estimators'] = len(ensemble.estimators_)
        metadata['estimator_names'] = [name for name, _ in ensemble.estimators_]
    
    if hasattr(ensemble, 'n_features_in_'):
        metadata['n_features'] = ensemble.n_features_in_
    
    return metadata
