"""
Diagnostic script to identify which module import is hanging
"""
import sys
import time

def test_import(module_name):
    print(f"Testing import: {module_name}...", end=" ", flush=True)
    start = time.time()
    try:
        __import__(module_name)
        elapsed = time.time() - start
        print(f"✅ ({elapsed:.2f}s)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Add backend to path
sys.path.insert(0, r"c:\Users\chira\Downloads\ml-fit-monitor\backend")

modules = [
    "app.drift",
    "app.fit_detector",
    "app.ml_pipeline",
    "app.hyperparameter_tuning",
    "app.experiment_history",
    "app.threshold_calibration",
    "app.feature_importance",
    "app.model_evaluation",
    "app.data_profiling",
    "app.pdf_report_generator",
]

print("="*60)
print("Testing module imports...")
print("="*60)

for module in modules:
    if not test_import(module):
        print(f"\n⚠️  Failed on module: {module}")
        break

print("\n" + "="*60)
print("Now testing FastAPI app import...")
print("="*60)
test_import("app.main")
