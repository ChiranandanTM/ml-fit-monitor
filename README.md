# 🚀 ML Fit Monitor - Machine Learning Model Quality Decision-Support System

**ML Fit Monitor** is an advanced, full-stack Machine Learning Model Quality Decision-Support System designed to help data scientists and ML engineers evaluate, analyze, monitor, and improve machine learning models. The system automatically detects model fit status (Good Fit, Overfitting, or Underfitting), provides detailed statistical analysis, generates professional PDF reports, and offers actionable recommendations for model improvement.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)
- [Architecture](#architecture)
- [Development](#development)
- [Contributing](#contributing)

---

## 📖 Overview

### What is ML Fit Monitor?

ML Fit Monitor is a comprehensive solution for machine learning model evaluation and monitoring. It provides:

- **Automatic Model Fit Detection**: Identifies overfitting, underfitting, and good fit scenarios
- **Multi-Model Comparison**: Train and compare multiple algorithms simultaneously
- **Data Quality Analysis**: Profile datasets and identify quality issues
- **Feature Importance**: Understand which features matter most for predictions
- **Hyperparameter Optimization**: Automatically tune model parameters for better performance
- **Experiment Tracking**: Save and compare experiments over time
- **Model Drift Detection**: Monitor how model performance changes with data drift
- **Professional Reports**: Generate detailed PDF reports with charts and recommendations
- **Interactive Dashboard**: Visualize all analysis results in real-time

### Who Should Use It?

- **Data Scientists**: Quickly validate model quality and detect fitting issues
- **ML Engineers**: Monitor model performance in production
- **Data Analysts**: Understand data quality and feature importance
- **Researchers**: Track and compare experiments systematically
- **Business Stakeholders**: Get actionable insights through professional reports

---

## 🎯 Key Features

### 1. **Model Fit Detection**
Automatically analyzes training vs validation performance to classify models as:
- **Good Fit**: Balanced performance, optimal generalization
- **Overfitting**: High training accuracy, lower validation accuracy (model memorizes data)
- **Underfitting**: Poor performance on both sets (model too simple)

Uses statistical confidence intervals for accurate classification.

### 2. **Multi-Model Comparison**
Train and compare multiple algorithms simultaneously:
- Logistic Regression & Linear Regression
- Ridge Regression
- Random Forest (Classification & Regression)
- Gradient Boosting (Classification & Regression)
- Neural Networks (MLP Classifier & Regressor)
- View detailed metrics for each model side-by-side

### 3. **Data Profiling & Quality Analysis**
- Automatic dataset profiling and statistics
- Data quality checks and improvement recommendations
- Outlier detection using Interquartile Range (IQR)
- Missing value analysis
- Feature distribution analysis
- Data type detection and validation

### 4. **Feature Importance Analysis**
- Identify which features contribute most to predictions
- SelectKBest algorithm for feature ranking
- Feature selection recommendations
- Visual importance rankings and charts
- Actionable insights for feature engineering

### 5. **Hyperparameter Tuning**
- Automated hyperparameter optimization
- Grid search for optimal parameter combinations
- Before/after performance comparison
- Tuning history and trend tracking
- Model improvement suggestions

### 6. **Experiment History & Tracking**
- Save all experiments with metadata
- Compare multiple experiments side-by-side
- Track experiment trends over time
- Retrieve detailed results from past runs
- Experiment versioning and management

### 7. **Model Drift Detection**
- Simulate and detect data drift
- Analyze drift impact on model performance
- Generate drift analysis reports
- Monitor model stability over time
- Early warning for performance degradation

### 8. **Classification & Regression Analysis**
- **Classification**: ROC Curves, AUC, Confusion Matrices, Precision/Recall/F1-Score
- **Regression**: MSE, RMSE, MAE, R² Score, MAPE
- Learning curves to visualize fitting trends
- Optimal threshold finding for binary classification
- Comprehensive metric calculations

### 9. **Threshold Calibration**
- Adaptive threshold calibration for classification
- Optimize decision boundaries for business requirements
- Generate adaptive fit detectors
- Improve class balance and prediction metrics

### 10. **PDF Report Generation**
Generate professional PDF reports including:
- Executive Summary with key findings
- Model Performance metrics and comparisons
- Feature Importance charts
- Confusion matrices (classification)
- Learning curves
- Data profiling insights
- Actionable recommendations for improvement

### 11. **Interactive Dashboard**
- Real-time visualization with Recharts
- Responsive design for all devices
- Data upload panel for easy integration
- Comprehensive suggestion panel
- Feature importance visualization
- Model comparison charts
- Experiment history tracking

---

## 💻 Tech Stack

### **Frontend**
| Technology | Version | Purpose |
|---|---|---|
| React | 19.2.0 | UI Framework |
| TypeScript | 5.9.3 | Type-safe JavaScript |
| Vite | 8.0.0-beta | Build tool & dev server |
| Tailwind CSS | 3.4.4 | Styling & UI components |
| Recharts | 3.7.0 | Interactive charts & visualization |
| Zustand | 5.0.11 | State management |
| Axios | 1.13.5 | HTTP requests |
| JSPDF & html2canvas | Latest | Client-side PDF export |

### **Backend**
| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| scikit-learn | Machine Learning algorithms |
| pandas | Data manipulation & analysis |
| NumPy | Numerical computations |
| SciPy | Statistical analysis |
| Matplotlib | Data visualization (charts) |
| ReportLab | PDF generation |
| Pillow | Image processing |
| Jinja2 | Template rendering |

### **Architecture**
- **Frontend**: Single Page Application (SPA) with React
- **Backend**: RESTful API with FastAPI
- **Communication**: JSON over HTTP/CORS
- **Database**: File-based experiment storage
- **Deployment**: Docker-ready with included Dockerfile

---

## 📁 Project Structure

```
ml-fit-monitor/
├── frontend/                          # React TypeScript Frontend
│   ├── src/
│   │   ├── api/
│   │   │   └── mlApi.ts             # API client (Axios)
│   │   ├── components/               # React components
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── UploadPanel.tsx
│   │   │   ├── DataProfilingDashboard.tsx
│   │   │   ├── ModelComparison.tsx
│   │   │   ├── FeatureImportance.tsx
│   │   │   ├── HyperparameterTuningResults.tsx
│   │   │   ├── DriftSimulation.tsx
│   │   │   ├── ExperimentHistory.tsx
│   │   │   ├── ReportExporter.tsx
│   │   │   └── ... more components
│   │   ├── store/
│   │   │   └── useMLStore.ts         # Zustand state management
│   │   ├── types/
│   │   │   └── mlTypes.ts            # TypeScript type definitions
│   │   ├── utils/
│   │   │   └── chartExtractor.ts     # Chart utility functions
│   │   ├── App.tsx                    # Main component
│   │   ├── main.tsx                   # Entry point
│   │   └── index.css                  # Global styles
│   ├── package.json                   # Dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── vite.config.ts                 # Vite config
│   └── tailwind.config.js             # Tailwind CSS config
│
├── backend/                           # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # FastAPI application & routes
│   │   ├── ml_pipeline.py            # ML model training pipeline
│   │   ├── fit_detector.py           # Model fit detection logic
│   │   ├── feature_importance.py     # Feature analysis
│   │   ├── hyperparameter_tuning.py  # Hyperparameter optimization
│   │   ├── model_evaluation.py       # Performance metrics
│   │   ├── data_profiling.py         # Data quality analysis
│   │   ├── drift.py                  # Model drift detection
│   │   ├── experiment_history.py     # Experiment tracking
│   │   ├── threshold_calibration.py  # Threshold optimization
│   │   ├── ensemble_models.py        # Ensemble techniques
│   │   ├── pdf_generator_new.py      # PDF report generation
│   │   ├── pdf_report_generator.py   # Alternative PDF engine
│   │   ├── schemas.py                # Request/response schemas
│   │   ├── utils.py                  # Utility functions
│   │   └── __init__.py
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Docker configuration
│   └── .env (optional)                # Environment variables
│
├── test files/                        # Test and validation scripts
│   ├── test_api.py
│   ├── test_comprehensive.py
│   ├── test_backend.py
│   └── ... more test files
│
├── README.md                          # This file
├── PROJECT.md                         # Project overview
└── SETUP_COMPLETE.md                  # Setup status
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.9+** (for backend)
- **Node.js 16+** & **npm 8+** (for frontend)
- **pip** (Python package manager)
- **Git** (optional, for version control)

### 1. Clone/Navigate to Project

```bash
cd ml-fit-monitor
```

### 2. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

**Backend will run at**: `http://localhost:8000`

### 3. Setup Frontend

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will run at**: `http://localhost:5173` (or similar)

### 4. Verify Setup

- Frontend: Open `http://localhost:5173` in your browser
- Backend API Docs: Open `http://localhost:8000/docs` (Swagger UI)
- Backend ReDoc: Open `http://localhost:8000/redoc` (ReDoc UI)

---

## 🔧 How It Works

### Complete Workflow

```
1. USER UPLOADS DATA
   ↓
2. DATA PREPROCESSING
   - Clean data
   - Handle missing values
   - Detect outliers
   - Type validation
   ↓
3. PROBLEM TYPE DETECTION
   - Classification or Regression?
   - Binary or Multi-class?
   ↓
4. DATA PROFILING
   - Statistical summary
   - Distribution analysis
   - Quality assessment
   ↓
5. TRAIN MULTIPLE MODELS
   - Split data (train/val)
   - Train 8 different algorithms
   - Calculate metrics for each
   ↓
6. FIT DETECTION
   - Analyze train vs validation gap
   - Classify: Good Fit / Overfitting / Underfitting
   - Generate confidence intervals
   ↓
7. FEATURE ANALYSIS
   - Calculate feature importance
   - Rank features by impact
   - Generate recommendations
   ↓
8. OPTIONAL: HYPERPARAMETER TUNING
   - Grid search best parameters
   - Retrain with optimized parameters
   - Compare improvements
   ↓
9. REPORT GENERATION
   - Generate comprehensive PDF
   - Include charts and metrics
   - Add recommendations
   ↓
10. DASHBOARD VISUALIZATION
    - Display all results
    - Interactive charts
    - Comparison views
```

### Key Algorithms & Techniques

#### Model Fit Detection
```
Good Fit: validation_score ≈ training_score (gap < 0.1)
Overfitting: validation_score << training_score (gap > 0.15)
Underfitting: Both scores low (< 0.6)
```

#### Feature Importance
- **Classification**: f_classif (ANOVA F-statistic)
- **Regression**: f_regression (Pearson correlation coefficient)
- Uses SelectKBest for ranking

#### Data Quality Assessment
- Outlier detection: IQR method (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
- Missing values: Percentage and recommendation
- Type inference: Auto-detect categorical vs numerical

#### Drift Detection
- Simulate dataset drift by modifying feature values
- Track model performance degradation
- Compare original vs drifted predictions

---

## 🔌 API Endpoints

### Core ML Endpoints

#### 1. **Pipeline Execution**
```
POST /api/pipeline
```
Main endpoint for training models on your data.

**Request**:
```json
{
  "data": "CSV or Excel file content",
  "target_column": "column_name",
  "test_size": 0.2,
  "random_state": 42
}
```

**Response**:
```json
{
  "summary": {
    "best_model": "RandomForestClassifier",
    "overall_fit_status": "Good Fit",
    "dataset_size": 1000,
    "val_score": 0.92,
    "gap": 0.03
  },
  "models": [
    {
      "model": "LogisticRegression",
      "train_score": 0.91,
      "val_score": 0.89,
      "gap": 0.02,
      "fit_status": "Good Fit",
      "metrics": {...}
    },
    {...}
  ],
  "feature_importance": [
    {"name": "age", "importance": 0.35},
    {"name": "income", "importance": 0.28}
  ]
}
```

#### 2. **Data Profiling**
```
POST /api/profile
```
Analyze data quality and statistics.

#### 3. **Feature Importance**
```
POST /api/feature-importance
```
Calculate and rank feature importance.

#### 4. **Hyperparameter Tuning**
```
POST /api/hyperparameter-tuning
```
Optimize model parameters.

#### 5. **Model Drift Simulation**
```
POST /api/drift-simulation
```
Simulate data drift and analyze impact.

#### 6. **Experiment Management**
- `POST /api/experiments` - Save experiment
- `GET /api/experiments` - List experiments
- `GET /api/experiments/{id}` - Get specific experiment
- `POST /api/experiments/compare` - Compare multiple experiments

#### 7. **PDF Report Generation**
```
POST /api/reports/advanced-pdf
```
Generate professional PDF report with all analysis results.

#### 8. **Threshold Calibration** (Classification)
```
POST /api/threshold-calibration
```
Optimize decision threshold for binary classification.

---

## 💡 Usage Guide

### Step 1: Prepare Your Data
- CSV or Excel file format (.csv, .xlsx, .xls)
- First row should be column names
- One column should be your target variable
- Examples: customer_churn, house_price, disease_diagnosis

### Step 2: Upload Data
1. Open the dashboard at `http://localhost:5173`
2. Click on "Upload Panel"
3. Select your data file
4. Choose target column
5. Click "Upload & Analyze"

### Step 3: View Results
The dashboard will show:
- **Data Profiling**: Dataset statistics and quality
- **Model Comparison**: Performance of all trained models
- **Model Fit Status**: Classification as Good/Over/Underfitting
- **Feature Importance**: Most important features
- **Recommendations**: Actionable improvement suggestions

### Step 4: Optional - Hyperparameter Tuning
1. Select a model to tune
2. Click "Tune Hyperparameters"
3. View before/after comparison
4. Apply tuned model

### Step 5: Generate Report
1. Click "Export as PDF"
2. Report downloads with all analysis
3. Share with stakeholders

### Step 6: Track Experiments
1. Save experiment (automatically saved after analysis)
2. View all experiments in "Experiment History"
3. Compare experiments side-by-side
4. Track improvements over time

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                             │
│            (React + TypeScript + Tailwind CSS)               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ UploadPanel  │  │  Dashboard   │  │ ReportExporter  │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                      Zustand Store                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ Axios HTTP Requests
                           ↓
┌──────────────────────────────────────────────────────────────┐
│         FastAPI Backend (Python)                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              CORS Middleware                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐ │
│  │ ML Pipeline  │ │ Data         │ │ Feature            │ │
│  │ - Training   │ │ Profiling    │ │ Importance         │ │
│  │ - Evaluation │ │ - QA         │ │ - Selection        │ │
│  │ - Metrics    │ │ - Analysis   │ │ - Ranking          │ │
│  └──────────────┘ └──────────────┘ └────────────────────┘ │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐ │
│  │ Hyperparameter│ │ Drift        │ │ PDF Generator      │ │
│  │ Tuning       │ │ Detection    │ │ - ReportLab        │ │
│  │ - Grid Search│ │ - Simulation │ │ - Charts           │ │
│  │ - Comparison │ │ - Analysis   │ │ - Formatting       │ │
│  └──────────────┘ └──────────────┘ └────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         scikit-learn ML Models                        │  │
│  │  - Logistic/Linear Regression  - Random Forest        │  │
│  │  - Ridge Regression            - Gradient Boosting   │  │
│  │  - Neural Networks (MLP)       - Ensemble Methods    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Processing Layer                         │  │
│  │  - pandas: Data manipulation & cleaning              │  │
│  │  - NumPy: Numerical computations                     │  │
│  │  - SciPy: Statistical analysis                       │  │
│  │  - sklearn preprocessing: Scaling, encoding          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Storage Layer                                │  │
│  │  - Experiment history (JSON files)                   │  │
│  │  - Generated reports (PDF files)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. FILE UPLOAD
   User File (CSV/Excel) → Browser → FormData → API

2. PREPROCESSING
   Raw Data → Clean → Type Detection → Train/Test Split

3. PARALLEL PROCESSING (8 Models)
   ├─ LogisticRegression/LinearRegression
   ├─ Ridge Regression
   ├─ RandomForest (Classifier/Regressor)
   ├─ GradientBoosting (Classifier/Regressor)
   └─ Neural Network (MLP)
   
4. ANALYSIS
   Models → Metrics → Feature Importance → Fit Detection
   
5. RESPONSE
   Results JSON → Browser → Zustand Store → Visualization

6. REPORT GENERATION
   Stored Data → PDF Engine → Downloadable PDF
```

### State Management (Zustand)

The frontend uses Zustand for state management with the following store:

```typescript
interface MLStore {
  // Data
  uploadedFile: File | null;
  analysisResults: AnalysisResults | null;
  dataProfile: DataProfile | null;
  
  // UI State
  isLoading: boolean;
  error: string | null;
  selectedModel: string;
  
  // Actions
  setUploadedFile: (file: File) => void;
  setAnalysisResults: (results: AnalysisResults) => void;
  // ... more actions
}
```

---

## 🔄 Development

### Project Setup for Development

```bash
# Install all dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# Start development servers
# Terminal 1:
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2:
cd frontend && npm run dev
```

### Key Files to Understand

| File | Purpose |
|------|---------|
| `backend/app/main.py` | REST API routes |
| `backend/app/ml_pipeline.py` | Model training logic |
| `backend/app/fit_detector.py` | Fit detection algorithm |
| `frontend/src/store/useMLStore.ts` | Global state |
| `frontend/src/api/mlApi.ts` | API client |
| `frontend/src/components/DashboardLayout.tsx` | Main UI layout |

### Building for Production

**Frontend**:
```bash
cd frontend
npm run build
# Output: dist/ folder with optimized files
```

**Backend**:
```bash
# Use Dockerfile for containerization
docker build -t ml-fit-monitor:latest .
docker run -p 8000:8000 ml-fit-monitor:latest
```

### Testing

```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend linting
cd frontend
npm run lint
```

---

## 📊 Example Workflow

### Training a Classification Model

1. **Prepare Data**: Customer churn dataset (1000 rows, 15 features)

2. **Upload**: Click upload, select churn_prediction.csv, target="churned"

3. **Automatic Analysis**:
   - Data profiling: 85% data quality, 2% missing values
   - 8 models trained simultaneously
   - Best model: RandomForest (97% validation accuracy)
   - Fit Status: **Good Fit** (gap = 0.02)

4. **Feature Importance**:
   - Monthly_charges (32% importance)
   - Contract_type (28%)
   - Internet_service (19%)
   - Recommendations: Focus on pricing strategy

5. **Hyperparameter Tuning**:
   - Grid search optimizes parameters
   - Improves accuracy from 97% → 98.5%

6. **Report**: PDF generated with executive summary, confusion matrix, feature rankings, recommendations

7. **Tracking**: Experiment saved for future comparison

---

## 🤝 Contributing

### Adding New Features

1. **New ML Model**: Add to `backend/app/ml_pipeline.py`
2. **New Metric**: Add to `backend/app/model_evaluation.py`
3. **New UI Component**: Add to `frontend/src/components/`
4. **New API Endpoint**: Add to `backend/app/main.py`

### Code Style

- **Python**: PEP 8
- **TypeScript**: ESLint configuration in project
- **Formatting**: Automatic with Prettier/Black

---

## 📝 Common Issues & Solutions

### Issue: Port Already in Use
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 9000
```

### Issue: CORS Errors
- Ensure backend is running on correct port
- Check frontend URL in backend CORS configuration
- Verify no proxy/firewall blocking

### Issue: Out of Memory with Large Files
- Use data sampling for initial analysis
- Process in chunks
- Increase RAM or optimize data types

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Project Details**: See `PROJECT.md`
- **Setup Status**: See `SETUP_COMPLETE.md`

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 🙋 Support

For issues, questions, or feature requests:
1. Check existing test files for examples
2. Review API documentation at `/docs` endpoint
3. Check backend logs for error details
4. Verify all dependencies are correctly installed

---

## 🎯 Roadmap

Future enhancements:
- [ ] Real-time model monitoring dashboard
- [ ] Advanced ensemble techniques
- [ ] Time-series model support
- [ ] Explainability with SHAP values
- [ ] Multi-class classification improvements
- [ ] Cloud deployment templates
- [ ] Mobile app support
- [ ] Advanced data visualization options

---

**Built with ❤️ for ML practitioners**

---

Last Updated: April 2026
