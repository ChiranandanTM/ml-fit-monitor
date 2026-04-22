"""
Test FastAPI app directly without network
"""
import sys
sys.path.insert(0, r"c:\Users\chira\Downloads\ml-fit-monitor\backend")

from fastapi.testclient import TestClient
from app.main import app

print("="*60)
print("Testing FastAPI app with TestClient")
print("="*60)

client = TestClient(app)

print("\n1️⃣ Testing root endpoint...")
try:
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n2️⃣ Testing /docs endpoint...")
try:
    response = client.get("/docs")
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.content)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n3️⃣ Testing /generate-dataset endpoint...")
try:
    response = client.get("/generate-dataset/good_fit")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Generated dataset shape: {data.get('rows')} x {data.get('columns')}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ Direct app testing complete!")
print("="*60)
