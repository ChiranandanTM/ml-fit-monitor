"""
Comprehensive Report Generator for ML Model Analysis
Generates JSON, HTML, and PDF reports with model evaluation results.
"""
import json
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any


class ReportGenerator:
    """Generates comprehensive ML model analysis reports in multiple formats."""
    
    def __init__(self, project_name: str = "ML Analysis", dataset_name: str = "dataset"):
        """
        Initialize the report generator.
        
        Args:
            project_name: Name of the project
            dataset_name: Name of the dataset being analyzed
        """
        self.project_name = project_name
        self.dataset_name = dataset_name
        self.timestamp = datetime.now().isoformat()
        self.sections = {}
        self.executive_summary = None
        self.models_data = []
        self.feature_importance_data = []
        self.data_quality_data = None
        self.recommendations_data = []
    
    def add_executive_summary(self, num_samples: int, num_features: int, best_model: str,
                             best_score: float, fit_status: str, data_quality_score: float,
                             task_type: str) -> None:
        """
        Add executive summary section to the report.
        
        Args:
            num_samples: Number of samples in dataset
            num_features: Number of features
            best_model: Name of best performing model
            best_score: Score of best model
            fit_status: Model fit status (Good Fit, Overfitting, Underfitting, etc.)
            data_quality_score: Data quality score (0-100)
            task_type: Type of task (classification, regression)
        """
        self.executive_summary = {
            "num_samples": num_samples,
            "num_features": num_features,
            "best_model": best_model,
            "best_score": best_score,
            "fit_status": fit_status,
            "data_quality_score": data_quality_score,
            "task_type": task_type
        }
    
    def add_model_performance_section(self, models: List[Dict[str, Any]]) -> None:
        """
        Add model performance section with multiple model results.
        
        Args:
            models: List of model performance dictionaries
        """
        self.models_data = models
    
    def add_feature_importance_section(self, feature_importance: List[Dict[str, Any]]) -> None:
        """
        Add feature importance analysis section.
        
        Args:
            feature_importance: List of features with importance scores
        """
        self.feature_importance_data = feature_importance
    
    def add_data_quality_section(self, data_profile: Dict[str, Any], 
                                quality_summary: Dict[str, Any]) -> None:
        """
        Add data quality analysis section.
        
        Args:
            data_profile: Detailed data profile information
            quality_summary: Summary of data quality metrics
        """
        self.data_quality_data = {
            "profile": data_profile,
            "summary": quality_summary
        }
    
    def add_recommendations_section(self, recommendations: List[Dict[str, str]], 
                                   fit_status: str) -> None:
        """
        Add recommendations section based on analysis results.
        
        Args:
            recommendations: List of recommended actions
            fit_status: Current fit status of the model
        """
        self.recommendations_data = {
            "fit_status": fit_status,
            "recommendations": recommendations
        }
    
    def generate_json_report(self) -> str:
        """
        Generate a comprehensive JSON report.
        
        Returns:
            JSON string containing the complete report
        """
        report_dict = {
            "metadata": {
                "project_name": self.project_name,
                "dataset_name": self.dataset_name,
                "generated_at": self.timestamp,
                "report_type": "comprehensive_analysis"
            },
            "executive_summary": self.executive_summary,
            "model_performance": self.models_data,
            "feature_importance": self.feature_importance_data,
            "data_quality": self.data_quality_data,
            "recommendations": self.recommendations_data
        }
        
        return json.dumps(report_dict, indent=2, default=str)
    
    def generate_html_report(self) -> str:
        """
        Generate a comprehensive HTML report.
        
        Returns:
            HTML string containing the complete report
        """
        html_parts = []
        
        # HTML Header
        html_parts.append("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ML Model Analysis Report</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }
                .header h1 {
                    margin: 0;
                    font-size: 28px;
                }
                .header p {
                    margin: 5px 0 0 0;
                    opacity: 0.9;
                }
                .section {
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .section h2 {
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 10px;
                    margin-top: 0;
                    color: #667eea;
                }
                .summary-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 15px;
                    margin: 15px 0;
                }
                .summary-card {
                    background: #f8f9fa;
                    padding: 15px;
                    border-left: 4px solid #667eea;
                    border-radius: 4px;
                }
                .summary-card strong {
                    display: block;
                    color: #667eea;
                    font-size: 12px;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                }
                .summary-card span {
                    font-size: 20px;
                    font-weight: bold;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background: #f8f9fa;
                    font-weight: 600;
                    color: #667eea;
                }
                tr:hover {
                    background: #f8f9fa;
                }
                .status-badge {
                    display: inline-block;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                }
                .status-good {
                    background: #d4edda;
                    color: #155724;
                }
                .status-warning {
                    background: #fff3cd;
                    color: #856404;
                }
                .status-danger {
                    background: #f8d7da;
                    color: #721c24;
                }
                .recommendation {
                    background: #e7f3ff;
                    border-left: 4px solid #2196F3;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 4px;
                }
                .recommendation strong {
                    color: #1565c0;
                    display: block;
                    margin-bottom: 5px;
                }
                .priority-high {
                    color: #d32f2f;
                }
                .priority-medium {
                    color: #f57c00;
                }
                .priority-low {
                    color: #388e3c;
                }
                .footer {
                    text-align: center;
                    padding: 20px;
                    color: #999;
                    font-size: 12px;
                    border-top: 1px solid #ddd;
                    margin-top: 30px;
                }
            </style>
        </head>
        <body>
        """)
        
        # Header Section
        html_parts.append(f"""
        <div class="header">
            <h1>{self.project_name}</h1>
            <p>Dataset: {self.dataset_name}</p>
            <p>Generated: {self.timestamp}</p>
        </div>
        """)
        
        # Executive Summary
        if self.executive_summary:
            summary = self.executive_summary
            status_class = self._get_status_class(summary.get("fit_status", ""))
            
            html_parts.append("""
            <div class="section">
                <h2>Executive Summary</h2>
                <div class="summary-grid">
            """)
            
            html_parts.append(f"""
                    <div class="summary-card">
                        <strong>Best Model</strong>
                        <span>{summary.get('best_model', 'N/A')}</span>
                    </div>
                    <div class="summary-card">
                        <strong>Best Score</strong>
                        <span>{summary.get('best_score', 0):.4f}</span>
                    </div>
                    <div class="summary-card">
                        <strong>Fit Status</strong>
                        <span><span class="status-badge {status_class}">{summary.get('fit_status', 'Unknown')}</span></span>
                    </div>
                    <div class="summary-card">
                        <strong>Data Quality</strong>
                        <span>{summary.get('data_quality_score', 0):.1f}%</span>
                    </div>
                    <div class="summary-card">
                        <strong>Samples</strong>
                        <span>{summary.get('num_samples', 0):,}</span>
                    </div>
                    <div class="summary-card">
                        <strong>Features</strong>
                        <span>{summary.get('num_features', 0)}</span>
                    </div>
            """)
            
            html_parts.append("</div></div>")
        
        # Model Performance
        if self.models_data:
            html_parts.append("""
            <div class="section">
                <h2>Model Performance Comparison</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Score</th>
                            <th>Train Time</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
            """)
            
            for model in self.models_data[:10]:  # Limit to 10 models
                score = model.get("score", 0)
                train_time = model.get("train_time", "N/A")
                html_parts.append(f"""
                        <tr>
                            <td>{model.get('name', 'Unknown')}</td>
                            <td>{score:.4f}</td>
                            <td>{train_time}</td>
                            <td>{model.get('status', 'N/A')}</td>
                        </tr>
                """)
            
            html_parts.append("</tbody></table></div>")
        
        # Feature Importance
        if self.feature_importance_data:
            html_parts.append("""
            <div class="section">
                <h2>Feature Importance Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th>Importance Score</th>
                            <th>Rank</th>
                        </tr>
                    </thead>
                    <tbody>
            """)
            
            for idx, feature in enumerate(self.feature_importance_data[:15], 1):  # Top 15
                name = feature.get("name", f"Feature {idx}")
                importance = feature.get("importance", 0)
                html_parts.append(f"""
                        <tr>
                            <td>{name}</td>
                            <td>{importance:.4f}</td>
                            <td>#{idx}</td>
                        </tr>
                """)
            
            html_parts.append("</tbody></table></div>")
        
        # Data Quality
        if self.data_quality_data:
            summary = self.data_quality_data.get("summary", {})
            html_parts.append(f"""
            <div class="section">
                <h2>Data Quality Assessment</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <strong>Quality Grade</strong>
                        <span>{summary.get('quality_grade', 'N/A')}</span>
                    </div>
                    <div class="summary-card">
                        <strong>Overall Quality</strong>
                        <span>{summary.get('overall_quality', 0):.1f}%</span>
                    </div>
                    <div class="summary-card">
                        <strong>Total Issues</strong>
                        <span>{summary.get('total_issues', 0)}</span>
                    </div>
                    <div class="summary-card">
                        <strong>Missing Values</strong>
                        <span>{summary.get('missing_values_count', 0)}</span>
                    </div>
                </div>
                <p><strong>Recommendation:</strong> {summary.get('recommendation', 'N/A')}</p>
            </div>
            """)
        
        # Recommendations
        if self.recommendations_data and self.recommendations_data.get("recommendations"):
            html_parts.append("""
            <div class="section">
                <h2>Recommendations</h2>
            """)
            
            for rec in self.recommendations_data["recommendations"]:
                priority = rec.get("priority", "MEDIUM").upper()
                priority_class = f"priority-{priority.lower()}"
                html_parts.append(f"""
                <div class="recommendation">
                    <strong>{rec.get('action', 'Action')}</strong>
                    <span class="{priority_class}">Priority: {priority}</span>
                    <p>{rec.get('details', '')}</p>
                </div>
                """)
            
            html_parts.append("</div>")
        
        # Footer
        html_parts.append("""
        <div class="footer">
            <p>ML Model Quality Decision-Support System</p>
            <p>This report was automatically generated by the ML Fit Monitor.</p>
        </div>
        </body>
        </html>
        """)
        
        return "\n".join(html_parts)
    
    def _get_status_class(self, status: str) -> str:
        """Get CSS class for status badge."""
        status_lower = status.lower()
        if "good" in status_lower or "excellent" in status_lower:
            return "status-good"
        elif "overfitting" in status_lower or "warning" in status_lower:
            return "status-warning"
        elif "underfitting" in status_lower or "error" in status_lower or "failure" in status_lower:
            return "status-danger"
        else:
            return "status-warning"
