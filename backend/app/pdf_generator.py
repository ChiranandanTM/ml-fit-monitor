"""
Simple Advanced PDF Report Generation using ReportLab only
Generates professional PDF reports with tables and text (no charts initially)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
import traceback


class PDFReportGenerator:
    """Generate professional ML analysis reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()

    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

    def generate_report(self, analysis_results):
        """Generate complete professional PDF report"""
        try:
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )

            story = []

            # ===== TITLE =====
            story.append(Paragraph('ML Fit Monitor - Analysis Report', self.styles['CustomTitle']))
            story.append(Paragraph(
                f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                self.styles['Normal']
            ))
            story.append(Spacer(1, 0.3*inch))

            # ===== EXECUTIVE SUMMARY =====
            story.append(Paragraph('Executive Summary', self.styles['SectionHeader']))
            
            summary = analysis_results.get('summary', {})
            summary_data = [
                ['Metric', 'Value'],
                ['Best Model', str(summary.get('best_model', 'N/A'))],
                ['Fit Status', str(summary.get('overall_fit_status', 'N/A'))],
                ['Validation Score', f"{summary.get('val_score', 0):.2%}"],
                ['Train-Val Gap', f"{summary.get('gap', 0):.2%}"],
                ['Dataset Size', str(summary.get('dataset_size', 'N/A'))],
            ]

            summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')])
            ]))
            story.extend([summary_table, Spacer(1, 0.3*inch)])

            # ===== MODEL PERFORMANCE =====
            story.append(Paragraph('Model Performance', self.styles['SectionHeader']))
            
            models = analysis_results.get('models', [])
            if models:
                metrics_data = [['Model', 'Train Score', 'Val Score', 'Gap', 'Status']]
                for model in models:
                    metrics_data.append([
                        str(model.get('model', 'N/A'))[:20],
                        f"{model.get('train_score', 0):.2%}",
                        f"{model.get('val_score', 0):.2%}",
                        f"{model.get('gap', 0):.2%}",
                        str(model.get('fit_status', 'Unknown'))[:12]
                    ])

                metrics_table = Table(metrics_data, colWidths=[1.3*inch, 1.1*inch, 1.1*inch, 0.9*inch, 1.1*inch])
                metrics_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')])
                ]))
                story.extend([metrics_table, Spacer(1, 0.3*inch)])

            # ===== FEATURE IMPORTANCE =====
            features = analysis_results.get('feature_importance', [])
            if features:
                story.append(PageBreak())
                story.append(Paragraph('Top Features', self.styles['SectionHeader']))
                
                feat_data = [['Feature Name', 'Importance Score']]
                for i, feat in enumerate(features[:10]):
                    feat_data.append([
                        str(feat.get('name', f'Feature {i}'))[:30],
                        f"{feat.get('importance', 0):.4f}"
                    ])

                feat_table = Table(feat_data, colWidths=[3*inch, 2*inch])
                feat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')])
                ]))
                story.extend([feat_table, Spacer(1, 0.3*inch)])

            # ===== CONFUSION MATRIX =====
            cm = analysis_results.get('confusion_matrix')
            if cm is not None:
                story.append(PageBreak())
                story.append(Paragraph('Confusion Matrix', self.styles['SectionHeader']))
                
                cm_data = [['', 'Predicted Negative', 'Predicted Positive']]
                cm_data.append(['Actual Negative', str(int(cm[0][0])), str(int(cm[0][1]))])
                cm_data.append(['Actual Positive', str(int(cm[1][0])), str(int(cm[1][1]))])

                cm_table = Table(cm_data, colWidths=[2*inch, 2*inch, 2*inch])
                cm_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e0e7ff')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ]))
                story.extend([cm_table, Spacer(1, 0.3*inch)])

            # ===== RECOMMENDATIONS =====
            recommendations = analysis_results.get('recommendations', [])
            if recommendations:
                story.append(PageBreak())
                story.append(Paragraph('Recommendations', self.styles['SectionHeader']))
                
                for rec in recommendations:
                    story.append(Paragraph(f'• {str(rec)[:100]}', self.styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))

            # ===== FOOTER =====
            story.append(Spacer(1, 0.5*inch))
            footer = Paragraph(
                f'<b>End of Report</b><br/>ML Fit Monitor | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                self.styles['Normal']
            )
            story.append(footer)

            # Build PDF
            doc.build(story)
            pdf_buffer.seek(0)

            print(f"✅ PDF report generated successfully ({len(pdf_buffer.getvalue())} bytes)")
            return pdf_buffer

        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            traceback.print_exc()
            raise
