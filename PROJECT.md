# ML Fit Monitor - Project Documentation

## 📋 Project Overview

**ML Fit Monitor** is an advanced **Machine Learning Model Quality Decision-Support System** that helps data scientists and ML engineers evaluate, analyze, and monitor machine learning models. The system automatically detects model fit status (Good Fit, Overfitting, or Underfitting), provides detailed analysis, generates comprehensive reports, and offers actionable recommendations for model improvement.

The application provides a full-stack solution with a React-based interactive dashboard and a Python FastAPI backend that handles all ML computations and model evaluations.

---

## 🎯 Key Features

### 1. **Model Fit Detection**
- Automatically detects whether a model is:
  - **Good Fit**: Balanced performance on training and validation data
  - **Overfitting**: High training accuracy but lower validation accuracy
  - **Underfitting**: Low performance on both training and validation data
- Uses confidence intervals and statistical analysis for accurate detection

### 2. **Multi-Model Comparison**
- Train multiple ML models simultaneously on your dataset
- Supported models include:
  - Logistic Regression, Linear Regression, Ridge Regression
  - Random Forest Classifier/Regressor
  - Gradient Boosting Classifier/Regressor
  - Neural Network (MLP) Classifier/Regressor
- Compare model performance side-by-side with detailed metrics

### 3. **Data Profiling & Quality Analysis**
- Automatic dataset profiling
- Data quality checks and recommendations
- Outlier detection using IQR (Interquartile Range)
- Missing value analysis
- Feature statistics and distributions

### 4. **Feature Importance Analysis**
- Identify which features contribute most to model predictions
- Feature selection using SelectKBest algorithm
- Feature recommendations for improving model performance
- Visualization of feature importance rankings

### 5. **Hyperparameter Tuning**
- Automated hyperparameter optimization
- Grid search for optimal parameter combinations
- Performance comparison before and after tuning
- Tuning history and trend analysis

### 6. **Experiment History & Tracking**
- Save and track all experiments
- Compare multiple experiments side-by-side
- View experiment trends over time
- Retrieve detailed results from past experiments

### 7. **Model Drift Detection**
- Simulate and detect data drift
- Analyze drift trends and impact on model performance
- Generate drift analysis reports
- Monitor model stability over time

### 8. **Classification & Regression Analysis**
- ROC Curves and AUC analysis (for classification)
- Learning curves to detect overfitting/underfitting
- Confusion matrices for classification tasks
- Comprehensive metric calculations (Accuracy, Precision, Recall, F1-Score, MSE, R²)
- Optimal threshold finding for binary classification

### 9. **Threshold Calibration**
- Adaptive threshold calibration for classification models
- Optimize decision boundaries based on business requirements
- Generate adaptive fit detectors

### 10. **PDF Report Generation**
- Generate professional PDF reports with:
  - Executive summary
  - Model performance metrics
  - Feature importance charts
  - Confusion matrices
  - Recommendations for improvement
- Multiple report generation engines for flexibility

### 11. **Interactive Dashboard**
- Real-time visualization of analysis results
- Charts and graphs powered by Recharts
- Responsive design for all screen sizes
- Data upload panel for easy dataset integration
- Comprehensive suggestion panel with recommendations

---

## 💻 Tech Stack

### **Frontend**
- **Framework**: React 19.2.0
- **Language**: TypeScript 5.9.3
- **Build Tool**: Vite 8.0.0 (Beta)
- **UI Framework**: Tailwind CSS 3.4.4
- **Styling**: PostCSS with Autoprefixer
- **Charts**: Recharts 3.7.0 (Interactive data visualization)
- **State Management**: Zustand 5.0.11
- **HTTP Client**: Axios 1.13.5
- **PDF Export**: 
  - jsPDF 4.2.1 (PDF generation)
  - html2canvas 1.4.1 (Canvas to image conversion)
- **Linting**: ESLint 9.39.1
- **Code Compiler**: Babel React Compiler 1.0.0

### **Backend**
- **Framework**: FastAPI (High-performance API framework)
- **Server**: Uvicorn (ASGI server)
- **Language**: Python 3.x
- **Core Libraries**:
  - **scikit-learn**: Machine learning algorithms and evaluation metrics
  - **pandas**: Data manipulation and analysis
  - **NumPy**: Numerical computing
  - **SciPy**: Scientific computing (statistics, distributions)
  - **python-multipart**: File upload handling
  
- **Data Processing**:
  - **openpyxl**: Excel file reading/writing
  - **xlrd**: Legacy Excel support
  
- **Reporting & Visualization**:
  - **reportlab**: PDF generation with ReportLab
  - **matplotlib**: Data visualization
  - **Pillow**: Image processing
  - **weasyprint**: PDF rendering from HTML/CSS
  - **jinja2**: HTML templating
  
- **Architecture**: CORS-enabled for local development
- **Port**: 9000 (configurable)

### **Deployment**
- **Docker**: Containerized backend (Dockerfile provided)
- **Database**: Experiment history stored locally (JSON-based or file-based)

---

## 📁 Project Structure

```
ml-fit-monitor/
├── frontend/                          # React TypeScript Application
│   ├── src/
│   │   ├── components/               # React Components
│   │   │   ├── DashboardLayout.tsx          # Main dashboard container
│   │   │   ├── UploadPanel.tsx              # File upload interface
│   │   │   ├── DataProfilingDashboard.tsx   # Data quality analysis
│   │   │   ├── FitStatusCard.tsx            # Model fit status display
│   │   │   ├── ModelComparison.tsx          # Side-by-side model comparison
│   │   │   ├── FeatureImportance.tsx        # Feature importance visualization
│   │   │   ├── ExperimentHistory.tsx        # Experiment tracking
│   │   │   ├── ExperimentComparison.tsx     # Compare multiple experiments
│   │   │   ├── HyperparameterTuningResults.tsx # Tuning results
│   │   │   ├── DriftSimulation.tsx          # Drift detection
│   │   │   ├── ROCAnalysis.tsx              # ROC curve analysis
│   │   │   ├── LearningCurves.tsx           # Learning curve visualization
│   │   │   ├── MetricsDeltaTable.tsx        # Metric comparison table
│   │   │   ├── SuggestionsPanel.tsx         # Recommendations panel
│   │   │   └── ReportExporter.tsx           # PDF report generation
│   │   ├── api/
│   │   │   └── mlApi.ts                     # API client for backend
│   │   ├── store/
│   │   │   └── useMLStore.ts                # Zustand state management
│   │   ├── types/
│   │   │   └── mlTypes.ts                   # TypeScript type definitions
│   │   ├── utils/
│   │   │   └── chartExtractor.ts            # Chart utilities
│   │   ├── App.tsx                    # Root component
│   │   ├── main.tsx                   # Application entry point
│   │   └── index.css                  # Global styles
│   ├── package.json                   # Dependencies and scripts
│   ├── vite.config.ts                 # Vite configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   └── tailwind.config.js             # Tailwind CSS configuration
│
├── backend/                           # FastAPI Python Application
│   ├── app/
│   │   ├── main.py                          # FastAPI application & endpoints
│   │   ├── ml_pipeline.py                   # Core ML pipeline logic
│   │   ├── fit_detector.py                  # Model fit status detection
│   │   ├── model_evaluation.py              # Classification/regression metrics
│   │   ├── feature_importance.py            # Feature analysis
│   │   ├── hyperparameter_tuning.py         # Hyperparameter optimization
│   │   ├── experiment_history.py            # Experiment tracking & storage
│   │   ├── drift.py                         # Data drift detection
│   │   ├── threshold_calibration.py         # Decision threshold optimization
│   │   ├── data_profiling.py                # Data quality analysis
│   │   ├── ensemble_models.py               # Ensemble model utilities
│   │   ├── pdf_report_generator.py          # PDF report generation
│   │   ├── pdf_generator_new.py             # Advanced PDF engine
│   │   ├── pdf_generator_advanced.py        # Enhanced PDF features
│   │   ├── pdf_generator_canvas.py          # Canvas-based PDF
│   │   ├── pdf_generator_charts.py          # Chart PDF integration
│   │   ├── monitoring_dashboard.py          # Dashboard backend logic
│   │   ├── schemas.py                       # Pydantic models for validation
│   │   └── utils.py                         # Helper utilities
│   ├── requirements.txt                # Python dependencies
│   └── Dockerfile                      # Docker containerization
│
├── SETUP_COMPLETE.md                  # Setup documentation
└── PROJECT.md                          # This file
```

---

## 🔄 How the Project Works

### **High-Level Architecture**

```
User Upload → React Dashboard → FastAPI Backend → ML Pipeline → Results → PDF Report
                (Frontend)         (Port 9000)      (scikit-learn)     (Visualization)
```

### **Workflow Steps**

#### 1. **Data Upload**
- User uploads a CSV or Excel file through the UploadPanel component
- Frontend sends file to backend via `/upload` endpoint
- Backend reads and preprocesses the data using pandas

#### 2. **Problem Type Detection**
- Backend automatically detects if the task is **classification** or **regression**
- Uses data characteristics and target variable analysis
- Adjusts model selection accordingly

#### 3. **Model Training Pipeline** (`ml_pipeline.py`)
- **Train-Test Split**: Divides data (80% train, 20% test)
- **Feature Preprocessing**: Standardization and encoding
- **Model Training**: Trains multiple models in parallel
- **Cross-Validation**: Uses adaptive CV (2-3 folds based on dataset size)
- **Metric Calculation**: Computes accuracy, F1, precision, recall, etc.

#### 4. **Fit Status Detection** (`fit_detector.py`)
- Compares training score vs validation score
- Calculates the performance gap
- Determines fit status based on thresholds:
  - **Good Fit**: Balanced performance (gap < 10%)
  - **Overfitting**: Large gap (training >> validation)
  - **Underfitting**: Low performance on both

#### 5. **Feature Analysis** (`feature_importance.py`)
- Extracts feature importance from tree-based models
- Uses SelectKBest for linear models
- Generates recommendations for top features
- Identifies potentially irrelevant features

#### 6. **Data Profiling** (`data_profiling.py`)
- Analyzes dataset statistics
- Detects outliers using IQR method
- Identifies data quality issues
- Provides recommendations for data cleaning

#### 7. **Experiment Tracking** (`experiment_history.py`)
- Saves all analysis results with metadata (timestamp, parameters)
- Stores in JSON format for persistence
- Enables comparison between experiments
- Tracks performance trends over time

#### 8. **Advanced Analysis**
- **Hyperparameter Tuning**: Grid search optimization
- **Drift Detection**: Simulates data drift scenarios
- **Threshold Calibration**: Finds optimal decision boundaries
- **ROC Analysis**: Generates ROC curves for classification

#### 9. **PDF Report Generation**
- Collects all analysis results
- Generates professional PDF using ReportLab
- Includes charts, metrics, and recommendations
- Uses multiple rendering engines for flexibility

#### 10. **Dashboard Visualization**
- Frontend receives API responses
- Updates Zustand state management
- Renders charts using Recharts
- Displays recommendations and insights

---

## 🚀 Running the Project

### **Frontend Setup**
```bash
cd frontend
npm install          # Install dependencies
npm run dev         # Start Vite dev server (http://localhost:5173)
npm run build       # Build for production
```

### **Backend Setup**
```bash
cd backend
pip install -r requirements.txt    # Install Python dependencies
python -m uvicorn app.main:app --host 0.0.0.0 --port 9000  # Start API
```

### **Docker (Optional)**
```bash
cd backend
docker build -t ml-fit-monitor .
docker run -p 9000:8000 ml-fit-monitor
```

---

## 🔌 Main API Endpoints

### **Core Endpoints**
- `POST /upload` - Upload and analyze dataset
- `POST /train` - Train multiple models
- `GET /models` - Get trained model results
- `GET /fit-status` - Get model fit status
- `GET /feature-importance` - Get feature importance analysis

### **Analysis Endpoints**
- `POST /data-profile` - Profile dataset quality
- `GET /outliers` - Detect outliers
- `POST /hyperparameter-tune` - Optimize hyperparameters
- `POST /drift/simulate` - Simulate data drift
- `GET /drift/analysis` - Get drift analysis

### **Experiment & Reporting**
- `POST /experiments` - Save experiment
- `GET /experiments` - List all experiments
- `GET /experiments/{id}` - Get specific experiment
- `POST /experiments/compare` - Compare experiments
- `POST /reports/advanced-pdf` - Generate PDF report

---

## 📊 Key Technologies Explained

### **scikit-learn**
- Provides ML algorithms (Random Forest, Gradient Boosting, Neural Networks)
- Calculates evaluation metrics and cross-validation scores
- Implements feature selection and preprocessing

### **Recharts**
- Interactive React charting library
- Visualizes model performance, feature importance, ROC curves
- Responsive and mobile-friendly

### **Zustand**
- Lightweight state management
- Stores ML analysis results across components
- Eliminates prop drilling

### **FastAPI**
- Auto-generates API documentation (Swagger/OpenAPI)
- Type-safe endpoints with Pydantic validation
- High performance and async support
- CORS enabled for local frontend communication

### **ReportLab**
- Generates PDFs programmatically
- Creates tables, charts, and formatted text
- No external dependencies like matplotlib subprocess

---

## 🎓 Use Cases

1. **Model Evaluation**: Quickly assess if trained models are overfit or underfit
2. **Feature Engineering**: Identify important features for model improvement
3. **Experiment Tracking**: Maintain history of all model training experiments
4. **Data Quality**: Profile and analyze dataset characteristics
5. **Model Monitoring**: Detect data drift and model performance degradation
6. **Decision Support**: Get actionable recommendations for ML improvements
7. **Stakeholder Reports**: Generate professional PDF reports for presentations

---

## 🔐 Security Considerations

- CORS properly configured for localhost development
- File upload validation in backend
- Type safety with TypeScript and Pydantic
- Input sanitization for JSON serialization

---

## 📝 Notes

- The system uses **adaptive cross-validation** (2-3 folds) for faster training on large datasets
- **Port 9000** is used to avoid Windows socket TIME_WAIT issues
- PDF reports use **ReportLab** for reliability and minimal dependencies
- Experiment data is stored locally for persistence across sessions
- Multiple PDF generation engines available for different use cases

---

## 🎯 Future Enhancements

- Cloud deployment (AWS, Azure, GCP integration)
- Real-time model monitoring dashboard
- Advanced ensemble techniques
- Custom model architecture support
- SHAP explainability integration
- Multi-user support with authentication
- Model versioning and registry
- REST API client libraries

---

**Created**: 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
