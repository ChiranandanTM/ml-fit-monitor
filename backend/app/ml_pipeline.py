import numpy as np
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, cross_validate
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, mean_squared_error, r2_score, confusion_matrix, roc_auc_score, roc_curve, auc
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
from .fit_detector import detect_fit_status
from .model_evaluation import calculate_classification_metrics

# Suppress convergence warnings so they don't crash training
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*ConvergenceWarning.*')
try:
    from sklearn.exceptions import ConvergenceWarning
    warnings.filterwarnings('ignore', category=ConvergenceWarning)
except ImportError:
    pass


def get_adaptive_cv(n_samples, y=None, problem_type="classification"):
    """Calculate adaptive number of CV folds based on dataset size and class distribution."""
    if problem_type == "classification" and y is not None:
        unique, counts = np.unique(y, return_counts=True)
        min_class_count = int(min(counts))
        # Each fold needs at least 1 sample of each class
        max_folds = min_class_count
    else:
        max_folds = n_samples
    
    # FAST: Use at most 3 folds instead of 5, minimum 2
    cv = min(3, max_folds)  # CHANGED: 5 → 3
    cv = max(2, cv)
    return cv


def safe_float(value):
    """Safely convert value to float, handling edge cases"""
    try:
        if value is None or pd.isna(value) or np.isinf(value):
            return 0.0
    except (TypeError, ValueError):
        pass
    try:
        f = float(value)
        if np.isnan(f) or np.isinf(f):
            return 0.0
        return f
    except (TypeError, ValueError):
        return 0.0


def sanitize_for_json(obj):
    """Recursively sanitize a data structure so it is JSON-serializable.
    Replaces NaN / Inf floats with 0.0."""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return 0.0
        return obj
    if isinstance(obj, (np.floating, np.integer)):
        f = float(obj)
        if np.isnan(f) or np.isinf(f):
            return 0.0
        return f
    if isinstance(obj, np.ndarray):
        return sanitize_for_json(obj.tolist())
    return obj


def detect_problem_type(y):
    """Automatically detect if problem is classification or regression"""
    unique_values = len(np.unique(y))
    
    # Heuristics:
    # - If < 30 unique values and appears to be discrete → Classification
    # - If > 30 unique values or continuous values → Regression
    if unique_values <= 30:
        # Check if values are mostly integers
        y_numeric = pd.to_numeric(y, errors='coerce')
        if (y_numeric == y_numeric.astype(int)).sum() / len(y_numeric) > 0.9:
            if unique_values >= 2:
                return "classification"
    
    return "regression" if unique_values > 30 else "classification"


def detect_outliers_iqr(X, threshold=1.5):
    """Detect outliers using IQR method"""
    Q1 = np.percentile(X, 25, axis=0)
    Q3 = np.percentile(X, 75, axis=0)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    outliers = np.any((X < lower_bound) | (X > upper_bound), axis=1)
    return np.where(outliers)[0]


def calculate_learning_curves(model, X, y, problem_type, cv=None):
    """Generate learning curve data (train size vs score) - OPTIMIZED VERSION"""
    try:
        if cv is None:
            cv = get_adaptive_cv(len(y), y, problem_type)
        
        if problem_type == "classification":
            scoring = 'accuracy'
        else:
            scoring = 'r2'
        
        # For fast performance: use only 2-3 points instead of 5-10
        n_samples = len(y)
        if n_samples < 50:
            n_points = 2  # FAST: Only 2 points for small datasets
        elif n_samples < 200:
            n_points = 3  # FAST: Only 3 points for medium datasets
        else:
            n_points = 4  # FAST: Only 4 points for larger datasets
        
        train_sizes, train_scores, val_scores = learning_curve(
            model, X, y, cv=min(2, cv),  # FAST: Use max 2 folds instead of adaptive
            train_sizes=np.linspace(0.3, 1.0, n_points),  # FAST: Start at 0.3 instead of 0.2
            scoring=scoring,
            n_jobs=1,
            shuffle=False  # FAST: Disable shuffle
        )
        
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)
        
        return sanitize_for_json({
            "train_sizes": train_sizes.tolist(),
            "train_mean": train_mean.tolist(),
            "train_std": train_std.tolist(),
            "val_mean": val_mean.tolist(),
            "val_std": val_std.tolist()
        })
    except Exception as e:
        print(f"  ⚠ Learning curve failed: {str(e)}")
        return None


def calculate_cv_confidence_intervals(cv_scores, confidence=0.95):
    """Calculate 95% confidence intervals from cross-validation scores"""
    mean_score = np.mean(cv_scores)
    std_score = np.std(cv_scores)
    n = len(cv_scores)
    
    # t-statistic for 95% confidence with n-1 degrees of freedom
    t_stat = stats.t.ppf((1 + confidence) / 2, n - 1)
    margin_of_error = t_stat * (std_score / np.sqrt(n))
    
    return {
        "mean": safe_float(mean_score),
        "std": safe_float(std_score),
        "ci_lower": safe_float(mean_score - margin_of_error),
        "ci_upper": safe_float(mean_score + margin_of_error),
        "margin": safe_float(margin_of_error)
    }


def calculate_bias_variance(cv_scores):
    """Calculate bias and variance indicators from CV scores"""
    mean_cv = np.mean(cv_scores)
    std_cv = np.std(cv_scores)
    
    # Bias: How far from perfect (1.0)
    bias = 1.0 - mean_cv
    
    # Variance: Sensitivity to training data changes
    variance = std_cv
    
    return {
        "bias": safe_float(bias),
        "variance": safe_float(variance),
        "bias_variance_ratio": safe_float(bias / (variance + 1e-10))
    }


def clean_dataframe(df):
    """Clean and prepare dataframe for training - handles mixed data types"""
    print(f"\n📥 Input Data Analysis:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {df.columns.tolist()}")
    print(f"  Dtypes:\n{df.dtypes}")
    
    # Remove completely empty rows
    df = df.dropna(how="all")
    print(f"  After removing empty rows: {df.shape[0]} rows")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")
    print(f"  After removing empty columns: {df.shape[1]} columns")

    # Remove columns with too many NaN values (>70%)
    threshold = len(df) * 0.3  # Keep columns with at least 30% data
    df = df.dropna(axis=1, thresh=threshold)
    print(f"  After removing sparse columns: {df.shape[1]} columns")

    if df.shape[0] == 0:
        raise ValueError("No valid data rows found. Dataset is empty after cleaning.")
    
    if df.shape[1] < 2:
        raise ValueError(f"Not enough columns. Found {df.shape[1]}, need at least 2 (features + target).")

    print(f"\n🔄 Processing columns:")
    
    # Process each column - try numeric first, then categorical
    processed_cols = {}
    col_types = {}
    
    for i, col in enumerate(df.columns):
        is_target = (i == len(df.columns) - 1)  # Last column is target
        try:
            # Try to convert to numeric
            numeric_col = pd.to_numeric(df[col], errors='coerce')
            valid_count = numeric_col.notna().sum()
            valid_ratio = valid_count / len(df)
            
            # If mostly numeric, use numeric
            if valid_ratio > 0.5:
                filled = numeric_col.fillna(numeric_col.median() or 0)
                processed_cols[col] = filled
                col_types[col] = "numeric"
                print(f"  ✓ {col}: numeric ({valid_count}/{len(df)} valid)" + (" [TARGET]" if is_target else ""))
            else:
                # Try categorical encoding
                fill_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'unknown'
                categorical = df[col].fillna(fill_value).astype(str)
                
                # Check for unique values
                n_unique = len(categorical.unique())
                if n_unique == 1:
                    print(f"  ⚠ {col}: only 1 unique value, SKIPPING")
                    continue
                
                le = LabelEncoder()
                encoded = le.fit_transform(categorical)
                processed_cols[col] = encoded
                col_types[col] = f"categorical({n_unique} classes)"
                print(f"  ✓ {col}: categorical ({n_unique} unique values)" + (" [TARGET]" if is_target else ""))
                
        except Exception as e:
            print(f"  ⚠ {col}: SKIPPED ({str(e)})")
            continue
    
    if not processed_cols:
        raise ValueError("No valid columns could be processed.")
    
    if len(processed_cols) < 2:
        raise ValueError(f"Only {len(processed_cols)} valid column(s) after processing. Need at least 2.")
    
    # Create new dataframe from processed columns
    df = pd.DataFrame(processed_cols)
    
    # Ensure target (last column) is numeric
    target_col = df.iloc[:, -1]
    if target_col.dtype not in ['int64', 'int32', 'float64', 'float32']:
        print(f"  Converting target column to numeric...")
        df.iloc[:, -1] = pd.to_numeric(target_col, errors='coerce')
    
    # Drop any remaining rows with NaN
    before_dropna = len(df)
    df = df.dropna()
    after_dropna = len(df)
    
    print(f"\n  After processing: {df.shape}")
    print(f"  Dropped {before_dropna - after_dropna} rows with remaining NaN")
    
    if df.shape[0] < 4:
        raise ValueError(f"Not enough valid data. Found {df.shape[0]} rows, need at least 4.")
    
    # Validate all values are numeric and not NaN/Inf
    df_values = df.values.astype(float)
    if np.isnan(df_values).any():
        raise ValueError("NaN values remain after processing")
    if np.isinf(df_values).any():
        raise ValueError("Infinite values in data")
    
    # For classification, ensure target has at least 2 classes
    unique_vals = np.unique(df.iloc[:, -1])
    if len(unique_vals) < 2:
        raise ValueError(f"Target column must have at least 2 unique values, found {len(unique_vals)}")
    
    # Detect and report outliers
    X_features = df.iloc[:, :-1].values.astype(float)
    outlier_indices = detect_outliers_iqr(X_features, threshold=1.5)
    if len(outlier_indices) > 0:
        outlier_ratio = len(outlier_indices) / len(df)
        print(f"\n⚠ Outlier Detection: Found {len(outlier_indices)} outliers ({outlier_ratio*100:.1f}%)")
        if outlier_ratio < 0.2:  # Keep outliers if < 20%
            print(f"  Keeping outliers (ratio < 20%)")
        else:
            print(f"  Consider reviewing/removing outliers")
    
    print(f"✓ Data cleaning successful: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def run_pipeline(df):
    """Enhanced pipeline with comprehensive ML analysis"""
    print("\n" + "="*70)
    print("🚀 ML QUALITY DECISION-SUPPORT SYSTEM - PIPELINE STARTING")
    print("="*70)
    
    try:
        df = clean_dataframe(df)
        print(f"\n✓ Cleaned dataframe shape: {df.shape}")

        if df.shape[1] < 2:
            raise ValueError("Dataset must contain at least one feature and one target column.")

        # Separate features and target
        X = df.iloc[:, :-1].values.astype(float)
        y_raw = df.iloc[:, -1].values
        
        # Ensure target is numeric
        try:
            y = pd.to_numeric(y_raw, errors='coerce').values
            if np.isnan(y).any():
                le_target = LabelEncoder()
                y = le_target.fit_transform(y_raw.astype(str))
        except:
            le_target = LabelEncoder()
            y = le_target.fit_transform(y_raw.astype(str))
        
        print(f"\n📊 Dataset Analysis:")
        print(f"  Features: {X.shape[1]} | Samples: {X.shape[0]}")
        print(f"  Target unique values: {len(np.unique(y))}")
        
        # Detect problem type
        problem_type = detect_problem_type(y)
        print(f"  Problem Type: {problem_type.upper()}")
        
        # Handle imbalanced classification
        if problem_type == "classification":
            unique, counts = np.unique(y, return_counts=True)
            class_distribution = dict(zip(unique, counts))
            print(f"  Class Distribution: {class_distribution}")
            
            imbalance_ratio = max(counts) / min(counts)
            if imbalance_ratio > 3:
                print(f"  ⚠ Imbalanced classes detected (ratio: {imbalance_ratio:.1f}:1)")

        if np.isnan(X).any() or np.isinf(X).any():
            X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        
        if np.isnan(y).any() or np.isinf(y).any():
            raise ValueError("NaN or Inf values in target")
        
        # Scale features
        print(f"\n→ Scaling features...")
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        print(f"✓ Scaled (mean={X.mean():.4f}, std={X.std():.4f})")

        # Determine test size
        n_samples = X.shape[0]
        if n_samples < 10:
            test_size = 0.3
        elif n_samples < 50:
            test_size = 0.25
        else:
            test_size = 0.2
        
        # Configure models based on problem type and dataset size
        if problem_type == "classification":
            if n_samples < 20:
                nn_hidden = (16,)
                nn_early_stop = False
                n_estimators = 50  # FAST: Reduced from 100
            elif n_samples < 100:
                nn_hidden = (32,)
                nn_early_stop = False
                n_estimators = 75  # FAST: Reduced from 100
            else:
                nn_hidden = (64, 32)
                nn_early_stop = True
                n_estimators = 100
            
            models = {
                "Logistic Regression": LogisticRegression(
                    max_iter=1000, solver='lbfgs', random_state=42, class_weight='balanced'  # FAST: max_iter 1000 instead of 2000
                ),
                "Random Forest": RandomForestClassifier(
                    n_estimators=n_estimators, max_depth=10, random_state=42, n_jobs=1, class_weight='balanced'  # FAST: max_depth 10 instead of 15
                ),
                "Gradient Boosting": GradientBoostingClassifier(
                    n_estimators=50, learning_rate=0.1, max_depth=4, random_state=42  # FAST: n_est 50, depth 4
                ),
                "Neural Network": MLPClassifier(
                    hidden_layer_sizes=nn_hidden, max_iter=500, random_state=42,  # FAST: max_iter 500 instead of 1000
                    early_stopping=nn_early_stop, learning_rate_init=0.01,
                    learning_rate='adaptive', solver='adam', tol=1e-3  # FAST: tol 1e-3 for faster convergence
                )
            }
            scoring_metric = 'accuracy'
        else:
            if n_samples < 100:
                n_estimators = 50
            else:
                n_estimators = 100
            
            models = {
                "Linear Regression": LinearRegression(),
                "Ridge Regression": Ridge(alpha=1.0),
                "Random Forest": RandomForestRegressor(
                    n_estimators=n_estimators, max_depth=10, random_state=42, n_jobs=1  # FAST: max_depth 10 instead of 15
                ),
                "Gradient Boosting": GradientBoostingRegressor(
                    n_estimators=50, learning_rate=0.1, max_depth=4, random_state=42  # FAST: n_est 50, depth 4
                ),
                "Neural Network": MLPRegressor(
                    hidden_layer_sizes=(64, 32), max_iter=500, random_state=42,  # FAST: max_iter 500 instead of 1000
                    early_stopping=True, learning_rate_init=0.01, learning_rate='adaptive', solver='adam'  # FAST: faster
                )
            }
            scoring_metric = 'r2'
        
        print(f"\n→ Train/Val Split: {1-test_size:.0%}/{test_size:.0%}")
        print(f"  Training set size: {int(n_samples * (1-test_size))}")
        print(f"  Validation set size: {int(n_samples * test_size)}")

        # Split data
        try:
            if problem_type == "classification":
                X_train, X_val, y_train, y_val = train_test_split(
                    X, y, test_size=test_size, random_state=42, stratify=y
                )
                print("✓ Stratified split successful")
            else:
                X_train, X_val, y_train, y_val = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
                print("✓ Random split successful")
        except ValueError as e:
            print(f"⚠ Stratified split failed, using regular split...")
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=None
            )
            print("✓ Split successful")

        results = []
        successful_models = 0

        print(f"\n{'='*70}")
        print("🔬 MODEL TRAINING & EVALUATION")
        print(f"{'='*70}")

        for name, model in models.items():
            try:
                print(f"\n📍 {name}")
                print(f"  {'─' * 65}")
                
                # Train model
                X_train_clean = np.nan_to_num(X_train, nan=0.0, posinf=0.0, neginf=0.0)
                model.fit(X_train_clean, y_train)
                print(f"  ✓ Model training complete")

                # Calculate train and validation scores
                train_score = model.score(X_train_clean, y_train)
                val_score = model.score(X_val, y_val)

                print(f"  📈 Train Score: {train_score:.4f} ({train_score*100:.2f}%)")
                print(f"  📊 Validation Score: {val_score:.4f} ({val_score*100:.2f}%)")
                
                # Cross-validation with adaptive folds - OPTIMIZED
                adaptive_cv = get_adaptive_cv(len(y_train), y_train, problem_type)
                adaptive_cv = min(2, adaptive_cv)  # FAST: Use max 2 folds for speed
                print(f"  📋 Using {adaptive_cv}-fold cross-validation")
                cv_scores = cross_val_score(model, X_train_clean, y_train, cv=adaptive_cv, scoring=scoring_metric, n_jobs=1)
                cv_info = calculate_cv_confidence_intervals(cv_scores)
                print(f"  🎯 CV Mean: {cv_info['mean']:.4f} ± {cv_info['margin']:.4f}")
                
                # Bias-Variance Analysis
                bv_info = calculate_bias_variance(cv_scores)
                print(f"  ⚖️  Bias: {bv_info['bias']:.4f} | Variance: {bv_info['variance']:.4f}")
                
                # Detect fit status
                fit_status = detect_fit_status(train_score, val_score, problem_type)
                print(f"  🎯 Fit Status: {fit_status}")
                
                # Learning curves (adaptive CV)
                learning_curves = calculate_learning_curves(model, X_train_clean, y_train, problem_type, cv=adaptive_cv)
                
                # ============================================================
                # DETAILED CLASSIFICATION METRICS (NEW - Following Guide)
                # ============================================================
                detailed_metrics = {}
                if problem_type == "classification":
                    try:
                        # Step 1: Get predictions
                        y_pred = model.predict(X_val)
                        
                        # Step 2: Try to get predicted probabilities
                        y_pred_proba = None
                        if hasattr(model, 'predict_proba'):
                            y_pred_proba = model.predict_proba(X_val)
                        elif hasattr(model, 'decision_function'):
                            # For models without predict_proba, use decision function
                            decision = model.decision_function(X_val)
                            # Convert decision scores to probabilities
                            y_pred_proba = np.column_stack([
                                1 / (1 + np.exp(decision)),
                                1 / (1 + np.exp(-decision))
                            ])
                        
                        # Step 3: Calculate metrics using the guide's formulas
                        print(f"  📋 Calculating detailed classification metrics...")
                        
                        # Confusion Matrix
                        cm = confusion_matrix(y_val, y_pred)
                        TP = cm[1, 1] if cm.shape == (2, 2) else np.sum([cm[i, i] for i in range(cm.shape[0])])
                        TN = cm[0, 0] if cm.shape == (2, 2) else 0
                        FP = cm[0, 1] if cm.shape == (2, 2) else np.sum(cm) - np.trace(cm)
                        FN = cm[1, 0] if cm.shape == (2, 2) else 0
                        
                        # Accuracy = (TP + TN) / Total
                        accuracy = accuracy_score(y_val, y_pred)
                        
                        # Precision = TP / (TP + FP)
                        precision = precision_score(y_val, y_pred, average='binary' if len(np.unique(y_val)) == 2 else 'weighted', zero_division=0)
                        
                        # Recall = TP / (TP + FN)
                        recall = recall_score(y_val, y_pred, average='binary' if len(np.unique(y_val)) == 2 else 'weighted', zero_division=0)
                        
                        # F1 = 2 × (Precision × Recall) / (Precision + Recall)
                        f1 = f1_score(y_val, y_pred, average='binary' if len(np.unique(y_val)) == 2 else 'weighted', zero_division=0)
                        
                        # ROC-AUC (only for binary classification with probabilities)
                        roc_auc = None
                        roc_data = None
                        if len(np.unique(y_val)) == 2 and y_pred_proba is not None:
                            try:
                                # ROC-AUC uses probabilities, not predicted class
                                if y_pred_proba.shape[1] == 2:
                                    proba_positive = y_pred_proba[:, 1]
                                else:
                                    proba_positive = y_pred_proba[:, 0]
                                
                                roc_auc = roc_auc_score(y_val, proba_positive)
                                fpr, tpr, thresholds = roc_curve(y_val, proba_positive)
                                
                                roc_data = {
                                    'fpr': fpr.tolist(),
                                    'tpr': tpr.tolist(),
                                    'auc': float(roc_auc)
                                }
                                print(f"    ✓ Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
                                print(f"    ✓ Precision: {precision:.4f}")
                                print(f"    ✓ Recall:    {recall:.4f}")
                                print(f"    ✓ F1 Score:  {f1:.4f}")
                                print(f"    ✓ ROC-AUC:   {roc_auc:.4f}")
                            except Exception as e:
                                print(f"    ⚠ ROC-AUC calculation failed: {str(e)}")
                        else:
                            print(f"    ✓ Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
                            print(f"    ✓ Precision: {precision:.4f}")
                            print(f"    ✓ Recall:    {recall:.4f}")
                            print(f"    ✓ F1 Score:  {f1:.4f}")
                        
                        detailed_metrics = {
                            'accuracy': safe_float(accuracy),
                            'precision': safe_float(precision),
                            'recall': safe_float(recall),
                            'f1_score': safe_float(f1),
                            'roc_auc': safe_float(roc_auc) if roc_auc else None,
                            'confusion_matrix': cm.tolist(),
                            'roc_curve': roc_data,
                            'tp': int(TP) if isinstance(TP, (int, np.integer)) else int(np.sum(TP.flatten() if hasattr(TP, 'flatten') else TP)),
                            'tn': int(TN) if isinstance(TN, (int, np.integer)) else int(np.sum(TN.flatten() if hasattr(TN, 'flatten') else TN)),
                            'fp': int(FP) if isinstance(FP, (int, np.integer)) else int(np.sum(FP.flatten() if hasattr(FP, 'flatten') else FP)),
                            'fn': int(FN) if isinstance(FN, (int, np.integer)) else int(np.sum(FN.flatten() if hasattr(FN, 'flatten') else FN)),
                        }
                    except Exception as e:
                        print(f"    ⚠ Detailed metrics calculation failed: {str(e)}")
                        detailed_metrics = {}
                
                results.append(sanitize_for_json({
                    "model": name,
                    "train_score": safe_float(train_score),
                    "val_score": safe_float(val_score),
                    "cv_mean": safe_float(cv_info['mean']),
                    "cv_std": safe_float(cv_info['std']),
                    "confidence_interval": [safe_float(cv_info['ci_lower']), safe_float(cv_info['ci_upper'])],
                    "bias": safe_float(bv_info['bias']),
                    "variance": safe_float(bv_info['variance']),
                    "fit_status": fit_status,
                    "learning_curves": learning_curves,
                    "gap": safe_float(abs(train_score - val_score)),
                    "detailed_metrics": detailed_metrics
                }))
                
                successful_models += 1

            except Exception as e:
                print(f"  ✗ Training failed: {type(e).__name__}: {str(e)[:100]}")
                results.append({
                    "model": name,
                    "train_score": 0.0,
                    "val_score": 0.0,
                    "cv_mean": 0.0,
                    "confidence_interval": [0.0, 0.0],
                    "bias": 0.0,
                    "variance": 0.0,
                    "fit_status": "Error",
                    "error": str(e)[:200]
                })

        if successful_models == 0:
            raise ValueError(f"All {len(models)} models failed to train")
        
        # Model comparison and ranking
        print(f"\n{'='*70}")
        print("🏆 MODEL COMPARISON & RANKING")
        print(f"{'='*70}\n")
        
        # Sort by generalization score
        for r in results:
            if r["fit_status"] != "Error":
                r["generalization_score"] = r["val_score"] - (0.3 * r["gap"])
        
        sorted_results = sorted(
            [r for r in results if r["fit_status"] != "Error"],
            key=lambda x: x.get("generalization_score", 0),
            reverse=True
        )
        
        for i, r in enumerate(sorted_results, 1):
            print(f"{i}. {r['model']:20} | Val: {r['val_score']:.3f} | Gap: {r['gap']:.3f} | {r['fit_status']}")
        
        print(f"\n{'='*70}")
        print("✓ PIPELINE COMPLETE")
        print(f"{'='*70}\n")
        
        return sanitize_for_json({
            "task_type": problem_type,
            "models": results,
            "summary": {
                "successful_models": successful_models,
                "total_models": len(models),
                "dataset_size": n_samples,
                "features": int(X.shape[1]),
                "unique_targets": int(len(np.unique(y)))
            }
        })
    except Exception as e:
        print(f"\n✗ PIPELINE FAILED: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
