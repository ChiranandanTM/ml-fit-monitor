# 🧠 ML Fit Monitor — Model Quality Intelligence Platform

A comprehensive **ML Model Quality Decision-Support System** that **automatically analyzes** machine learning models, detects overfitting/underfitting, and provides **actionable improvement recommendations**. Features a stunning dark-themed React dashboard and a powerful FastAPI backend.

---

## 🎯 What This Project Does

**The Problem:** Most people only look at accuracy scores. But a 95% accurate model could be completely useless if:
- 🔴 It's **overfitted** (memorized training data, poor real-world performance)
- 🔴 It's **underfitted** (too simple to capture patterns)
- 🔴 It will **fail in production** when data distribution changes

**The Solution:** ML Fit Monitor **automatically detects** which category your model falls into and **tells you exactly what to do** to fix it.

---

## 🔄 How It Works: Complete Workflow

```
USER UPLOADS CSV DATASET
          ↓
    DATA CLEANING
    ├─ Fill missing values
    ├─ Encode categorical
    ├─ Detect outliers
    └─ Normalize features
          ↓
   TRAIN TEST SPLIT (80/20)
          ↓
   TRAIN 4 MODELS IN PARALLEL
   ├─ Logistic Regression / Linear Regression
   ├─ Random Forest (100 trees)
   ├─ Gradient Boosting (100 estimators)
   └─ Neural Network (adaptive layers)
          ↓
   EVALUATE EACH MODEL
   ├─ Calculate training score
   ├─ Calculate validation score
   ├─ K-fold cross-validation
   ├─ Confidence intervals (95%)
   └─ Learning curves
          ↓
   AUTOMATICALLY DETECT FIT STATUS
   ├─ train ≥ 0.80, val ≥ 0.75, gap ≤ 0.08 → ✅ GOOD FIT (generalize well)
   ├─ train >> val (gap > 0.15) → ⚠️ OVERFITTING (memorized data)
   └─ both low (val < 0.60) → ❌ UNDERFITTING (too simple)
          ↓
   GENERATE INTERACTIVE DASHBOARD
   ├─ Model comparison charts
   ├─ Fit status cards with visual indicators
   ├─ Learning curves visualization
   ├─ 6+ actionable improvement suggestions
   └─ Optional: Data drift simulation
          ↓
   DISPLAY RESULTS IN REACT UI
```

---

## 🌟 Key Features

### 1️⃣ Automatic Fit Status Detection ✨
No manual threshold tuning. The system **automatically classifies** your model:

| Status | What It Means | Example | What To Do |
|--------|--------------|---------|-----------|
| ✅ **Good Fit** | Model generalizes well | Train 82%, Val 80%, Gap 2% | Deploy with monitoring |
| ⚠️ **Overfitting** | Memorized training data | Train 95%, Val 60%, Gap 35% | Add regularization, get more data |
| ❌ **Underfitting** | Model too simple | Train 55%, Val 50%, Gap 5% | Increase complexity, engineer features |

### 2️⃣ Advanced Analytics
- **Learning Curves** - See how scores improve with more training data
- **Cross-Validation** - 95% confidence intervals from k-fold CV
- **Bias-Variance Analysis** - Understand the bias-variance tradeoff
- **Generalization Score** - Smart model ranking

### 3️⃣ Actionable Recommendations
Smart suggestions tailored to **your specific problem**:

**If Overfitting:** 
1. [HIGH] Increase regularization (L1/L2)
2. [HIGH] Remove non-informative features
3. [MEDIUM] Collect more training data

**If Underfitting:**
1. [HIGH] Increase model complexity
2. [HIGH] Engineer more features
3. [MEDIUM] Improve data quality

### 4️⃣ Data Drift Simulation
**Realistic production scenario testing:**
- Simulate 5%, 10%, 15%, 20%, 30%, 50% data distribution shifts
- Watch performance degrade in real-time
- Get automatic retraining trigger recommendations
- Know when model monitoring is critical

### 5️⃣ Four Analysis Modes
Choose what you need:

| Mode | Use Case | Time | Output |
|------|----------|------|--------|
| 📊 **Train** | Quick model check | 5-8 sec | Fit status + scores |
| 🔬 **Analyze** | Complete assessment | 10-20 sec | Everything (full report) |
| 💡 **Suggest** | Improvement focus | 5-10 sec | Prioritized recommendations |
| 📈 **Drift** | Production risk | 4-6 sec | Degradation curves + triggers |

---

## 🛠️ System Architecture

### Two-Tier Architecture

```
FRONTEND (React + TypeScript)          BACKEND (FastAPI + Python)
─────────────────────────────          ──────────────────────────

┌─────────────────────────┐             ┌──────────────────────┐
│   Upload Panel          │             │  FastAPI Routes      │
│  - File upload          │────────────▶│  /train              │
│  - Mode selection (4)   │             │  /analyze            │
│  - Sample generation    │◀────────────│  /suggest            │
└─────────────────────────┘             │  /drift-simulate     │
         ▼                              │  /generate-dataset   │
┌─────────────────────────┐             └──────────────────────┘
│  Model Comparison Cpt   │                     ▼
│  (Bar Chart)            │             ┌──────────────────────┐
└─────────────────────────┘             │   ML Pipeline        │
         ▼                              │  1. Clean data       │
┌─────────────────────────┐             │  2. Train 4 models   │
│  FitStatusCard Cpt      │             │  3. Evaluate scores  │
│  (Status Badge + Score) │             │  4. Detect fit       │
└─────────────────────────┘             └──────────────────────┘
         ▼                                     ▼
┌─────────────────────────┐             ┌──────────────────────┐
│  LearningCurves Cpt     │             │  Fit Detector        │
│  (Analytics Detail)     │             │  (Programmatic rules)│
└─────────────────────────┘             │  - Good Fit          │
         ▼                              │  - Overfitting       │
┌─────────────────────────┐             │  - Underfitting      │
│  SuggestionsPanel Cpt   │             └──────────────────────┘
│  (Improvement list)     │                     ▼
└─────────────────────────┘             ┌──────────────────────┐
         ▼                              │  Drift Simulator     │
┌─────────────────────────┐             │  (Severity analysis) │
│  DriftSimulation Cpt    │             └──────────────────────┘
│  (Drift curve + alert)  │
└─────────────────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Node.js 18+

### Step 1: Start Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate  # Windows or: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
✓ Backend running at: **http://localhost:8000**

### Step 2: Start Frontend (New Terminal)
```bash
cd frontend
npm install
npm run dev
```
✓ Frontend running at: **http://localhost:5174**

### Step 3: Use It!
1. Open http://localhost:5174
2. Click "Upload CSV" or "Generate Dataset"
3. See results instantly!

---

## 📊 Understanding Results

### Example: Your Overfitting Model

```
MODEL: Neural Network
STATUS: ⚠️ OVERFITTING

Train Score: 95%    │████████████████████│ (Very High)
Val Score:   60%    │████████│ (Low)
Gap:         35%    │████████████████████████│ (High gap = Problem!)

95% Confidence: [58%, 62%]

DIAGNOSIS:
  Bias:     0.5% (Good - model is learning)
  Variance: 8.2% (BAD - high variance = overfitting)
  
NEXT STEPS:
  1. [HIGH] Add L1/L2 regularization
  2. [HIGH] Remove redundant features
  3. [MEDIUM] Collect more data
```

### What Each Metric Means

| Metric | Interpretation |
|--------|----------------|
| **Train Score** | How well model performs on training data |
| **Val Score** | How well model performs on unseen data |
| **Gap** | Difference between train & val (should be small) |
| **Confidence Interval** | 95% CI - where true score probably lies |
| **Bias** | Distance from perfect score (how wrong on average) |
| **Variance** | Sensitivity to different training data |

---

## 🧪 Test It Out

### Option A: Upload a CSV
Format requirements:
```csv
feature1,feature2,feature3,target
1.5,2.3,3.1,0
2.1,2.8,3.5,1
3.2,3.5,4.1,0
```
Minimum 4 rows, last column is target

### Option B: Generate Samples
Frontend buttons generate:
- ✅ **Good Fit** - Balanced train/val (~80% both)
- ⚠️ **Overfitting** - Train 100%, Val 60%
- ❌ **Underfitting** - Train 60%, Val 40%

### Option C: Use Test Files
Included:
- `good_fit_dataset.csv`
- `test_complex_dataset.csv`
- `underfitting_dataset_new.csv`

---

## 🔧 API Endpoints

All endpoints accept CSV file uploads

```bash
# Basic training & fit detection
POST /train → 5-8 sec response
Response: Model metrics, fit status, learning curves

# Comprehensive analysis
POST /analyze → 10-20 sec response
Response: Executive summary, suggestions, drift analysis

# Improvement recommendations
POST /suggest → 5-10 sec response
Response: Prioritized suggestions per model

# Production risk assessment
POST /drift-simulate → 4-6 sec response
Response: Degradation curves, trigger levels

# Generate sample datasets
GET /generate-dataset/{fit_type}
Types: good_fit, overfitting, underfitting
Response: CSV data ready for training
```

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend UI** | React 19.2, TypeScript, Vite 8 |
| **Styling** | Tailwind CSS + Custom CSS Design System |
| **Charts** | Recharts 3.7 (interactive) |
| **State** | Zustand 5.0 (lightweight) |
| **HTTP Client** | Axios |
| **Backend API** | FastAPI (async) |
| **ML Models** | scikit-learn (4 algorithms) |
| **Data Processing** | pandas, numpy |
| **Statistics** | scipy |
| **Server** | Uvicorn (ASGI) |

---

## 📁 Project Structure

```
ml-fit-monitor/
├── backend/app/
│   ├── main.py                # 5 API endpoints
│   ├── ml_pipeline.py         # Model training logic
│   ├── fit_detector.py        # Automatic fit detection
│   ├── drift.py               # Data drift simulation
│   └── utils.py               # Helper functions
│
├── frontend/src/
│   ├── components/            # 7 React components
│   │   ├── UploadPanel.tsx     # File upload + mode selector
│   │   ├── ModelComparison.tsx # Bar chart
│   │   ├── FitStatusCard.tsx   # Status + scores
│   │   ├── LearningCurves.tsx  # Analytics detail
│   │   ├── SuggestionsPanel.tsx# Recommendations
│   │   ├── DriftSimulation.tsx # Drift analysis
│   │   └── DashboardLayout.tsx # Smart routing
│   ├── api/mlApi.ts           # API client
│   ├── store/useMLStore.ts    # State management
│   └── types/mlTypes.ts       # TypeScript definitions
│
└── test_*.csv                # Test datasets
└── test_*.py                 # Test scripts
```

---

## 🚀 Real-World Example Workflow

### Scenario: You built a model with 95% accuracy

**Step 1: Upload to ML Fit Monitor**
```
Result: Train 95%, Val 60% → ⚠️ OVERFITTING DETECTED
```

**Step 2: See the Problem**
```
Gap: 35% (way too high!)
Diagnosis: Model memorized training data
Severity: HIGH - won't perform in production
```

**Step 3: Get Recommendations**
```
[HIGH] Add L1/L2 regularization
[HIGH] Remove low-importance features  
[MEDIUM] Collect more training data
[MEDIUM] Use ensemble methods
[LOW] Cross-validation hyperparameter tuning
```

**Step 4: Simulate Production Risk**
```
With 10% data drift:
├─ Current: 60% score
├─ After drift: 35% score (-25%)
├─ Severity: 🔴 CRITICAL
└─ Action: Retrain immediately
```

**Step 5: Improve & Retry**
```
Make changes → Re-upload → Check fit status → Verify improvement
```

---

## ⚠️ Drift Trigger Levels

As data distribution changes:

| Drop % | Level | Action | Monitoring |
|--------|-------|--------|-----------|
| < 5% | 🟢 Stable | Continue normal ops | Daily |
| 5-10% | 🟡 Warning | Monitor closely | Every 4 hours |
| 10-15% | 🟠 Alert | Prepare retraining | Every 30 min |
| 15-25% | 🔴 Critical | Retrain immediately | Continuous |
| > 25% | 🔴 Failsafe | Switch to backup model | Real-time |

---

## 🎓 Learning Resources

**New to ML diagnostics?** Start here:

1. **Upload** `good_fit_dataset.csv` → Understand what good looks like
2. **Upload** `underfitting_dataset_new.csv` → See why complexity matters  
3. **Upload** `test_complex_dataset.csv` → Observe overfitting signal
4. **Try** each analysis mode to understand their value
5. **Experiment** with the improvement suggestions

---

## 📝 API Endpoints Reference

```bash
# Health check
GET http://localhost:8000/ → {"message": "..."}

# Interactive API docs
GET http://localhost:8000/docs → Swagger UI

# Upload and train models
POST http://localhost:8000/train
  Input: CSV file
  Output: {models: [...], task_type: "classification|regression"}

# Full analysis with everything
POST http://localhost:8000/analyze
  Input: CSV file
  Output: {executive_summary, model_analysis, suggestions, drift_analysis}

# Get improvement suggestions
POST http://localhost:8000/suggest
  Input: CSV file
  Output: {model_suggestions: [...], general_recommendations}

# Simulate data drift
POST http://localhost:8000/drift-simulate
  Input: CSV file
  Output: {models: [...], severity_tested: [0.05, 0.10, ...]}

# Generate sample dataset
GET http://localhost:8000/generate-dataset/good_fit
  Output: {csv: "...", filename, rows, columns}
  Types: good_fit, overfitting, underfitting
```

---

## 🐛 Troubleshooting

### CORS Error When Uploading?
**Problem:** "Access-Control-Allow-Origin blocked"

**Solution:** Update backend CORS in `backend/app/main.py`:
```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",  # Add any port you're using
    "http://localhost:3000"
]
```
Then restart backend: `uvicorn app.main:app --reload`

### Import Errors?
```bash
# Ensure venv is active
.\venv\Scripts\Activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port Already in Use?
```bash
# Use different port
uvicorn app.main:app --port 8001
npm run dev -- --port 5175
```

---

## ✨ All Features Implemented

✅ Upload any CSV dataset
✅ Automatic problem type detection
✅ Train 4 different model types
✅ Programmatic fit status detection
✅ Learning curve generation
✅ Confidence interval calculation
✅ Bias-variance analysis
✅ Actionable improvement suggestions
✅ Data drift simulation (6 severity levels)
✅ Retraining trigger recommendations
✅ 4 analysis modes
✅ Interactive dark-themed UI
✅ Responsive design (mobile-friendly)
✅ Sample dataset generation

---

## 🎉 You're Ready!

Open **http://localhost:5174** and start analyzing models!

**Questions?** Check the tests:
- `test_comprehensive.py` - See all workflows
- `test_fit_status_verification.py` - Understand detection
- `test_frontend_integration.py` - Verify integration

**Happy model optimization! 🚀**
