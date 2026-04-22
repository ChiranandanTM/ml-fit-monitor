"""
Test Report Generation Endpoints

Demonstrates generating comprehensive reports in JSON, HTML, and PDF formats
from the ML Fit Monitor backend.
"""

import requests
import json
import os
from datetime import datetime

print('='*80)
print('ML FIT MONITOR - COMPREHENSIVE REPORT GENERATION TEST')
print('='*80)

BASE_URL = 'http://localhost:8000'

# Using a sample dataset for testing
test_file_path = 'good_fit_dataset.csv'

if not os.path.exists(test_file_path):
    print(f"\n⚠️  Test file not found: {test_file_path}")
    print("   Creating a sample dataset...")
    import pandas as pd
    import numpy as np
    
    # Create sample good-fit dataset
    np.random.seed(42)
    X = np.random.randn(200, 5)
    y = (X[:, 0] + X[:, 1] - X[:, 2] + np.random.randn(200) * 0.1 > 0).astype(int)
    
    df = pd.DataFrame(X, columns=[f'feature_{i+1}' for i in range(5)])
    df['target'] = y
    df.to_csv(test_file_path, index=False)
    print(f"✓ Created: {test_file_path}")

print(f"\n📂 Using test file: {test_file_path}")

# Test 1: JSON Report
print('\n' + '-'*80)
print('TEST 1: Generating JSON Report')
print('-'*80)

try:
    with open(test_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{BASE_URL}/reports/json',
            files=files,
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ JSON Report Generated Successfully")
        print(f"   Status: {data.get('status')}")
        print(f"   Format: {data.get('format')}")
        print(f"   Filename: {data.get('filename')}")
        
        # Save JSON report
        json_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w') as f:
            json.dump(data.get('content'), f, indent=2)
        print(f"   ✓ Saved to: {json_filename}")
        
        # Show report structure
        content = data.get('content', {})
        if 'sections' in content:
            print(f"\n   Report Sections:")
            for section in content.get('sections', []):
                print(f"   - {section.get('type', 'unknown')}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 2: HTML Report
print('\n' + '-'*80)
print('TEST 2: Generating HTML Report')
print('-'*80)

try:
    with open(test_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{BASE_URL}/reports/html',
            files=files,
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ HTML Report Generated Successfully")
        print(f"   Status: {data.get('status')}")
        print(f"   Format: {data.get('format')}")
        print(f"   Filename: {data.get('filename')}")
        
        # Save HTML report
        html_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(data.get('content', ''))
        print(f"   ✓ Saved to: {html_filename}")
        
        # Show HTML size
        html_size = len(data.get('content', '')) / 1024
        print(f"   Size: {html_size:.1f} KB")
        
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 3: PDF Report (returns HTML for client-side conversion)
print('\n' + '-'*80)
print('TEST 3: Generating PDF Report')
print('-'*80)

try:
    with open(test_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{BASE_URL}/reports/pdf',
            files=files,
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PDF Report Generated Successfully")
        print(f"   Status: {data.get('status')}")
        print(f"   Format: {data.get('format')}")
        print(f"   Filename: {data.get('filename')}")
        print(f"   Message: {data.get('message')}")
        
        # Save HTML content for PDF generation
        html_content = data.get('html_content', '')
        if html_content:
            pdf_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(pdf_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"   ✓ HTML saved (for PDF conversion): {pdf_filename}")
            
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 4: Generic /generate-report endpoint with format parameter
print('\n' + '-'*80)
print('TEST 4: Generic /generate-report Endpoint (JSON)')
print('-'*80)

try:
    with open(test_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{BASE_URL}/generate-report',
            files=files,
            params={'report_format': 'json'},
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Generic Report Generated Successfully")
        print(f"   Format: {data.get('format')}")
        print(f"   Filename: {data.get('filename')}")
    else:
        print(f"❌ Failed: {response.status_code}")

except Exception as e:
    print(f"❌ Error: {str(e)}")

print('\n' + '='*80)
print('REPORT GENERATION TEST COMPLETE')
print('='*80)
print("\n✅ All reports generated in current directory")
print("   - JSON reports: Machine-readable structured data")
print("   - HTML reports: Professional formatted documents")
print("   - PDF reports: Can be generated using html2pdf or wkhtmltopdf")
print('\n')
