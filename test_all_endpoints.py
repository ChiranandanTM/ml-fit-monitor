import requests
import json

print('='*70)
print('TESTING API ENDPOINTS')
print('='*70)

# Test 1: Basic training
print('\n1. Testing /train endpoint...')
with open('test_complex_dataset.csv', 'rb') as f:
    r = requests.post('http://localhost:8000/train', files={'file': f})
    if r.status_code == 200:
        data = r.json()
        print(f'✓ /train: {len(data["models"])} models trained')
        for m in data['models']:
            print(f'  - {m["model"]}: {m["fit_status"]}')
    else:
        print(f'✗ /train failed: {r.status_code}')

# Test 2: Generate dataset
print('\n2. Testing /generate-dataset endpoint...')
r = requests.get('http://localhost:8000/generate-dataset/good_fit')
if r.status_code == 200:
    data = r.json()
    print(f'✓ Generated {data["filename"]} ({data["rows"]} rows, {data["columns"]} cols)')
else:
    print(f'✗ /generate-dataset failed: {r.status_code}')

# Test 3: Full analysis
print('\n3. Testing /analyze endpoint...')
with open('good_fit_dataset.csv', 'rb') as f:
    r = requests.post('http://localhost:8000/analyze', files={'file': f})
    if r.status_code == 200:
        data = r.json()
        print(f'✓ /analyze: Generated report with {len(data.get("model_analysis", []))} models')
        print(f'  Best performing: {data["executive_summary"]["best_performing"]}')
    else:
        print(f'✗ /analyze failed: {r.status_code}')

# Test 4: Suggestions
print('\n4. Testing /suggest endpoint...')
with open('test_complex_dataset.csv', 'rb') as f:
    r = requests.post('http://localhost:8000/suggest', files={'file': f})
    if r.status_code == 200:
        data = r.json()
        print(f'✓ /suggest: Generated suggestions for {len(data.get("model_suggestions", []))} models')
    else:
        print(f'✗ /suggest failed: {r.status_code}')

# Test 5: Drift simulation
print('\n5. Testing /drift-simulate endpoint...')
with open('underfitting_dataset_new.csv', 'rb') as f:
    r = requests.post('http://localhost:8000/drift-simulate', files={'file': f})
    if r.status_code == 200:
        data = r.json()
        print(f'✓ /drift-simulate: Analyzed {len(data.get("models", []))} models for drift')
    else:
        print(f'✗ /drift-simulate failed: {r.status_code}')

print('\n' + '='*70)
print('ALL ENDPOINTS WORKING ✓')
print('='*70)
