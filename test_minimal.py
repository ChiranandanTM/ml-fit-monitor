"""
Minimal test to identify the hang issue
"""
import sys
sys.path.insert(0, r"c:\Users\chira\Downloads\ml-fit-monitor\backend")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Test 1: App with just root endpoint
app1 = FastAPI()

@app1.get("/")
def root():
    return {"message": "Test 1: Basic endpoint"}

# Test 2: App with CORS
app2 = FastAPI()
app2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app2.get("/")
def root2():
    return {"message": "Test 2: With CORS"}

# Test 3: App with imports from main
print("Testing basic app creation...")
try:
    from app.main import app
    print("✅ App imported successfully")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

print("\nApp is ready for testing")
print(f"App title: {app.title}")
print(f"Number of routes: {len(app.routes)}")

# Show first few routes
print("\nFirst 10 routes:")
for i, route in enumerate(app.routes[:10]):
    if hasattr(route, 'path'):
        print(f"  {i+1}. {route.path}")
    if i >= 9:
        break
