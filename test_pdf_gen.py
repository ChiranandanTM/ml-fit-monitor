import requests
import json

data = {
    'summary': {
        'best_model': 'Random Forest',
        'overall_fit_status': 'Good Fit',
        'val_score': 0.92,
        'gap': 0.05
    },
    'models': [{
        'model': 'Random Forest',
        'train_score': 0.97,
        'val_score': 0.92,
        'gap': 0.05,
        'fit_status': 'Good'
    }],
    'feature_importance': [
        {'name': 'Feature1', 'importance': 0.35},
        {'name': 'Feature2', 'importance': 0.28}
    ],
    'confusion_matrix': [[68, 12], [8, 62]],
    'recommendations': ['Good generalization', 'Monitor metrics']
}

response = requests.post('http://localhost:9000/reports/advanced-pdf', json=data)
if response.status_code == 200:
    with open('test_pdf.pdf', 'wb') as f:
        f.write(response.content)
    print(f'✓ PDF saved! Size: {len(response.content)} bytes')
else:
    print(f'✗ Error: {response.status_code}')
    print(response.text)
