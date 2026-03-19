# ML Fit Monitor - System Overview

## 1. Purpose
ML Fit Monitor is a model-quality decision support system that analyzes uploaded datasets and reports whether model behavior is:
- Good Fit
- Overfitting
- Underfitting

It also provides suggestions and can attempt automatic dataset transformation to improve fit quality.

## 2. High-Level Architecture
The project uses a two-tier architecture:

- Frontend: React + TypeScript + Vite
  - Upload UI (CSV/Excel)
  - Analysis mode selection
  - Charts, fit cards, suggestion panels
  - Best-model improvement action

- Backend: FastAPI + scikit-learn
  - Dataset ingestion and cleaning
  - Multi-model training and evaluation
  - Fit status detection logic
  - Suggestions and drift simulation
  - Automatic improvement endpoint

## 3. Core Workflow
1. User uploads dataset file (`.csv`, `.xlsx`, `.xls`).
2. Backend parses file and validates shape/content.
3. Data is cleaned and preprocessed.
4. Multiple models are trained and evaluated.
5. Fit status is detected per model from train/validation behavior.
6. Best model is selected using a generalization-oriented score.
7. Frontend displays status, metrics, and recommendations.
8. User can run best-model-driven improvement and download improved dataset.

## 4. Backend Modules
- `backend/app/main.py`
  - FastAPI app and all routes
  - File parsing helper (`read_uploaded_dataframe`)
  - Best model selection (`get_best_model`)
  - Summary enrichment (`enrich_results_summary`)
  - Improvement strategy (`improve_dataset_for_fit`)

- `backend/app/ml_pipeline.py`
  - Data cleaning, feature prep, scaling, split
  - Model training and evaluation
  - CV metrics, learning curves, bias/variance helpers

- `backend/app/fit_detector.py`
  - Rule-based fit classification
  - Fit explanation generation

- `backend/app/drift.py`
  - Drift simulation and retraining triggers

## 5. Primary API Endpoints
- `GET /`
  - Health/info message

- `POST /train`
  - Train and evaluate models
  - Returns model metrics + summary + best model + overall fit status

- `POST /suggest`
  - Returns per-model suggestions
  - Returns best model block with targeted suggestions

- `POST /analyze`
  - Comprehensive analysis with executive summary and drift details

- `POST /drift-simulate`
  - Drift stress testing report

- `POST /improve-fit?strategy=best_model|generic`
  - Applies improvement pipeline
  - Returns original vs improved status, improved results, and downloadable CSV content

- `GET /generate-dataset/{fit_type}`
  - Generates sample datasets (`good_fit`, `overfitting`, `underfitting`)

## 6. Fit Detection Logic (Conceptual)
For each model:
- Compute train score and validation score.
- Compute generalization gap = `abs(train - val)`.
- Classify as:
  - Good Fit: high train + high validation + small gap
  - Overfitting: high train + significantly lower validation
  - Underfitting: low train and/or low validation

Best model selection is based on a generalization-aware ranking score used in backend summary generation.

## 7. Improvement System
When user triggers improvement:
1. Run baseline pipeline and identify overall status and best model.
2. Choose transformation strategy:
   - `best_model` (default): applies model-aware heuristics
   - `generic`: fallback/general heuristics
3. For overfitting: reduce complexity, feature selection, optional rebalance, optional outlier removal.
4. For underfitting: increase feature expressiveness via polynomial interactions.
5. Re-run pipeline on transformed dataset.
6. Return improved outputs and downloadable improved CSV.

## 8. Frontend Behavior
- Upload panel supports CSV and Excel.
- Modes:
  - Basic Training
  - Full Analysis
  - Suggestions
  - Drift Simulation
- Suggestions mode shows:
  - Best model recommendation block
  - "Improve File Using Best Model Suggestions" action when not Good Fit
- Improvement result view shows:
  - Original vs improved status
  - Improved model outputs
  - Download button for improved dataset

## 9. Key Dependencies
Backend:
- `fastapi`
- `uvicorn`
- `pandas`
- `numpy`
- `scikit-learn`
- `scipy`
- `python-multipart`
- `openpyxl`
- `xlrd`

Frontend:
- `react`
- `typescript`
- `vite`
- `axios`
- `recharts`
- `zustand`

## 10. Run Notes
Backend:
1. Activate Python environment
2. `pip install -r backend/requirements.txt`
3. `cd backend`
4. `uvicorn app.main:app --reload --port 8000`

Frontend:
1. `cd frontend`
2. `npm install`
3. `npm run dev`

App URLs:
- Frontend: `http://localhost:5173` (or Vite-assigned port)
- Backend docs: `http://localhost:8000/docs`

## 11. Current Constraints
- Improvement is heuristic and best-effort; Good Fit is not guaranteed for all datasets.
- Rule thresholds are static and may need calibration for domain-specific data.
- Very small datasets can cause unstable fit labels due to split variance.

## 12. Recommended Next Enhancements
- Add model-specific hyperparameter tuning in improvement loop.
- Add before/after metric delta table for best model in UI.
- Add persisted experiment history and comparison.
- Add automated threshold calibration from validation behavior.
