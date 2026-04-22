"""
Module: PDF Report Generator

Generate professional reports in multiple formats:
- JSON: Structured data export
- HTML: Interactive formatted report
- PDF: Professional PDF document
"""

from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any, Optional
import base64
import json
import os


class ReportGenerator:
    """Generate professional analysis reports in multiple formats."""
    
    def __init__(self, project_name: str = "ML Fit Monitor Analysis", dataset_name: str = "Dataset"):
        """
        Initialize report builder.
        
        Parameters:
        -----------
        project_name : str
            Name of the analysis project
        dataset_name : str
            Name of the dataset
        """
        self.project_name = project_name
        self.dataset_name = dataset_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sections = []
    
    def add_executive_summary(
        self,
        num_samples: int,
        num_features: int,
        best_model: str,
        best_score: float,
        fit_status: str,
        data_quality_score: float,
        task_type: str = "classification"
    ) -> 'ReportGenerator':
        """Add executive summary section."""
        
        summary = {
            'type': 'executive_summary',
            'dataset_name': self.dataset_name,
            'samples': num_samples,
            'features': num_features,
            'best_model': best_model,
            'best_score': float(best_score),
            'fit_status': fit_status,
            'data_quality': float(data_quality_score),
            'task_type': task_type,
            'timestamp': self.timestamp
        }
        
        self.sections.append(summary)
        return self
    
    def add_model_performance_section(
        self,
        models: List[Dict[str, Any]]
    ) -> 'ReportGenerator':
        """Add model performance comparison section."""
        
        section = {
            'type': 'model_performance',
            'title': 'Model Performance Comparison',
            'models': models
        }
        
        self.sections.append(section)
        return self
    
    def add_feature_importance_section(
        self,
        features: List[Dict[str, Any]]
    ) -> 'ReportGenerator':
        """Add feature importance analysis section."""
        
        section = {
            'type': 'feature_importance',
            'title': 'Feature Importance Analysis',
            'features': features
        }
        
        self.sections.append(section)
        return self
    
    def add_data_quality_section(
        self,
        profile: Dict[str, Any],
        quality_summary: Dict[str, Any]
    ) -> 'ReportGenerator':
        """Add data quality profile section."""
        
        section = {
            'type': 'data_quality',
            'title': 'Data Quality Assessment',
            'profile': profile,
            'summary': quality_summary
        }
        
        self.sections.append(section)
        return self
    
    def add_recommendations_section(
        self,
        recommendations: List[Dict[str, str]],
        fit_status: str
    ) -> 'ReportGenerator':
        """Add actionable recommendations section."""
        
        section = {
            'type': 'recommendations',
            'title': 'Recommendations & Action Items',
            'fit_status': fit_status,
            'recommendations': recommendations
        }
        
        self.sections.append(section)
        return self
    
    def add_roc_analysis_section(
        self,
        roc_data: List[Dict[str, Any]]
    ) -> 'ReportGenerator':
        """Add ROC curve analysis section."""
        
        section = {
            'type': 'roc_analysis',
            'title': 'Classification Metrics by Model',
            'models': roc_data
        }
        
        self.sections.append(section)
        return self
    
    def add_drift_analysis_section(
        self,
        drift_analysis: Dict[str, Any]
    ) -> 'ReportGenerator':
        """Add drift analysis section."""
        
        section = {
            'type': 'drift_analysis',
            'title': 'Data Drift Analysis',
            'analysis': drift_analysis
        }
        
        self.sections.append(section)
        return self
    
    def get_report_dict(self) -> Dict:
        """Get report as dictionary."""
        return {
            'project_name': self.project_name,
            'dataset_name': self.dataset_name,
            'timestamp': self.timestamp,
            'sections': self.sections
        }
    
    def generate_json_report(self) -> str:
        """
        Generate JSON version of report.
        
        Returns:
        --------
        str : JSON report content
        """
        return json.dumps(self.get_report_dict(), indent=2)
    
    def generate_html_report(self) -> str:
        """
        Generate comprehensive HTML version of report.
        
        Returns:
        --------
        str : HTML report content
        """
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '<title>ML Fit Monitor - Analysis Report</title>',
            '<style>',
            self._get_css_styles(),
            '</style>',
            '</head>',
            '<body>',
            self._render_header(),
        ]
        
        # Add sections
        for section in self.sections:
            if section['type'] == 'executive_summary':
                html_parts.append(self._render_executive_summary_html(section))
            elif section['type'] == 'model_performance':
                html_parts.append(self._render_performance_html(section))
            elif section['type'] == 'feature_importance':
                html_parts.append(self._render_feature_importance_html(section))
            elif section['type'] == 'data_quality':
                html_parts.append(self._render_data_quality_html(section))
            elif section['type'] == 'recommendations':
                html_parts.append(self._render_recommendations_html(section))
            elif section['type'] == 'roc_analysis':
                html_parts.append(self._render_roc_analysis_html(section))
            elif section['type'] == 'drift_analysis':
                html_parts.append(self._render_drift_analysis_html(section))
        
        html_parts.extend([
            self._render_footer(),
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_parts)
    
    def _get_css_styles(self) -> str:
        """Get comprehensive CSS styles."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .section {
            background: #fff;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .section h2 {
            color: #1e293b;
            font-size: 22px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            text-align: center;
        }
        .metric-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #1e293b;
        }
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-good {
            background: #d1fae5;
            color: #065f46;
        }
        .status-warning {
            background: #fef3c7;
            color: #92400e;
        }
        .status-critical {
            background: #fee2e2;
            color: #7f1d1d;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 14px;
        }
        .table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        .table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e5e7eb;
        }
        .table tbody tr:hover {
            background: #f9fafb;
        }
        .table tbody tr:nth-child(even) {
            background: #f3f4f6;
        }
        .recommendation-item {
            background: #f0f9ff;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #3b82f6;
            border-radius: 4px;
        }
        .recommendation-priority {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 10px;
        }
        .priority-high {
            background: #fee2e2;
            color: #7f1d1d;
        }
        .priority-medium {
            background: #fef3c7;
            color: #92400e;
        }
        .priority-low {
            background: #d1fae5;
            color: #065f46;
        }
        .footer {
            background: #f9fafb;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #e5e7eb;
        }
        .bar-chart {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            align-items: flex-end;
            height: 150px;
        }
        .bar {
            flex: 1;
            background: linear-gradient(to top, #667eea, #764ba2);
            border-radius: 4px 4px 0 0;
            min-height: 30px;
            position: relative;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: bold;
        }
        """
    
    def _render_header(self) -> str:
        """Render report header."""
        return f"""
        <div class="container">
        <div class="header">
            <h1>🚀 ML Fit Monitor</h1>
            <h2>{self.project_name}</h2>
            <p>Dataset: <strong>{self.dataset_name}</strong> | Generated: {self.timestamp}</p>
        </div>
        <div class="content">
        """
    
    def _render_footer(self) -> str:
        """Render report footer."""
        return """
        </div>
        <div class="footer">
            <p><strong>ML Fit Monitor</strong> - Advanced Model Quality Intelligence Platform</p>
            <p>© 2026 All Rights Reserved | Precision Machine Learning Analysis</p>
        </div>
        </div>
        """
    
    def _render_executive_summary_html(self, section: Dict) -> str:
        """Render executive summary HTML."""
        fit_status = section['fit_status']
        status_class = 'status-good' if 'Good' in fit_status else ('status-warning' if 'Under' in fit_status else 'status-critical')
        
        return f"""
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Samples</div>
                    <div class="metric-value">{section['samples']:,}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Features</div>
                    <div class="metric-value">{section['features']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Best Model Performance</div>
                    <div class="metric-value">{section['best_score']:.2%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Data Quality Score</div>
                    <div class="metric-value">{section['data_quality']:.1f}/100</div>
                </div>
            </div>
            <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin-top: 20px;">
                <p><strong>Best Performing Model:</strong> <span style="color: #667eea; font-size: 18px;">{section['best_model']}</span></p>
                <p style="margin-top: 10px;"><strong>Fit Status:</strong> 
                    <span class="status-badge {status_class}">{fit_status}</span>
                </p>
                <p style="margin-top: 10px;"><strong>Task Type:</strong> {section['task_type'].title()}</p>
            </div>
        </div>
        """
    
    def _render_performance_html(self, section: Dict) -> str:
        """Render model performance HTML."""
        rows = []
        for model in section['models']:
            status_val = model.get('fit_status', 'Unknown')
            status_class = 'status-good' if 'Good' in status_val else ('status-warning' if 'Under' in status_val else 'status-critical')
            
            rows.append(f"""
            <tr>
                <td><strong>{model['model']}</strong></td>
                <td>{model.get('train_score', 0):.4f}</td>
                <td>{model.get('val_score', 0):.4f}</td>
                <td>{model.get('gap', 0):.4f}</td>
                <td><span class="status-badge {status_class}">{status_val}</span></td>
            </tr>
            """)
        
        return f"""
        <div class="section">
            <h2>📈 {section['title']}</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Model Name</th>
                        <th>Train Score</th>
                        <th>Validation Score</th>
                        <th>Generalization Gap</th>
                        <th>Fit Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """
    
    def _render_feature_importance_html(self, section: Dict) -> str:
        """Render feature importance HTML."""
        if not section.get('features'):
            return '<div class="section"><h2>🔍 Feature Importance Analysis</h2><p>No feature importance data available.</p></div>'
        
        features = section['features'][:10]  # Top 10 features
        max_importance = max([f.get('importance', 0) for f in features]) if features else 1
        
        rows = []
        for i, feat in enumerate(features, 1):
            importance = feat.get('importance', 0)
            width = (importance / max_importance * 100) if max_importance > 0 else 0
            rows.append(f"""
            <tr>
                <td>{i}.</td>
                <td><strong>{feat.get('name', 'Feature')}</strong></td>
                <td>
                    <div style="background: #e5e7eb; border-radius: 4px; height: 20px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {width}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold;">
                            {importance:.4f}
                        </div>
                    </div>
                </td>
            </tr>
            """)
        
        return f"""
        <div class="section">
            <h2>🔍 {section['title']}</h2>
            <p>Top features that contribute most to model predictions:</p>
            <table class="table" style="margin-top: 15px;">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Feature Name</th>
                        <th>Importance Score</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """
    
    def _render_data_quality_html(self, section: Dict) -> str:
        """Render data quality HTML."""
        summary = section['summary']
        grade = summary.get('quality_grade', 'B')
        grade_color = {'A': '#10b981', 'B': '#3b82f6', 'C': '#f59e0b', 'D': '#ef4444'}.get(grade[0], '#3b82f6')
        
        return f"""
        <div class="section">
            <h2>✅ {section['title']}</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Quality Grade</div>
                    <div class="metric-value" style="color: {grade_color}; font-size: 36px;">{grade}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Overall Quality Score</div>
                    <div class="metric-value">{summary.get('overall_quality', 0):.1f}/100</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Issues Found</div>
                    <div class="metric-value">{summary.get('total_issues', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Missing Values</div>
                    <div class="metric-value">{summary.get('missing_values_count', 0)}</div>
                </div>
            </div>
            <p style="margin-top: 20px;"><strong>Recommendation:</strong> {summary.get('recommendation', 'Continue with current data')}</p>
        </div>
        """
    
    def _render_recommendations_html(self, section: Dict) -> str:
        """Render recommendations HTML."""
        recs = section.get('recommendations', [])
        if not recs:
            return '<div class="section"><h2>💡 Recommendations</h2><p>No recommendations available.</p></div>'
        
        rec_items = []
        for rec in recs:
            priority = rec.get('priority', 'MEDIUM')
            priority_class = f'priority-{priority.lower()}'
            rec_items.append(f"""
            <div class="recommendation-item">
                <span class="recommendation-priority {priority_class}">{priority}</span>
                <strong>{rec.get('action', 'Action')}</strong>
                <p style="margin-top: 8px; color: #555;">{rec.get('details', '')}</p>
            </div>
            """)
        
        return f"""
        <div class="section">
            <h2>💡 {section['title']}</h2>
            <p><strong>Current Status:</strong> <span class="status-badge {'status-good' if 'Good' in section['fit_status'] else 'status-warning'}">{section['fit_status']}</span></p>
            {''.join(rec_items)}
        </div>
        """
    
    def _render_roc_analysis_html(self, section: Dict) -> str:
        """Render ROC analysis HTML."""
        models = section.get('models', [])
        if not models:
            return '<div class="section"><h2>📊 Classification Metrics by Model</h2><p>No ROC analysis data available.</p></div>'
        
        rows = []
        for model in models:
            rows.append(f"""
            <tr>
                <td><strong>{model.get('model_name', 'Model')}</strong></td>
                <td>{model.get('roc_auc', 0):.4f}</td>
                <td>{model.get('accuracy', 0):.4f}</td>
                <td>{model.get('precision', 0):.4f}</td>
                <td>{model.get('recall', 0):.4f}</td>
                <td>{model.get('f1_score', 0):.4f}</td>
            </tr>
            """)
        
        return f"""
        <div class="section">
            <h2>📊 {section['title']}</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>ROC AUC</th>
                        <th>Accuracy</th>
                        <th>Precision</th>
                        <th>Recall</th>
                        <th>F1-Score</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """
    
    def _render_drift_analysis_html(self, section: Dict) -> str:
        """Render drift analysis HTML."""
        return f"""
        <div class="section">
            <h2>📡 {section['title']}</h2>
            <p>Drift analysis helps detect changes in data distribution over time.</p>
        </div>
        """


# Backward compatibility
class PDFReportGenerator(ReportGenerator):
    """Legacy alias for ReportGenerator."""
    pass

