"""
ML Fit Monitor - Report Generator Client

Easy-to-use Python client for generating reports from the ML Fit Monitor backend.
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal, Dict, Optional


class MLFitMonitorReportClient:
    """Client for generating ML Fit Monitor analysis reports."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the report client.
        
        Args:
            base_url: Backend URL (default: http://localhost:8000)
        """
        self.base_url = base_url
        self.timeout = 120
    
    def generate_report(
        self,
        file_path: str,
        report_format: Literal['json', 'html', 'pdf'] = 'html',
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Generate a report from uploaded dataset.
        
        Args:
            file_path: Path to dataset file (.csv or .xlsx)
            report_format: Report format ('json', 'html', or 'pdf')
            output_dir: Directory to save report (default: current directory)
        
        Returns:
            Dictionary with report data
        
        Raises:
            FileNotFoundError: If dataset file not found
            requests.Exception: If API call fails
        """
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"📂 Loading dataset: {file_path}")
        print(f"📄 Generating {report_format.upper()} report...")
        
        # Call API
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/reports/{report_format}",
                files=files,
                timeout=self.timeout
            )
        
        if response.status_code != 200:
            raise requests.HTTPError(
                f"Failed to generate report: {response.status_code} - {response.text}"
            )
        
        data = response.json()
        
        # Save report
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = '.'
        
        filename = data.get('filename', f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{report_format}')
        filepath = os.path.join(output_dir, filename)
        
        if report_format in ['json', 'html']:
            content = str(data.get('content', ''))
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif report_format == 'pdf':
            html_content = data.get('html_content', '')
            html_filepath = filepath.replace('.pdf', '.html')
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"   💾 Saved HTML (for PDF conversion): {html_filepath}")
        
        print(f"✅ Report generated: {filepath}")
        
        return {
            'status': 'success',
            'format': report_format,
            'filepath': filepath,
            'data': data
        }
    
    def generate_all_formats(
        self,
        file_path: str,
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Generate reports in all formats (JSON, HTML, PDF).
        
        Args:
            file_path: Path to dataset file
            output_dir: Directory to save reports
        
        Returns:
            Dictionary with all generated reports
        """
        
        results = {
            'json': None,
            'html': None,
            'pdf': None
        }
        
        for fmt in ['json', 'html', 'pdf']:
            try:
                result = self.generate_report(file_path, fmt, output_dir)
                results[fmt] = result
            except Exception as e:
                print(f"❌ Failed to generate {fmt} report: {str(e)}")
                results[fmt] = {'status': 'failed', 'error': str(e)}
        
        return results
    
    def health_check(self) -> bool:
        """Check if backend is running."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False


def main():
    """Example usage of the report client."""
    
    # Initialize client
    client = MLFitMonitorReportClient()
    
    # Check backend
    print("🔍 Checking backend status...")
    if not client.health_check():
        print("❌ Backend is not running!")
        print("   Start the backend with: uvicorn app.main:app --reload")
        return
    
    print("✅ Backend is running\n")
    
    # Create sample dataset if needed
    dataset_file = 'sample_dataset.csv'
    if not os.path.exists(dataset_file):
        print(f"📊 Creating sample dataset: {dataset_file}")
        import pandas as pd
        import numpy as np
        
        np.random.seed(42)
        X = np.random.randn(300, 8)
        y = (X[:, 0] + X[:, 1] - X[:, 2] > 0).astype(int)
        
        df = pd.DataFrame(X, columns=[f'feature_{i+1}' for i in range(8)])
        df['target'] = y
        df.to_csv(dataset_file, index=False)
        print(f"   ✓ Created {dataset_file}\n")
    
    # Generate reports
    print("="*80)
    print("GENERATING COMPREHENSIVE REPORTS")
    print("="*80 + "\n")
    
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)
    
    # Option 1: Generate individual reports
    print("📋 Generating JSON report...")
    try:
        json_result = client.generate_report(dataset_file, 'json', output_dir)
        print(f"   ✓ Size: {len(str(json_result['data']['content'])) / 1024:.1f} KB\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("📋 Generating HTML report...")
    try:
        html_result = client.generate_report(dataset_file, 'html', output_dir)
        print(f"   ✓ Size: {len(str(html_result['data']['content'])) / 1024:.1f} KB\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("📋 Generating PDF report...")
    try:
        pdf_result = client.generate_report(dataset_file, 'pdf', output_dir)
        print(f"   ✓ HTML content ready for conversion\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Option 2: Generate all formats at once
    # print("📋 Generating all report formats...")
    # all_results = client.generate_all_formats(dataset_file, output_dir)
    # print(f"✅ Generated {len([r for r in all_results.values() if r['status'] == 'success'])} reports\n")
    
    print("="*80)
    print("✅ Report generation complete!")
    print("="*80)
    print(f"\n📂 Reports saved to: {output_dir}/")
    print("   - JSON reports for data analysis")
    print("   - HTML reports for viewing/printing")
    print("   - PDF-ready HTML for conversion")


if __name__ == '__main__':
    main()
