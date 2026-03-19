from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from io import StringIO, BytesIO
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
from sklearn.preprocessing import PolynomialFeatures
from .ml_pipeline import (
    run_pipeline,
    sanitize_for_json,
    clean_dataframe,
    detect_problem_type,
    detect_outliers_iqr,
)
from .drift import simulate_drift, generate_drift_report, analyze_drift_trend
from .fit_detector import generate_fit_explanation
import traceback

app = FastAPI(title="🚀 ML Model Quality Decision-Support System API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ML Fit Monitor Backend Running"}


def read_uploaded_dataframe(file: UploadFile, content: bytes) -> pd.DataFrame:
    """Read CSV/Excel uploads into a dataframe."""
    filename = (file.filename or "").lower()

    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(BytesIO(content))

    # Default to CSV parsing for backward compatibility.
    try:
        return pd.read_csv(StringIO(content.decode("utf-8")))
    except UnicodeDecodeError:
        return pd.read_csv(StringIO(content.decode("latin-1")))


def get_best_model(models):
    """Return best non-error model based on generalization score."""
    valid = [m for m in models if m.get("fit_status") != "Error"]
    if not valid:
        return None

    return max(valid, key=lambda m: m.get("val_score", 0) - (0.3 * m.get("gap", 0)))


def enrich_results_summary(results):
    """Attach best model and overall status to pipeline summary."""
    models = results.get("models", [])
    summary = results.get("summary", {})
    best = get_best_model(models)

    if best:
        summary["best_model"] = best.get("model")
        summary["overall_fit_status"] = best.get("fit_status")
    else:
        summary["best_model"] = None
        summary["overall_fit_status"] = "Error"

    results["summary"] = summary
    return results


def improve_dataset_for_fit(
    df: pd.DataFrame,
    original_status: str,
    best_model_name: str | None = None,
    strategy: str = "best_model"
) -> pd.DataFrame:
    """Heuristic dataset transformation to improve generalization.

    strategy="best_model" applies transformations guided by the selected best model.
    """
    cleaned = clean_dataframe(df.copy())
    X = cleaned.iloc[:, :-1].values.astype(float)
    y = cleaned.iloc[:, -1].values
    problem_type = detect_problem_type(y)
    model_name = (best_model_name or "").lower()

    # Overfitting fix: reduce complexity, remove outliers, rebalance classes.
    if original_status == "Overfitting":
        outlier_indices = detect_outliers_iqr(X, threshold=1.5)
        if 0 < len(outlier_indices) < len(cleaned) * 0.35:
            keep_mask = np.ones(len(cleaned), dtype=bool)
            keep_mask[outlier_indices] = False
            cleaned = cleaned[keep_mask].reset_index(drop=True)
            X = cleaned.iloc[:, :-1].values.astype(float)
            y = cleaned.iloc[:, -1].values

        if X.shape[1] > 6:
            # Best-model-specific complexity control.
            if strategy == "best_model" and "logistic" in model_name:
                k = max(3, min(8, X.shape[1] // 3))
            elif strategy == "best_model" and ("random forest" in model_name or "gradient" in model_name):
                k = max(4, min(10, X.shape[1] // 2))
            elif strategy == "best_model" and "neural" in model_name:
                k = max(4, min(12, (X.shape[1] * 2) // 3))
            else:
                k = max(4, min(10, X.shape[1] // 2))
            score_fn = f_classif if problem_type == "classification" else f_regression
            selector = SelectKBest(score_func=score_fn, k=k)
            X = selector.fit_transform(X, y)

        if problem_type == "classification":
            temp = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(X.shape[1])])
            temp["target"] = y
            class_counts = temp["target"].value_counts()
            if len(class_counts) > 1:
                max_count = class_counts.max()
                balanced_parts = []
                for label, group in temp.groupby("target"):
                    replace = len(group) < max_count
                    sampled = group.sample(n=max_count, replace=replace, random_state=42)
                    balanced_parts.append(sampled)
                temp = pd.concat(balanced_parts, ignore_index=True)
            cleaned = temp
        else:
            cleaned = pd.DataFrame(X, columns=[f"feature_{i+1}" for i in range(X.shape[1])])
            cleaned["target"] = y

        return cleaned

    # Underfitting fix: richer feature interactions.
    if original_status == "Underfitting":
        degree = 2
        if strategy == "best_model" and ("logistic" in model_name or "linear" in model_name):
            degree = 3
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        X_poly = poly.fit_transform(X)
        max_features = 40
        if X_poly.shape[1] > max_features:
            X_poly = X_poly[:, :max_features]

        improved = pd.DataFrame(X_poly, columns=[f"feature_{i+1}" for i in range(X_poly.shape[1])])
        improved["target"] = y
        return improved

    return cleaned

@app.post("/train")
async def train_model(file: UploadFile = File(...)):
    try:
        print("\n" + "="*50)
        print("DATA RECEIVED - Starting Processing")
        print("="*50)
        
        content = await file.read()
        print(f"✓ File size: {len(content)} bytes")
        print(f"✓ Filename: {file.filename}")

        df = read_uploaded_dataframe(file, content)

        print(f"✓ File parsed successfully")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {df.columns.tolist()}")
        print(f"  First few rows:\n{df.head()}")

        if df.shape[1] < 2:
            error_msg = "Dataset must contain at least 1 feature and 1 target column."
            print(f"✗ {error_msg}")
            return {"error": error_msg}

        if df.shape[0] < 4:
            error_msg = f"Dataset needs at least 4 rows, found {df.shape[0]}"
            print(f"✗ {error_msg}")
            return {"error": error_msg}

        print(f"\n✓ Pre-validation passed, running pipeline...")
        results = run_pipeline(df)
        results = enrich_results_summary(results)
        
        print("="*50)
        print("✓ SUCCESS - Processing Complete")
        print("="*50)
        return sanitize_for_json(results)

    except UnicodeDecodeError as e:
        error_msg = f"File encoding error: {str(e)}. Please ensure file is valid CSV/Excel format."
        print(f"✗ DECODE ERROR: {error_msg}")
        return {"error": error_msg}
    
    except pd.errors.ParserError as e:
        error_msg = f"CSV parsing error: {str(e)}. Please check CSV format."
        print(f"✗ PARSER ERROR: {error_msg}")
        return {"error": error_msg}
    
    except ValueError as e:
        error_msg = f"Value Error: {str(e)}"
        print(f"✗ VALUE ERROR: {error_msg}")
        return {"error": error_msg}
    
    except Exception as e:
        print("✗ UNEXPECTED ERROR OCCURRED")
        traceback.print_exc()
        error_msg = f"Server error: {str(e)}"
        return {"error": error_msg}


@app.get("/generate-dataset/{fit_type}")
def generate_dataset(fit_type: str):
    """Generate sample datasets for Good Fit, Overfitting, or Underfitting"""
    import numpy as np
    
    np.random.seed(42)
    
    if fit_type == "good_fit":
        # Good Fit: Well-balanced, learnable pattern, generalizes well
        # Train and validation scores both high (~0.80-0.85) with small gap (~0.05)
        X = np.random.randn(100, 4)
        w = np.array([2, -1.5, 1, -0.5])
        y = (X @ w > 0).astype(int)
        y = np.where(np.random.rand(100) < 0.05, 1 - y, y)  # Add 5% noise
        df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3', 'feature_4'])
        df['target'] = y
        
    elif fit_type == "overfitting":
        # Overfitting: Complex model trained on limited data with noise
        # High training score (~0.90+) but much lower validation (~0.60-0.65)
        X = np.random.randn(25, 10)
        y = np.random.randint(0, 2, 25)
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(1, 11)])
        df['target'] = y
        
    elif fit_type == "underfitting":
        # Underfitting: Simple features, complex target relationship
        # Both training and validation low (~0.55-0.65)
        X = np.random.randn(50, 2)
        y_true = (X[:, 0]**2 + X[:, 1]**2 > 1).astype(int)
        y = np.where(np.random.rand(50) < 0.3, 1 - y_true, y_true)  # Add 30% noise
        df = pd.DataFrame(X, columns=['feature_1', 'feature_2'])
        df['target'] = y
        
    else:
        return {"error": f"Unknown fit_type: {fit_type}. Use 'good_fit', 'overfitting', or 'underfitting'"}
    
    # Convert to CSV string
    csv_string = df.to_csv(index=False)
    return {
        "csv": csv_string,
        "filename": f"{fit_type}_dataset.csv",
        "rows": len(df),
        "columns": df.shape[1],
        "description": f"Sample {fit_type.replace('_', ' ')} dataset"
    }


def generate_suggestions(fit_status, model_results, task_type):
    """
    Module 4: Suggestion Engine
    Generate actionable recommendations based on detected fit status.
    """
    
    suggestions = {
        "Good Fit": [],
        "Overfitting": [
            {
                "priority": "HIGH",
                "action": "1. Increase Regularization",
                "details": "Apply L1/L2 penalties to model weights",
                "impl_effort": "Easy",
                "expected_impact": "±5-10% performance improvement"
            },
            {
                "priority": "HIGH",
                "action": "2. Feature Selection/Reduction",
                "details": "Remove non-informative features to reduce model complexity",
                "impl_effort": "Medium",
                "expected_impact": "±5-15% performance improvement"
            },
            {
                "priority": "MEDIUM",
                "action": "3. Collect More Data",
                "details": "Increase training set size (target: 2-3x current)",
                "impl_effort": "Hard",
                "expected_impact": "±10-20% performance improvement"
            },
            {
                "priority": "MEDIUM",
                "action": "4. Use Ensemble Methods",
                "details": "Apply bagging, boosting, or stacking for better generalization",
                "impl_effort": "Medium",
                "expected_impact": "±5-10% performance improvement"
            },
            {
                "priority": "MEDIUM",
                "action": "5. Apply Dropout/Early Stopping",
                "details": "Use regularization techniques for neural networks",
                "impl_effort": "Easy",
                "expected_impact": "±3-8% performance improvement"
            },
            {
                "priority": "LOW",
                "action": "6. Cross-Validation Tuning",
                "details": "Use k-fold CV with hyperparameter grid search",
                "impl_effort": "Hard",
                "expected_impact": "±2-5% performance improvement"
            }
        ],
        "Underfitting": [
            {
                "priority": "HIGH",
                "action": "1. Increase Model Complexity",
                "details": "Use deeper neural networks, more trees, or higher-degree polynomials",
                "impl_effort": "Easy",
                "expected_impact": "±10-20% performance improvement"
            },
            {
                "priority": "HIGH",
                "action": "2. Feature Engineering",
                "details": "Add polynomial features, interactions, or domain-specific features",
                "impl_effort": "Medium",
                "expected_impact": "±5-15% performance improvement"
            },
            {
                "priority": "HIGH",
                "action": "3. Collect More Data",
                "details": "Increase training set size (target: 2x current)",
                "impl_effort": "Hard",
                "expected_impact": "±5-15% performance improvement"
            },
            {
                "priority": "MEDIUM",
                "action": "4. Reduce Regularization",
                "details": "Lower L1/L2 penalties to allow model to learn more patterns",
                "impl_effort": "Easy",
                "expected_impact": "±3-8% performance improvement"
            },
            {
                "priority": "MEDIUM",
                "action": "5. Try Different Algorithms",
                "details": "Switch to more powerful models (Random Forest, Neural Networks, Boosting)",
                "impl_effort": "Medium",
                "expected_impact": "±5-15% performance improvement"
            },
            {
                "priority": "LOW",
                "action": "6. Data Quality Assessment",
                "details": "Check for noisy labels, outliers, or data quality issues",
                "impl_effort": "Medium",
                "expected_impact": "±2-8% performance improvement"
            }
        ]
    }
    
    # Get relevant suggestions for detected status
    if fit_status == "Good Fit":
        suggestions[fit_status] = [
            {
                "priority": "INFO",
                "action": "✅ Model is performing well!",
                "details": "No immediate improvements needed",
                "recommendations": [
                    "Consider deploying to production",
                    "Set up continuous monitoring for data drift",
                    "Plan periodic retraining (monthly/quarterly)",
                    "Document model performance baselines"
                ]
            }
        ]
    
    return suggestions.get(fit_status, suggestions["Underfitting"])


@app.post("/suggest")
async def get_suggestions(file: UploadFile = File(...)):
    """
    Module 4: Suggestion Engine Endpoint
    Analyzes dataset and returns actionable improvement suggestions.
    """
    try:
        content = await file.read()
        df = read_uploaded_dataframe(file, content)
        
        # Run pipeline
        results = run_pipeline(df)
        results = enrich_results_summary(results)
        
        # Generate suggestions for each model
        suggestions_list = []
        for model in results.get("models", []):
            if model.get("fit_status") != "Error":
                suggestions = generate_suggestions(
                    model["fit_status"],
                    results["models"],
                    results["task_type"]
                )
                suggestions_list.append({
                    "model": model["model"],
                    "fit_status": model["fit_status"],
                    "suggestions": suggestions,
                    "gap": model.get("gap", 0),
                    "confidence_interval": model.get("confidence_interval")
                })

        best_model = get_best_model(results.get("models", []))
        best_model_suggestions = []
        if best_model:
            best_model_suggestions = generate_suggestions(
                best_model.get("fit_status", "Underfitting"),
                results.get("models", []),
                results.get("task_type", "classification")
            )
        
        return sanitize_for_json({
            "dataset_info": {
                "rows": df.shape[0],
                "columns": df.shape[1] - 1,  # Excluding target
                "problem_type": results["task_type"]
            },
            "best_model": {
                "model": best_model.get("model") if best_model else None,
                "fit_status": best_model.get("fit_status") if best_model else "Error",
                "val_score": best_model.get("val_score", 0) if best_model else 0,
                "gap": best_model.get("gap", 0) if best_model else 0,
                "suggestions": best_model_suggestions,
            },
            "model_suggestions": suggestions_list,
            "general_recommendations": [
                "Start with highest priority suggestions",
                "Implement one change at a time to measure impact",
                "Use cross-validation to validate improvements",
                "Monitor retraining intervals and performance drift"
            ]
        })
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze")
async def comprehensive_analysis(file: UploadFile = File(...)):
    """
    Comprehensive ML Model Quality Analysis.
    Returns detailed analysis with learning curves, bias-variance, suggestions, and drift simulation.
    """
    try:
        content = await file.read()
        df = read_uploaded_dataframe(file, content)
        
        print("\n" + "="*80)
        print("🔬 COMPREHENSIVE ANALYSIS - Complete ML Model Quality Report")
        print("="*80)
        
        # Run full pipeline
        results = run_pipeline(df)
        results = enrich_results_summary(results)
        
        # Run drift simulation
        results_with_drift = simulate_drift(results, drift_severity=0.2)
        
        # Generate extended analysis
        analysis_report = {
            "executive_summary": {
                "dataset": f"{df.shape[0]} samples, {df.shape[1]-1} features",
                "problem_type": results["task_type"].upper(),
                "models_trained": results["summary"]["successful_models"],
                "best_performing": None,
                "overall_recommendation": ""
            },
            "model_analysis": [],
            "suggestions": [],
            "drift_analysis": {
                "simulated_severities": [5, 10, 15, 20, 30, 50],
                "models_detailed": []
            },
            "next_steps": []
        }
        
        # Find best model
        best_model = None
        best_score = -1
        for model in results_with_drift.get("models", []):
            if model.get("fit_status") != "Error":
                gen_score = model.get("val_score", 0) - (0.3 * model.get("gap", 0))
                if gen_score > best_score:
                    best_score = gen_score
                    best_model = model
        
        if best_model:
            analysis_report["executive_summary"]["best_performing"] = best_model["model"]
        
        # Detailed model analysis
        for model in results_with_drift.get("models", []):
            if model.get("fit_status") != "Error":
                fit_explanation = generate_fit_explanation(
                    model["fit_status"],
                    model["train_score"],
                    model["val_score"],
                    model.get("bias", 0),
                    model.get("variance", 0)
                )
                
                model_analysis = {
                    "model_name": model["model"],
                    "performance": {
                        "train_score": f"{model['train_score']:.1%}",
                        "val_score": f"{model['val_score']:.1%}",
                        "gap": f"{model.get('gap', 0):.1%}",
                        "cv_confidence": (
                            f"{model.get('cv_mean', 0):.1%} ± {model.get('cv_std', 0):.1%}"
                        )
                    },
                    "fit_diagnosis": {
                        "status": model["fit_status"],
                        "summary": fit_explanation["summary"],
                        "signal": fit_explanation["bias_variance_signal"],
                        "severity": fit_explanation["severity"],
                        "next_steps": fit_explanation["next_steps"]
                    },
                    "learning_curves": model.get("learning_curves"),
                    "drift_impact": model.get("drift_simulation", {})
                }
                analysis_report["model_analysis"].append(model_analysis)
                
                # Drift report
                if model.get("drift_simulation"):
                    drift_report = generate_drift_report(model)
                    analysis_report["drift_analysis"]["models_detailed"].append(drift_report)
        
        # Generate suggestions
        for model in results_with_drift["models"]:
            if model.get("fit_status") != "Error":
                suggestions = generate_suggestions(
                    model["fit_status"],
                    results["models"],
                    results["task_type"]
                )
                analysis_report["suggestions"].append({
                    "model": model["model"],
                    "status": model["fit_status"],
                    "recommendations": suggestions[:3]  # Top 3 suggestions
                })
        
        # Overall recommendation
        if best_model and best_model["fit_status"] == "Good Fit":
            analysis_report["executive_summary"]["overall_recommendation"] = (
                f"✅ Models show good generalization. {best_model['model']} is recommended "
                f"for deployment. Implement standard monitoring and quarterly retraining."
            )
            analysis_report["next_steps"] = [
                "Deploy best model with monitoring",
                "Set up data drift detection",
                "Plan retraining schedule"
            ]
        else:
            analysis_report["executive_summary"]["overall_recommendation"] = (
                "⚠️ Models need improvement before production deployment. "
                "Follow suggestions to enhance generalization."
            )
            analysis_report["next_steps"] = [
                "Implement high-priority suggestions",
                "Retrain and validate improvements",
                "Rerun analysis before deployment"
            ]
        
        print("\n✓ Analysis Complete\n")
        return sanitize_for_json(analysis_report)
    
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}


@app.post("/drift-simulate")
async def drift_simulation(file: UploadFile = File(...)):
    """
    Data Drift Simulation Endpoint.
    Simulates distribution shift and provides retraining recommendations.
    """
    try:
        content = await file.read()
        df = read_uploaded_dataframe(file, content)
        
        # Run pipeline first
        results = run_pipeline(df)
        results = enrich_results_summary(results)
        
        # Simulate drift with multiple severity levels
        drifted_results = simulate_drift(results, drift_severity=0.2)
        
        # Extract drift analysis
        drift_report = {
            "simulation_summary": "Synthetic data distribution shift simulation",
            "severity_tested": [0.05, 0.10, 0.15, 0.20, 0.30, 0.50],
            "models": []
        }
        
        for model in drifted_results.get("models", []):
            if model.get("drift_simulation"):
                drift_sim = model["drift_simulation"]
                triggers = drift_sim.get("retraining_triggers", [])
                
                model_drift = {
                    "model_name": model["model"],
                    "original_score": f"{drift_sim.get('original_score', 0):.1%}",
                    "worst_case": f"{min([p['degraded_score'] for p in drift_sim.get('degradation_curve', [])]):.1%}",
                    "critical_threshold": drift_sim.get("severity_at_critical"),
                    "trigger_events": triggers,
                    "monitoring_recommendation": "hourly" if len(triggers) > 2 else "daily",
                    "retraining_urgency": (
                        "IMMEDIATE" if any(t["trigger_level"] == "🔴 CRITICAL" for t in triggers)
                        else "PLANNED" if any(t["trigger_level"] == "🟠 ALERT" for t in triggers)
                        else "SCHEDULED"
                    )
                }
                drift_report["models"].append(model_drift)
        
        return sanitize_for_json(drift_report)
    
    except Exception as e:
        return {"error": str(e)}


@app.post("/improve-fit")
async def improve_fit(file: UploadFile = File(...), strategy: str = "best_model"):
    """
    Attempt to transform underfitting/overfitting datasets toward good fit.
    Returns improved model results and downloadable improved CSV.
    """
    try:
        content = await file.read()
        df = read_uploaded_dataframe(file, content)

        base_results = enrich_results_summary(run_pipeline(df))
        original_status = base_results.get("summary", {}).get("overall_fit_status", "Error")
        best_model = get_best_model(base_results.get("models", []))
        best_model_name = best_model.get("model") if best_model else None

        if strategy not in ["best_model", "generic"]:
            return {"error": "Invalid strategy. Use 'best_model' or 'generic'."}

        if original_status == "Good Fit":
            return sanitize_for_json({
                "message": "Dataset is already in Good Fit state. No improvement needed.",
                "original_overall_status": original_status,
                "improved_overall_status": original_status,
                "improvement_applied": False,
                "improved_results": base_results,
                "improved_file": {
                    "filename": "already_good_fit.csv",
                    "csv": clean_dataframe(df.copy()).to_csv(index=False)
                }
            })

        improved_df = improve_dataset_for_fit(
            df,
            original_status,
            best_model_name=best_model_name,
            strategy=strategy
        )
        improved_results = enrich_results_summary(run_pipeline(improved_df))
        improved_status = improved_results.get("summary", {}).get("overall_fit_status", "Error")

        best_model_suggestions = generate_suggestions(
            original_status,
            base_results.get("models", []),
            base_results.get("task_type", "classification")
        )

        message = (
            f"Improvement pipeline executed using {strategy} strategy on best model "
            f"'{best_model_name or 'N/A'}'. Status changed from {original_status} to {improved_status}."
        )

        return sanitize_for_json({
            "message": message,
            "original_overall_status": original_status,
            "improved_overall_status": improved_status,
            "improvement_applied": True,
            "strategy": strategy,
            "best_model_used": best_model_name,
            "best_model_suggestions_used": best_model_suggestions,
            "original_results": base_results,
            "improved_results": improved_results,
            "improved_file": {
                "filename": "improved_fit_dataset.csv",
                "csv": improved_df.to_csv(index=False)
            }
        })

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


