"""
Module: Feature Importance Analysis

Extracts and analyzes feature importance from tree-based models
- Random Forest
- Gradient Boosting
- Provides visualization-ready data format
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from typing import Dict, List, Tuple, Any


def calculate_feature_importance(
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    y_train: np.ndarray,
    y_val: np.ndarray,
    models: Dict[str, Any],
    task_type: str,
    top_n: int = 10
) -> Dict[str, Any]:
    """
    Calculate feature importance for all models.
    
    Parameters:
    -----------
    X_train, X_val : pd.DataFrame
        Training and validation features
    y_train, y_val : np.ndarray
        Training and validation targets
    models : dict
        Trained models {'model_name': model_object}
    task_type : str
        'classification' or 'regression'
    top_n : int
        Number of top features to return
    
    Returns:
    --------
    dict : Feature importance data for each model
    ```
    {
      'model_name': {
        'importance_type': 'built-in' or 'permutation',
        'top_features': [
          {'feature': 'age', 'importance': 0.25, 'rank': 1},
          ...
        ],
        'all_features': [...],
        'plot_data': [{'name': 'feature', 'importance': 0.25}]
      }
    }
    ```
    """
    
    feature_names = X_train.columns.tolist()
    results = {}
    
    print(f"\n📊 Feature Importance Analysis:")
    print(f"   Dataset: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"   Task: {task_type}")
    print(f"   Top N: {top_n}\n")
    
    for model_name, model in models.items():
        print(f"   🔍 {model_name}:")
        
        try:
            # Check if model has feature_importances_ (tree-based)
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                importance_type = 'built-in'
                print(f"      ✅ Using built-in feature importances")
            else:
                # Use permutation importance for other models
                print(f"      ⚠️  Using permutation importance (may be slow)...")
                perm_importance = permutation_importance(
                    model, X_val, y_val, n_repeats=10, random_state=42, n_jobs=-1
                )
                importances = perm_importance.importances_mean
                importance_type = 'permutation'
                print(f"      ✅ Permutation importance calculated")
            
            # Create feature importance dataframe
            feature_importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Calculate statistics
            total_importance = feature_importance_df['importance'].sum()
            if total_importance > 0:
                feature_importance_df['importance_pct'] = (
                    feature_importance_df['importance'] / total_importance * 100
                )
            else:
                feature_importance_df['importance_pct'] = 0
            
            feature_importance_df['rank'] = range(1, len(feature_importance_df) + 1)
            feature_importance_df['cumsum_pct'] = feature_importance_df['importance_pct'].cumsum()
            
            # Top N features
            top_features = feature_importance_df.head(top_n).to_dict('records')
            
            # All features for detailed view
            all_features = feature_importance_df.to_dict('records')
            
            # Plot data (sorted by importance)
            plot_data = [
                {
                    'name': row['feature'],
                    'importance': round(row['importance_pct'], 2),
                    'rank': int(row['rank'])
                }
                for _, row in feature_importance_df.head(top_n).iterrows()
            ]
            
            # Find 80% threshold
            cumsum_pct = feature_importance_df['cumsum_pct'].values
            features_for_80_pct = np.argmax(cumsum_pct >= 80) + 1 if np.any(cumsum_pct >= 80) else len(feature_importance_df)
            
            results[model_name] = {
                'importance_type': importance_type,
                'top_features': top_features,
                'all_features': all_features,
                'plot_data': plot_data,
                'total_features': len(feature_names),
                'features_for_80_pct': features_for_80_pct,
                'avg_importance': float(feature_importance_df['importance'].mean()),
                'max_importance': float(feature_importance_df['importance'].max()),
                'min_importance': float(feature_importance_df['importance'].min())
            }
            
            print(f"      📈 Top feature: {top_features[0]['feature']} ({top_features[0]['importance_pct']:.1f}%)")
            print(f"      📊 Features explaining 80% importance: {features_for_80_pct}/{len(feature_names)}")
            
        except Exception as e:
            print(f"      ❌ Error calculating importance: {str(e)}")
            results[model_name] = {
                'error': str(e),
                'importance_type': 'error',
                'top_features': [],
                'all_features': [],
                'plot_data': []
            }
    
    print(f"\n✅ Feature importance analysis complete")
    return results


def get_feature_recommendations(
    feature_importance_results: Dict[str, Any],
    threshold_pct: float = 1.0
) -> Dict[str, List[str]]:
    """
    Get feature recommendations based on importance scores.
    
    Identifies:
    - Low importance features (candidates for removal)
    - Redundant features
    - Top predictive features
    
    Parameters:
    -----------
    feature_importance_results : dict
        Output from calculate_feature_importance()
    threshold_pct : float
        Importance percentage threshold for "low importance"
    
    Returns:
    --------
    dict : Recommendations per model
    """
    
    recommendations = {}
    
    for model_name, result in feature_importance_results.items():
        if 'error' in result:
            continue
        
        all_features = pd.DataFrame(result['all_features'])
        
        # Features to consider removing (low importance across all models)
        low_importance_features = all_features[
            all_features['importance_pct'] < threshold_pct
        ]['feature'].tolist()
        
        # Top predictive features
        top_predictive = all_features.head(5)['feature'].tolist()
        
        recommendations[model_name] = {
            'remove_candidates': low_importance_features,
            'top_predictive': top_predictive,
            'action': 'Consider removing low-importance features to reduce noise and improve model interpretability.'
        }
    
    return recommendations
