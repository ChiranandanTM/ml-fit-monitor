"""
Backend test with extended timeouts and better error handling
"""
import requests
import json
import time
from urllib3.exceptions import ReadTimeoutError

print("="*60)
print("ML FIT MONITOR - Backend Health Check (Extended Timeouts)")
print("="*60)

# Use session with longer timeout
session = requests.Session()

def test_endpoint(name, method, url, **kwargs):
    """Test an endpoint with extended timeout"""
    print(f"\n{name}...")
    try:
        # Extended timeout: 5 seconds connection, 60 seconds read
        timeout = kwargs.pop('timeout', (5, 60))
        
        print(f"  URL: {url}")
        print(f"  Timeout: {timeout}s")
        
        start = time.time()
        
        if method == "GET":
            response = session.get(url, timeout=timeout, **kwargs)
        else:
            response = session.post(url, timeout=timeout, **kwargs)
        
        elapsed = time.time() - start
        
        print(f"  ✅ Status: {response.status_code}")
        print(f"  ⏱️  Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            try:
                data = response.json()
                return True, data
            except:
                return True, response.text
        else:
            return False, response.text
            
    except requests.exceptions.Timeout as e:
        print(f"  ❌ Timeout Error: {e}")
        return False, str(e)
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ Connection Error: {e}")
        return False, str(e)
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}")
        return False, str(e)

# Test 1: Root endpoint
success, response = test_endpoint("1️⃣ Testing root endpoint", "GET", "http://localhost:8000/")
if success and isinstance(response, dict):
    print(f"  Message: {response.get('message')}")

# Test 2: Docs
success, response = test_endpoint("2️⃣ Testing /docs endpoint", "GET", "http://localhost:8000/docs")
if success:
    print(f"  Content length: {len(response)} bytes")

# Test 3: Generate dataset
success, response = test_endpoint("3️⃣ Testing /generate-dataset", "GET", "http://localhost:8000/generate-dataset/good_fit")
if success and isinstance(response, dict):
    print(f"  Shape: {response.get('rows')} x {response.get('columns')}")

print("\n" + "="*60)
print("✅ Backend health check complete!")
print("="*60)
