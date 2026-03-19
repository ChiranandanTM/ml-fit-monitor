import requests
import json

# Test the generate dataset endpoint
response = requests.get('http://localhost:8000/generate-dataset/good_fit')
print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Generated {data['fit_type'].replace('_', ' ')} dataset")
    print(f"   Filename: {data['filename']}")
    print(f"   Rows: {data['rows']}")
    print(f"   Columns: {data['columns']}")
    print(f"\n First few lines of CSV:")
    print('\n'.join(data['csv'].split('\n')[:5]))
else:
    print("Error:", response.text)
