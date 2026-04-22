"""Charts-focused PDF generator with working image embedding"""
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import tempfile
import os


class ChartsPDFReportGenerator:
    def __init__(self):
        self.width = letter[0]
        self.height = letter[1]
        self.temp_files = []
    
    def _safe_str(self, value):
        """Convert to safe ASCII string"""
        if value is None:
            return "N/A"
        s = str(value)
        s = ''.join(c for c in s if ord(c) < 128)
        return s.strip()[:150]
    
    def _save_roc_chart(self, fpr, tpr, auc_score):
        """Generate and save ROC curve"""
        try:
            fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
            
            # Ensure data is list/array
            fpr = list(fpr) if not isinstance(fpr, list) else fpr
            tpr = list(tpr) if not isinstance(tpr, list) else tpr
            auc_score = float(auc_score)
            
            ax.plot(fpr, tpr, color='#1e40af', lw=3, label=f'ROC Curve (AUC = {auc_score:.3f})')
            ax.plot([0, 1], [0, 1], color='grey', lw=2, linestyle='--', label='Random Classifier')
            
            ax.set_xlim([-0.02, 1.02])
            ax.set_ylim([-0.02, 1.05])
            ax.set_xlabel('False Positive Rate', fontsize=11, fontweight='bold')
            ax.set_ylabel('True Positive Rate', fontsize=11, fontweight='bold')
            ax.set_title('ROC Curve Analysis', fontsize=13, fontweight='bold', pad=15)
            ax.legend(loc="lower right", fontsize=10)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')
            
            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            plt.savefig(temp_path, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            
            self.temp_files.append(temp_path)
            return temp_path
        except Exception as e:
            print(f"Error creating ROC chart: {e}")
            return None
    
    def _save_confusion_matrix_chart(self, cm):
        """Generate and save confusion matrix"""
        try:
            fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
            
            cm = np.array(cm, dtype=float)
            
            im = ax.imshow(cm, cmap='Blues', aspect='auto')
            
            labels = ['Negative', 'Positive']
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_xticklabels(labels, fontsize=11)
            ax.set_yticklabels(labels, fontsize=11)
            ax.set_ylabel('True Label', fontsize=11, fontweight='bold')
            ax.set_xlabel('Predicted Label', fontsize=11, fontweight='bold')
            ax.set_title('Confusion Matrix', fontsize=13, fontweight='bold', pad=15)
            
            # Add text annotations
            for i in range(2):
                for j in range(2):
                    val = int(cm[i][j])
                    ax.text(j, i, str(val), ha="center", va="center",
                           color="white" if cm[i][j] > cm.max()/2 else "black",
                           fontsize=14, fontweight='bold')
            
            fig.colorbar(im, ax=ax, label='Count')
            fig.patch.set_facecolor('white')
            
            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            plt.savefig(temp_path, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            
            self.temp_files.append(temp_path)
            return temp_path
        except Exception as e:
            print(f"Error creating confusion matrix: {e}")
            return None
    
    def _save_feature_importance_chart(self, features):
        """Generate and save feature importance chart"""
        try:
            fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
            
            names = []
            importances = []
            
            for f in features[:10]:
                if isinstance(f, dict):
                    name = str(f.get('name', f.get('feature', 'Feature')))
                    importance = float(f.get('importance', f.get('score', 0)))
                else:
                    name = str(f)
                    importance = 0.1
                
                names.append(name[:20])
                importances.append(max(0, min(1, importance)))
            
            if not names:
                names = ['Feature 1', 'Feature 2', 'Feature 3']
                importances = [0.3, 0.25, 0.2]
            
            colors_list = plt.cm.viridis(np.linspace(0.3, 0.9, len(names)))
            bars = ax.barh(names, importances, color=colors_list, edgecolor='black', linewidth=1.5)
            
            ax.set_xlabel('Importance Score', fontsize=11, fontweight='bold')
            ax.set_title('Feature Importance Analysis', fontsize=13, fontweight='bold', pad=15)
            ax.invert_yaxis()
            ax.set_xlim([0, 1])
            
            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, importances)):
                ax.text(val + 0.02, i, f'{val:.2f}', va='center', fontsize=9)
            
            ax.grid(True, alpha=0.3, axis='x', linestyle='--')
            fig.patch.set_facecolor('white')
            
            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            plt.savefig(temp_path, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            
            self.temp_files.append(temp_path)
            return temp_path
        except Exception as e:
            print(f"Error creating feature importance: {e}")
            return None
    
    def generate_report(self, data):
        """Generate PDF with charts using Platypus"""
        try:
            buffer = BytesIO()
            
            styles = getSampleStyleSheet()
            
            # Create custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=28,
                textColor=colors.HexColor('#1e40af'),
                spaceAfter=6,
                fontName='Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#1e40af'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=11,
                spaceAfter=8,
                leading=14
            )
            
            elements = []
            
            # Page 1: Title and Summary
            elements.append(Paragraph("📊 ML Fit Monitor", title_style))
            elements.append(Paragraph("Advanced ML Model Analysis Report with Charts", styles['Normal']))
            elements.append(Spacer(1, 12))
            
            elements.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
            elements.append(Spacer(1, 20))
            
            # Executive Summary
            summary = data.get('summary', {})
            elements.append(Paragraph("Executive Summary", heading_style))
            
            summary_data = [
                ['Metric', 'Value'],
                ['Best Model', self._safe_str(summary.get('best_model', 'N/A'))],
                ['Fit Status', self._safe_str(summary.get('overall_fit_status', 'N/A'))],
                ['Validation Score', f"{float(summary.get('val_score', 0)):.1%}"],
                ['Train-Val Gap', f"{float(summary.get('gap', 0)):.1%}"],
                ['Dataset Size', str(summary.get('dataset_size', 'N/A'))]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')])
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
            
            # Model Performance Table
            elements.append(Paragraph("Model Performance", heading_style))
            
            models = data.get('models', [])
            models_data = [['Model', 'Train Score', 'Val Score', 'Gap', 'Status']]
            
            for m in models:
                models_data.append([
                    self._safe_str(m.get('model', 'N/A'))[:15],
                    f"{float(m.get('train_score', 0)):.1%}",
                    f"{float(m.get('val_score', 0)):.1%}",
                    f"{float(m.get('gap', 0)):.1%}",
                    self._safe_str(m.get('fit_status', 'N/A'))[:10]
                ])
            
            models_table = Table(models_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1*inch, 1.2*inch])
            models_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            elements.append(models_table)
            elements.append(PageBreak())
            
            # Page 2: Charts
            elements.append(Paragraph("Visual Analysis", heading_style))
            elements.append(Spacer(1, 12))
            
            # ROC Curve
            roc_data = data.get('roc_data', {})
            if roc_data and 'fpr' in roc_data and 'tpr' in roc_data:
                roc_path = self._save_roc_chart(
                    roc_data.get('fpr', [0, 1]),
                    roc_data.get('tpr', [0, 1]),
                    roc_data.get('auc', 0.5)
                )
                if roc_path:
                    elements.append(Paragraph("ROC Curve", heading_style))
                    elements.append(RLImage(roc_path, width=4.5*inch, height=3.5*inch))
                    elements.append(Spacer(1, 12))
            
            # Confusion Matrix
            cm = data.get('confusion_matrix')
            if cm and len(cm) >= 2:
                cm_path = self._save_confusion_matrix_chart(cm)
                if cm_path:
                    elements.append(Paragraph("Confusion Matrix", heading_style))
                    elements.append(RLImage(cm_path, width=4.5*inch, height=3.5*inch))
                    elements.append(Spacer(1, 12))
            
            elements.append(PageBreak())
            
            # Page 3: Feature Importance and Recommendations
            elements.append(Paragraph("Feature Analysis", heading_style))
            elements.append(Spacer(1, 12))
            
            # Feature Importance
            features = data.get('feature_importance', [])
            if features:
                feat_path = self._save_feature_importance_chart(features)
                if feat_path:
                    elements.append(RLImage(feat_path, width=4.5*inch, height=3.5*inch))
                    elements.append(Spacer(1, 12))
            
            elements.append(PageBreak())
            
            # Recommendations
            elements.append(Paragraph("Recommendations & Next Steps", heading_style))
            elements.append(Spacer(1, 12))
            
            recs = data.get('recommendations', [])
            for i, rec in enumerate(recs[:8], 1):
                rec_text = self._safe_str(rec)
                elements.append(Paragraph(f"<b>✓</b> {rec_text}", body_style))
                if i < len(recs[:8]):
                    elements.append(Spacer(1, 6))
            
            elements.append(Spacer(1, 20))
            
            # Footer
            footer_text = f"<i>ML Fit Monitor • Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Confidential</i>"
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            # Build PDF
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            doc.build(elements)
            
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            # Cleanup temp files at end
            for temp_file in self.temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
