"""
Module 7: Model-Specific Hyperparameter Tuning Engine

Orchestrates hyperparameter tuning based on fit status and model type.
Uses model-specific grid search with cross-validation to optimize performance.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import accuracy_score, r2_score
import warnings

warnings.filterwarnings('ignore')


def get_hyperparameter_grid(model_name: str, fit_status: str, problem_type: str, dataset_size: int):
    """
    Generate model-specific hyperparameter grid based on fit status and problem characteristics.
    
    Parameters:
    -----------
    model_name : str
        Name of the model
    fit_status : str
        Current fit status (Good Fit, Overfitting, Underfitting)
    problem_type : str
        'classification' or 'regression'
    dataset_size : int
        Number of training samples
        
    Returns:
    --------
    dict : Hyperparameter grid for GridSearchCV
    """
    
    base_grids = {
        "Logistic Regression": {
            "Good Fit": {
                "C": [0.1, 1.0, 10.0],
                "penalty": ['l2'],
                "solver": ['lbfgs', 'liblinear'],
                "max_iter": [1000, 2000]
            },
            "Overfitting": {
                "C": [0.001, 0.01, 0.1],  # Strong regularization
                "penalty": ['l1', 'l2'],
                "solver": ['liblinear'],
                "max_iter": [2000]
            },
            "Underfitting": {
                "C": [1.0, 10.0, 100.0],  # Weak regularization
                "penalty": ['l2'],
                "solver": ['lbfgs'],
                "max_iter": [2000, 3000]
            }
        },
        
        "Ridge Regression": {
            "Good Fit": {
                "alpha": [0.1, 1.0, 10.0],
                "solver": ['auto', 'svd', 'cholesky']
            },
            "Overfitting": {
                "alpha": [1.0, 10.0, 100.0, 1000.0],  # Strong regularization
                "solver": ['auto']
            },
            "Underfitting": {
                "alpha": [0.001, 0.01, 0.1, 1.0],  # Weak regularization
                "solver": ['auto']
            }
        },
        
        "Random Forest": {
            "Good Fit": {
                "n_estimators": [50, 100, 150],
                "max_depth": [10, 15, 20, None],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "Overfitting": {
                "n_estimators": [100, 200],
                "max_depth": [5, 8, 10],  # Shallow trees to reduce overfitting
                "min_samples_split": [5, 10, 20],  # Higher values prevent small splits
                "min_samples_leaf": [4, 8, 16]
            },
            "Underfitting": {
                "n_estimators": [200, 300, 500],
                "max_depth": [20, 30, None],  # Deeper trees for complexity
                "min_samples_split": [2, 5],
                "min_samples_leaf": [1, 2]
            }
        },
        
        "Gradient Boosting": {
            "Good Fit": {
                "n_estimators": [50, 100, 150],
                "learning_rate": [0.01, 0.05, 0.1],
                "max_depth": [3, 4, 5],
                "subsample": [0.8, 0.9, 1.0]
            },
            "Overfitting": {
                "n_estimators": [50, 100],
                "learning_rate": [0.001, 0.01, 0.05],  # Lower learning rate
                "max_depth": [2, 3, 4],  # Shallow trees
                "subsample": [0.5, 0.7, 0.9]  # Subsampling reduces overfitting
            },
            "Underfitting": {
                "n_estimators": [200, 300, 500],
                "learning_rate": [0.05, 0.1, 0.2],  # Higher learning rate
                "max_depth": [5, 7, 9],  # Deeper trees
                "subsample": [0.9, 1.0]
            }
        },
        
        "Neural Network": {
            "Good Fit": {
                "hidden_layer_sizes": [(32,), (64,), (64, 32), (128, 64)],
                "alpha": [0.0001, 0.001, 0.01],  # L2 regularization
                "learning_rate_init": [0.001, 0.01],
                "batch_size": [16, 32, 64]
            },
            "Overfitting": {
                "hidden_layer_sizes": [(32,), (32, 16)],  # Smaller networks
                "alpha": [0.01, 0.1, 1.0],  # Strong regularization
                "learning_rate_init": [0.0001, 0.001],
                "batch_size": [8, 16, 32]
            },
            "Underfitting": {
                "hidden_layer_sizes": [(128, 64), (256, 128), (256, 128, 64)],  # Larger networks
                "alpha": [0.00001, 0.0001],  # Weak regularization
                "learning_rate_init": [0.001, 0.01, 0.05],
                "batch_size": [16, 32]
            }
        },
        
        "Linear Regression": {
            "Good Fit": {
                "fit_intercept": [True],
                "normalize": [False]
            },
            "Overfitting": {
                "fit_intercept": [True],
                "normalize": [False]
            },
            "Underfitting": {
                "fit_intercept": [True],
                "normalize": [False]
            }
        }
    }
    
    # Get appropriate grid
    if model_name in base_grids:
        grid = base_grids[model_name].get(fit_status, base_grids[model_name].get("Good Fit", {}))
    else:
        grid = {}
    
    # Reduce grid size for very small datasets
    if dataset_size < 50:
        # Reduce complexity for small datasets
        reduced_grid = {}
        for key, values in grid.items():
            if isinstance(values, list):
                reduced_grid[key] = values[::max(1, len(values)//2)]
            else:
                reduced_grid[key] = values
        grid = reduced_grid
    
    return grid


def tune_hyperparameters(model, X_train, X_val, y_train, y_val, model_name: str, fit_status: str, 
                        problem_type: str, cv=5):
    """
    Perform hyperparameter tuning using GridSearchCV.
    
    Parameters:
    -----------
    model : sklearn model
        Model to tune
    X_train : ndarray
        Training features
    X_val : ndarray
        Validation features (for final evaluation)
    y_train : ndarray
        Training labels
    y_val : ndarray
        Validation labels
    model_name : str
        Name of the model
    fit_status : str
        Current fit status
    problem_type : str
        'classification' or 'regression'
    cv : int
        Number of cross-validation folds
        
    Returns:
    --------
    dict : Results containing best model, best params, improvement metrics
    """
    
    print(f"\n🔧 Hyperparameter Tuning: {model_name}")
    print(f"   Status: {fit_status} | Samples: {len(X_train)}")
    
    # Get hyperparameter grid
    param_grid = get_hyperparameter_grid(model_name, fit_status, problem_type, len(X_train))
    
    if not param_grid:
        print(f"   ⚠ No tuning grid available for {model_name}")
        return {
            "tuned": False,
            "reason": "No applicable hyperparameter grid"
        }
    
    # Determine scoring metric
    scoring = 'accuracy' if problem_type == 'classification' else 'r2'
    
    # Use RandomizedSearchCV for large grids, GridSearchCV for small grids
    grid_size = np.prod([len(v) if isinstance(v, list) else 1 for v in param_grid.values()])
    
    if grid_size > 50:
        print(f"   Using RandomizedSearchCV (grid size: {grid_size})")
        search = RandomizedSearchCV(
            model,
            param_grid,
            n_iter=min(20, grid_size),
            cv=min(cv, 3),  # Reduce CV for tuning
            scoring=scoring,
            n_jobs=1,
            random_state=42,
            verbose=0
        )
    else:
        print(f"   Using GridSearchCV (grid size: {grid_size})")
        search = GridSearchCV(
            model,
            param_grid,
            cv=min(cv, 3),
            scoring=scoring,
            n_jobs=1,
            verbose=0
        )
    
    try:
        # Fit the search
        search.fit(X_train, y_train)
        
        best_model = search.best_estimator_
        best_params = search.best_params_
        
        # Evaluate on training and validation sets
        train_score = best_model.score(X_train, y_train)
        val_score = best_model.score(X_val, y_val)
        
        # Get baseline scores for comparison
        baseline_model = model
        baseline_model.fit(X_train, y_train)
        baseline_train = baseline_model.score(X_train, y_train)
        baseline_val = baseline_model.score(X_val, y_val)
        
        # Calculate improvements
        train_improvement = train_score - baseline_train
        val_improvement = val_score - baseline_val
        
        gap_baseline = abs(baseline_train - baseline_val)
        gap_tuned = abs(train_score - val_score)
        gap_improvement = gap_baseline - gap_tuned
        
        print(f"   ✓ Best params found:")
        for key, value in best_params.items():
            print(f"     • {key} = {value}")
        
        print(f"   📊 Results:")
        print(f"     Baseline: train={baseline_train:.4f}, val={baseline_val:.4f}, gap={gap_baseline:.4f}")
        print(f"     Tuned:    train={train_score:.4f}, val={val_score:.4f}, gap={gap_tuned:.4f}")
        print(f"     Improvements: train={train_improvement:+.4f}, val={val_improvement:+.4f}, gap={gap_improvement:+.4f}")
        
        return {
            "tuned": True,
            "best_model": best_model,
            "best_params": best_params,
            "baseline_train_score": float(baseline_train),
            "baseline_val_score": float(baseline_val),
            "baseline_gap": float(gap_baseline),
            "tuned_train_score": float(train_score),
            "tuned_val_score": float(val_score),
            "tuned_gap": float(gap_tuned),
            "train_improvement": float(train_improvement),
            "val_improvement": float(val_improvement),
            "gap_improvement": float(gap_improvement),
            "search_best_score": float(search.best_score_)
        }
        
    except Exception as e:
        print(f"   ✗ Tuning failed: {str(e)}")
        return {
            "tuned": False,
            "reason": str(e)
        }


def apply_tuned_model(tuned_result, model):
    """
    Apply tuned hyperparameters to a fresh model instance.
    
    Parameters:
    -----------
    tuned_result : dict
        Result from tune_hyperparameters
    model : sklearn model
        Model to apply tuning to
        
    Returns:
    --------
    sklearn model : Model with tuned parameters
    """
    if not tuned_result.get("tuned"):
        return model
    
    best_params = tuned_result.get("best_params", {})
    for param, value in best_params.items():
        setattr(model, param, value)
    
    return model
