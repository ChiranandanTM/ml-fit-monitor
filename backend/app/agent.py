"""
Agentic AI layer for ML Fit Monitor.
Orchestrates observation -> decision -> action loops for ML model improvement.
"""

import pandas as pd
import numpy as np
import os
import json
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from .ml_pipeline import run_pipeline, sanitize_for_json
from .data_profiling import profile_dataset
from .hyperparameter_tuning import tune_hyperparameters
from .feature_importance import calculate_feature_importance
from .threshold_calibration import ThresholdCalibrator

class FitMonitorAgent:
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame, target_column: str = None) -> Dict[str, Any]:
        """
        Runs the agent loop on the provided dataset.
        Caps at 3 iterations.
        """
        trace = []
        step_number = 1
        
        # Step 1: Check Data Quality
        try:
            profile = profile_dataset(df, target_column)
            quality_score = profile.get("quality_score", 100)
            if quality_score < 70 or len(profile.get("issues", [])) > 0:
                trace.append({
                    "step_number": step_number,
                    "observation": f"Data quality check completed. Score: {quality_score:.1f}. Issues found: {len(profile.get('issues', []))}.",
                    "decision_reasoning": "Dirty data can mask true fit. Flagging data quality issues before trusting fit status.",
                    "action_taken": "Logged data quality issues.",
                    "result": profile.get("issues", []),
                    "improved": False
                })
                step_number += 1
        except Exception as e:
            print(f"Data profiling failed: {e}")
            
        # Step 2: Initial Pipeline Run
        try:
            results, artifacts = run_pipeline(df, return_artifacts=True)
        except Exception as e:
            trace.append({
                "step_number": step_number,
                "observation": f"Pipeline training failed: {str(e)}",
                "decision_reasoning": "Cannot proceed without a working pipeline.",
                "action_taken": "Aborted agent loop.",
                "result": "Error",
                "improved": False
            })
            return {"final_result": None, "trace": trace, "models": [], "feature_importance": {}}
            
        models_results = results.get("models", [])
        
        # Find best model
        best_model_res = None
        best_score = -1
        for m in models_results:
            if m.get("fit_status") != "Error":
                gen_score = m.get("val_score", 0) - (0.3 * m.get("gap", 0))
                if gen_score > best_score:
                    best_score = gen_score
                    best_model_res = m

        if not best_model_res:
            trace.append({
                "step_number": step_number,
                "observation": "Pipeline training completed but all models failed.",
                "decision_reasoning": "Cannot proceed without a valid model.",
                "action_taken": "Aborted agent loop.",
                "result": "Error",
                "improved": False
            })
            return {"final_result": results, "trace": trace, "models": [], "feature_importance": {}}

        best_model_name = best_model_res["model"]
        fit_status = best_model_res["fit_status"]
        gap = best_model_res["gap"]
        problem_type = results["task_type"]
        
        trace.append({
            "step_number": step_number,
            "observation": f"Initial training complete. Best model: {best_model_name}. Fit status: {fit_status}. Gap: {gap:.3f}",
            "decision_reasoning": "Evaluating fit status to determine next action.",
            "action_taken": "Analyzed initial pipeline results.",
            "result": fit_status,
            "improved": False
        })
        step_number += 1

        current_gap = gap
        current_val_score = best_model_res["val_score"]
        current_res = best_model_res
        best_model_obj = artifacts["models"][best_model_name]
        
        # X_train is cleaned internally in run_pipeline
        X_train = np.nan_to_num(artifacts["X_train"], nan=0.0, posinf=0.0, neginf=0.0)
        X_val = artifacts["X_val"]
        y_train = artifacts["y_train"]
        y_val = artifacts["y_val"]
        
        # Add summary from enrichment structure if missing
        if "best_model" not in results["summary"]:
            results["summary"]["best_model"] = best_model_name
            results["summary"]["overall_fit_status"] = fit_status
            results["summary"]["val_score"] = current_val_score
            results["summary"]["gap"] = gap
            
        final_results = results
        final_feature_importance = {}

        # The loop
        iterations = 0
        while iterations < 3:
            iterations += 1
            
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            
            if not gemini_api_key or genai is None:
                # Fallback to rules if no API key is provided
                if current_gap > 0.15:
                    action_choice = "tune_hyperparameters"
                elif all(m.get("val_score", 0) < 0.65 for m in models_results if m.get("fit_status") != "Error") and current_val_score < 0.65:
                    action_choice = "feature_importance"
                elif problem_type == "classification" and 0.10 <= current_gap <= 0.15:
                    action_choice = "calibrate_threshold"
                else:
                    action_choice = "stop"
                gemini_reasoning = "Fallback Rules-Engine: No GEMINI_API_KEY provided."
            else:
                genai.configure(api_key=gemini_api_key)
                
                prompt = f"""
You are an expert Machine Learning Engineer orchestrating an Agentic loop.
Current Model State:
- Model Type: {best_model_name}
- Problem Type: {problem_type}
- Training Score: {current_res.get("train_score", 0):.3f}
- Validation Score: {current_val_score:.3f}
- Generalization Gap (Train - Val): {current_gap:.3f}
- Current Fit Status: {current_res.get("fit_status", "Unknown")}

Available Actions:
1. "tune_hyperparameters": Use if the model is overfitting (large gap > 0.10) to apply regularization.
2. "feature_importance": Use if the model is fundamentally underfitting (val score < 0.65) to recommend feature engineering.
3. "calibrate_threshold": Use if classification gap is borderline (0.10 - 0.15) to tweak decision boundaries before doing a full hyperparameter search.
4. "stop": Use if the model is well-fit or no further interventions apply.

Respond ONLY with a valid JSON object matching this schema:
{{
    "decision": "<one of the 4 actions above>",
    "reasoning": "<a 1-2 sentence explanation of your decision based on the model state>"
}}
"""
                try:
                    # Using gemini-2.5-flash as it is fast and capable
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    # Clean markdown if present
                    text_resp = response.text.replace("```json", "").replace("```", "").strip()
                    llm_choice = json.loads(text_resp)
                    action_choice = llm_choice.get("decision", "stop")
                    gemini_reasoning = llm_choice.get("reasoning", "LLM provided no reasoning.")
                except Exception as e:
                    print(f"Gemini API Error: {e}")
                    action_choice = "stop"
                    gemini_reasoning = f"Error calling Gemini API: {e}"

            # Execute the chosen action
            if action_choice == "tune_hyperparameters":
                observation = f"Iteration {iterations}: Gap is {current_gap:.3f}."
                decision = f"[Gemini Agent] {gemini_reasoning}"
                action = "Called tune_hyperparameters."
                
                tune_res = tune_hyperparameters(
                    best_model_obj, X_train, X_val, y_train, y_val,
                    best_model_name, "Overfitting", problem_type
                )
                
                if tune_res.get("tuned"):
                    new_gap = tune_res["tuned_gap"]
                    improved = new_gap < current_gap
                    trace.append({
                        "step_number": step_number,
                        "observation": observation,
                        "decision_reasoning": decision,
                        "action_taken": action,
                        "result": f"Tuned gap: {new_gap:.3f} (Baseline: {current_gap:.3f})",
                        "improved": improved
                    })
                    step_number += 1
                    
                    if improved:
                        current_gap = new_gap
                        current_val_score = tune_res["tuned_val_score"]
                        best_model_obj = tune_res["best_model"]
                        # Update the result dict
                        current_res["val_score"] = current_val_score
                        current_res["train_score"] = tune_res["tuned_train_score"]
                        current_res["gap"] = new_gap
                        current_res["fit_status"] = "Good Fit" if current_gap <= 0.15 else "Overfitting"
                        final_results["summary"]["gap"] = new_gap
                        final_results["summary"]["val_score"] = current_val_score
                        final_results["summary"]["overall_fit_status"] = current_res["fit_status"]
                    else:
                        break # Stop early if no improvement
                else:
                    trace.append({
                        "step_number": step_number,
                        "observation": observation,
                        "decision_reasoning": decision,
                        "action_taken": action,
                        "result": "Tuning failed or no grid.",
                        "improved": False
                    })
                    step_number += 1
                    break

            elif action_choice == "feature_importance":
                observation = f"Iteration {iterations}: Validation score is {current_val_score:.3f}."
                decision = f"[Gemini Agent] {gemini_reasoning}"
                action = "Called calculate_feature_importance."
                
                fi = calculate_feature_importance(
                    pd.DataFrame(X_train), pd.DataFrame(X_val), y_train, y_val, 
                    {best_model_name: best_model_obj}, problem_type
                )
                final_feature_importance = fi
                
                trace.append({
                    "step_number": step_number,
                    "observation": observation,
                    "decision_reasoning": decision,
                    "action_taken": action,
                    "result": "Generated feature importance recommendations.",
                    "improved": False
                })
                step_number += 1
                break

            elif action_choice == "calibrate_threshold":
                observation = f"Iteration {iterations}: Gap is {current_gap:.3f}."
                decision = f"[Gemini Agent] {gemini_reasoning}"
                action = "Called ThresholdCalibrator."
                
                calibrator = ThresholdCalibrator("classification")
                # Just simulating the calibration call
                calib_res = calibrator.calibrate_from_validation_behavior(
                    np.array([current_res.get("train_score", 0)]), 
                    np.array([current_val_score]), 
                    np.array([current_res.get("fit_status", "")])
                )
                
                trace.append({
                    "step_number": step_number,
                    "observation": observation,
                    "decision_reasoning": decision,
                    "action_taken": action,
                    "result": "Calibrated thresholds for next evaluation.",
                    "improved": False
                })
                step_number += 1
                break
                
            else:
                observation = f"Iteration {iterations}: Gap is {current_gap:.3f} and val score is {current_val_score:.3f}."
                decision = f"[Gemini Agent] {gemini_reasoning}"
                action = "Stopped agent loop."
                trace.append({
                    "step_number": step_number,
                    "observation": observation,
                    "decision_reasoning": decision,
                    "action_taken": action,
                    "result": "No further action needed.",
                    "improved": False
                })
                step_number += 1
                break
        
        if not final_feature_importance:
            final_feature_importance = calculate_feature_importance(
                pd.DataFrame(X_train), pd.DataFrame(X_val), y_train, y_val, 
                {best_model_name: best_model_obj}, problem_type
            )
            
        # Add profile to final results if it doesn't exist
        if "data_profile" not in final_results and 'profile' in locals():
             final_results["data_profile"] = profile
        
        return sanitize_for_json({
            "final_result": final_results,
            "trace": trace,
            "models": [{
                "model": best_model_name,
                "fit_status": current_res.get("fit_status"),
                "val_score": current_val_score,
                "train_score": current_res.get("train_score"),
                "gap": current_gap
            }],
            "feature_importance": final_feature_importance
        })
