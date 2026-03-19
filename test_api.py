import requests
import json

with open('test_complex_dataset.csv', 'rb') as f:
    files = {'file': ('test_complex_dataset.csv', f, 'text/csv')}
    response = requests.post('http://localhost:8000/train', files=files)
    
print('Status Code:', response.status_code)
result = response.json()
print(f'\nTask Type: {result["task_type"]}')
print('\nModel Results:')
for model in result['models']:
    print(f"  {model['model']:20} | Fit: {model['fit_status']:15} | Train: {model['train_score']:.2f} | Val: {model['val_score']:.2f}")
