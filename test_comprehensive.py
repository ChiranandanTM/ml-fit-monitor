import requests
import json
import time

print('\n' + '='*80)
print('COMPREHENSIVE END-TO-END SYSTEM TEST')
print('='*80)

BASE_URL = 'http://localhost:8000'

# Test datasets
test_files = {
    'good_fit': 'good_fit_dataset.csv',
    'complex': 'test_complex_dataset.csv',
    'underfit': 'underfitting_dataset_new.csv'
}

def test_mode(mode_name, endpoint, filename):
    """Test a specific analysis mode"""
    print(f'\n📊 Testing {mode_name.upper()} mode ({endpoint})...')
    start = time.time()
    
    try:
        with open(filename, 'rb') as f:
            response = requests.post(f'{BASE_URL}{endpoint}', files={'file': f})
        
        if response.status_code != 200:
            print(f'  ✗ FAILED: Status {response.status_code}')
            return False
        
        data = response.json()
        elapsed = time.time() - start
        
        # Verify response structure
        if 'error' in data:
            print(f'  ✗ ERROR: {data["error"]}')
            return False
        
        # Check different response formats
        if '/train' in endpoint and 'models' in data:
            print(f'  ✓ {len(data["models"])} models trained in {elapsed:.1f}s')
            for model in data['models']:
                status = model.get('fit_status', 'ERROR')
                train = model.get('train_score', 0)
                val = model.get('val_score', 0)
                print(f'    - {model["model"]:25} | {status:15} | Train: {train:.2f} | Val: {val:.2f}')
            return True
        
        elif '/analyze' in endpoint and 'executive_summary' in data:
            print(f'  ✓ Analysis complete in {elapsed:.1f}s')
            print(f'    - Best model: {data["executive_summary"].get("best_performing", "N/A")}')
            print(f'    - Models analyzed: {len(data.get("model_analysis", []))}')
            print(f'    - Suggestions: {len(data.get("suggestions", []))}')
            return True
        
        elif '/suggest' in endpoint and 'model_suggestions' in data:
            print(f'  ✓ Suggestions generated in {elapsed:.1f}s')
            print(f'    - {len(data["model_suggestions"])} models with recommendations')
            return True
        
        elif '/drift-simulate' in endpoint and 'models' in data:
            print(f'  ✓ Drift simulation complete in {elapsed:.1f}s')
            print(f'    - {len(data["models"])} models analyzed')
            for model in data['models']:
                urgency = model.get('retraining_urgency', 'UNKNOWN')
                print(f'    - {model["model_name"]}: {urgency}')
            return True
        
        else:
            print(f'  ⚠ Unexpected response format')
            return False
            
    except Exception as e:
        print(f'  ✗ EXCEPTION: {str(e)}')
        return False

# Run comprehensive tests
print('\n' + '-'*80)
print('TEST SUITE 1: Basic Training Mode')
print('-'*80)
results = []

results.append(('Basic Training (good_fit)', test_mode('Basic Training', '/train', test_files['good_fit'])))
results.append(('Basic Training (complex)', test_mode('Basic Training', '/train', test_files['complex'])))
results.append(('Basic Training (underfit)', test_mode('Basic Training', '/train', test_files['underfit'])))

print('\n' + '-'*80)
print('TEST SUITE 2: Full Analysis Mode')
print('-'*80)

results.append(('Full Analysis (good_fit)', test_mode('Full Analysis', '/analyze', test_files['good_fit'])))

print('\n' + '-'*80)
print('TEST SUITE 3: Suggestions Mode')
print('-'*80)

results.append(('Suggestions (complex)', test_mode('Suggestions', '/suggest', test_files['complex'])))
results.append(('Suggestions (underfit)', test_mode('Suggestions', '/suggest', test_files['underfit'])))

print('\n' + '-'*80)
print('TEST SUITE 4: Drift Simulation Mode')
print('-'*80)

results.append(('Drift Simulation', test_mode('Drift Simulation', '/drift-simulate', test_files['complex'])))

# Summary
print('\n' + '='*80)
print('TEST SUMMARY')
print('='*80)

passed = sum(1 for _, result in results if result)
total = len(results)

for test_name, result in results:
    status = '✓ PASS' if result else '✗ FAIL'
    print(f'  {status}: {test_name}')

print(f'\n  Total: {passed}/{total} tests passed')

if passed == total:
    print('\n🎉 ALL TESTS PASSED - SYSTEM IS FULLY FUNCTIONAL! 🎉')
else:
    print(f'\n⚠️  {total - passed} tests failed - check API responses')

print('='*80)
