"""
Quick backend health check script
"""
import requests
import json
from time import sleep

print("="*60)
print("ML FIT MONITOR - Backend Health Check")
print("="*60)

# Test 1: Check if backend is running
print("\n1️⃣ Checking if backend is running...")
try:
    # Extended timeouts: (connection_timeout, read_timeout)
    response = requests.get("http://localhost:8000/", timeout=(5, 30))
    print(f"✅ Backend is running!")
    print(f"   Response: {response.status_code}")
    print(f"   Message: {response.json()}")
except requests.exceptions.ConnectionError:
    print("❌ Connection Error - Backend is NOT running")
    print("   Start it with: cd backend && uvicorn app.main:app --reload --port 8000")
    exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    exit(1)

# Test 2: Check if we can generate a dataset
print("\n2️⃣ Testing /generate-dataset endpoint...")
try:
    response = requests.get("http://localhost:8000/generate-dataset/good_fit", timeout=(5, 30))
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Generate dataset works!")
        print(f"   File: {data.get('filename')}")
        print(f"   Size: {data.get('rows')} rows × {data.get('columns')} cols")
    else:
        print(f"❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 3: Test training with a sample file
print("\n3️⃣ Testing /train endpoint (this may take 30-60 seconds)...")
try:
    # First, generate a sample dataset
    response = requests.get("http://localhost:8000/generate-dataset/good_fit", timeout=(5, 30))
    if response.status_code == 200:
        csv_content = response.json().get('csv')
        
        if csv_content:
            # Save as CSV
            with open('temp_test.csv', 'w') as f:
                f.write(csv_content)
            
            # Try to upload and train
            with open('temp_test.csv', 'rb') as f:
                files = {'file': f}
                # Extended timeout for training: (connection, read)
                response = requests.post("http://localhost:8000/train", files=files, timeout=(5, 120))
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Training works!")
                print(f"   Models trained: {len(data.get('models', []))}")
                if 'models' in data and len(data['models']) > 0:
                    print(f"   Best model: {data['models'][0].get('model')}")
                    print(f"   Status: {data['summary'].get('overall_fit_status')}")
            else:
                print(f"❌ Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
        else:
            print("❌ No CSV content from generate-dataset")
    else:
        print(f"❌ Failed to generate test dataset")
        
except requests.exceptions.Timeout:
    print("⏱️ Training timed out (expected for large datasets)")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 4: Check API docs
print("\n4️⃣ Checking API documentation...")
try:
    response = requests.get("http://localhost:8000/docs", timeout=(5, 30))
    if response.status_code == 200:
        print(f"✅ API docs available at http://localhost:8000/docs")
    else:
        print(f"⚠️ API docs returned {response.status_code}")
except Exception as e:
    print(f"⚠️ Could not access docs: {str(e)}")

print("\n" + "="*60)
print("✅ Backend health check complete!")
print("="*60)
print("\nIf all tests passed, the backend is working correctly.")
print("If any test failed, check the error messages above.")
