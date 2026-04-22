"""Advanced PDF generator with embedded charts (ROC, Confusion Matrix)"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Image as RLImage
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from sklearn.metrics import roc_curve, auc
import base64
from PIL import Image


class AdvancedPDFReportGenerator:
    def __init__(self):
        self.margin = 0.5 * inch
        self.page_width = letter[0]
        self.page_height = letter[1]
        self.line_height = 14
        
    def _safe_str(self, value):
        """Convert to safe ASCII string"""
        if value is None:
            return "N/A"
        s = str(value)
        s = ''.join(c for c in s if ord(c) < 128)
        return s.strip()[:150]
    
    def _create_roc_chart(self, fpr, tpr, auc_score):
        """Generate ROC Curve as PIL Image"""
        try:
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            
            ax.plot(fpr, tpr, color='#1e40af', lw=2, label=f'ROC curve (AUC = {auc_score:.3f})')
            ax.plot([0, 1], [0, 1], color='grey', lw=1, linestyle='--', label='Random Classifier')
            
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate', fontsize=9)
            ax.set_ylabel('True Positive Rate', fontsize=9)
            ax.set_title('ROC Curve', fontsize=11, fontweight='bold')
            ax.legend(loc="lower right", fontsize=8)
            ax.grid(True, alpha=0.3)
            
            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            img_buffer.seek(0)
            plt.close(fig)
            
            # Convert to PIL Image
            img = Image.open(img_buffer)
            img.load()
            return img_buffer
        except Exception as e:
            print(f"Error creating ROC chart: {e}")
            return None
    
    def _create_confusion_matrix_chart(self, cm):
        """Generate Confusion Matrix heatmap as PIL Image"""
        try:
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            
            # Ensure cm is numeric
            cm = np.array(cm, dtype=float)
            
            # Create heatmap
            im = ax.imshow(cm, cmap='Blues', aspect='auto')
            
            # Labels
            labels = ['Negative', 'Positive']
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
            ax.set_ylabel('True Label', fontsize=9)
            ax.set_xlabel('Predicted Label', fontsize=9)
            ax.set_title('Confusion Matrix', fontsize=11, fontweight='bold')
            
            # Add text annotations
            for i in range(2):
                for j in range(2):
                    val = int(cm[i][j])
                    text = ax.text(j, i, str(val), ha="center", va="center", 
                                 color="white" if cm[i][j] > cm.max()/2 else "black", fontsize=12)
            
            fig.colorbar(im, ax=ax)
            
            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
        except Exception as e:
            print(f"Error creating confusion matrix chart: {e}")
            return None
    
    def _create_feature_importance_chart(self, features):
        """Generate Feature Importance bar chart as PIL Image"""
        try:
            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            
            # Handle different feature structures
            names = []
            importances = []
            
            for f in features[:8]:
                if isinstance(f, dict):
                    name = str(f.get('name', f.get('feature', 'Feature')))
                    importance = float(f.get('importance', f.get('score', 0)))
                else:
                    name = str(f)
                    importance = 0.1
                
                names.append(name[:20])  # Truncate long names
                importances.append(max(0, min(1, importance)))
            
            if not names:
                names = ['Feature 1', 'Feature 2', 'Feature 3']
                importances = [0.3, 0.25, 0.2]
            
            colors_list = plt.cm.Blues(np.linspace(0.4, 0.8, len(names)))
            ax.barh(names, importances, color=colors_list)
            
            ax.set_xlabel('Importance Score', fontsize=9)
            ax.set_title('Feature Importance (Top 8)', fontsize=11, fontweight='bold')
            ax.invert_yaxis()
            
            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
        except Exception as e:
            print(f"Error creating feature importance chart: {e}")
            return None
    
    def generate_report(self, data):
        """Generate advanced PDF with charts"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setTitle("ML Fit Monitor - Advanced Report")
        
        y = self.page_height - self.margin
        
        # ===== PAGE 1: TITLE & SUMMARY =====
        
        # Title
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.HexColor('#1e40af'))
        c.drawString(self.margin, y, "ML Fit Monitor")
        y -= self.line_height * 1.5
        
        # Subtitle
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.grey)
        c.drawString(self.margin, y, "Advanced ML Model Analysis Report with Visual Charts")
        y -= self.line_height * 0.7
        
        # Date
        c.setFont("Helvetica", 9)
        date_str = self._safe_str(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(self.margin, y, date_str)
        y -= self.line_height * 2
        
        # Executive Summary
        summary = data.get('summary', {})
        if summary:
            c.setFont("Helvetica-Bold", 13)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Executive Summary")
            y -= self.line_height * 1.3
            
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            
            items = [
                f"Best Model: {self._safe_str(summary.get('best_model', 'N/A'))}",
                f"Fit Status: {self._safe_str(summary.get('overall_fit_status', 'N/A'))}",
                f"Validation Score: {float(summary.get('val_score', 0)):.1%}",
                f"Train-Val Gap: {float(summary.get('gap', 0)):.1%}",
            ]
            
            for item in items:
                c.drawString(self.margin + 20, y, f"• {item}")
                y -= self.line_height
            
            y -= self.line_height
        
        # Model Performance
        models = data.get('models', [])
        if models:
            c.setFont("Helvetica-Bold", 13)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Model Performance")
            y -= self.line_height * 1.3
            
            # Header
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.rect(self.margin, y - 15, 5*inch, 15, stroke=1, fill=1)
            c.setFillColor(colors.white)
            
            headers = ["Model", "Train", "Val", "Gap", "Status"]
            x_positions = [self.margin + 5, self.margin + 90, self.margin + 140, self.margin + 180, self.margin + 220]
            
            for header, x_pos in zip(headers, x_positions):
                c.drawString(x_pos, y - 12, header)
            
            y -= 25
            
            # Rows
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            row_height = 18
            
            for i, m in enumerate(models):
                if i % 2 == 1:
                    c.setFillColor(colors.HexColor('#f0f4f8'))
                    c.rect(self.margin, y - row_height, 5*inch, row_height, stroke=0, fill=1)
                
                c.setFillColor(colors.black)
                
                model_name = self._safe_str(m.get('model', 'N/A'))[:12]
                train = f"{float(m.get('train_score', 0)):.0%}"
                val = f"{float(m.get('val_score', 0)):.0%}"
                gap = f"{float(m.get('gap', 0)):.0%}"
                status = self._safe_str(m.get('fit_status', 'N/A'))[:6]
                
                row_data = [model_name, train, val, gap, status]
                
                for data_val, x_pos in zip(row_data, x_positions):
                    c.drawString(x_pos, y - 12, data_val)
                
                c.setLineWidth(0.5)
                c.line(self.margin, y - row_height, self.margin + 5*inch, y - row_height)
                
                y -= row_height
            
            y -= self.line_height
        
        # ===== PAGE 2: CHARTS =====
        c.showPage()
        y = self.page_height - self.margin
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor('#1e40af'))
        c.drawString(self.margin, y, "Visual Analysis Charts")
        y -= self.line_height * 1.5
        
        # ROC Curve
        roc_data = data.get('roc_data', {})
        roc_generated = False
        if roc_data and 'fpr' in roc_data and 'tpr' in roc_data:
            try:
                fpr = list(roc_data.get('fpr', [0, 1]))
                tpr = list(roc_data.get('tpr', [0, 1]))
                auc_score = float(roc_data.get('auc', 0.5))
                
                roc_img = self._create_roc_chart(fpr, tpr, auc_score)
                if roc_img:
                    try:
                        # Ensure BytesIO is at the beginning
                        roc_img.seek(0)
                        c.drawImage(roc_img, self.margin, y - 2.2*inch, width=3*inch, height=2.2*inch, preserveAspectRatio=True)
                        roc_generated = True
                        y -= 2.5*inch
                    except Exception as e:
                        print(f"Error drawing ROC image: {e}")
            except Exception as e:
                print(f"ROC chart error: {e}")
        
        if not roc_generated:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.grey)
            c.drawString(self.margin, y, "ROC Curve - Unable to generate visualization")
            y -= self.line_height * 2.5
        
        # Confusion Matrix
        cm = data.get('confusion_matrix')
        cm_generated = False
        if cm and len(cm) >= 2 and len(cm[0]) >= 2:
            try:
                cm_array = np.array(cm, dtype=float)
                cm_img = self._create_confusion_matrix_chart(cm_array)
                if cm_img:
                    try:
                        # Ensure BytesIO is at the beginning
                        cm_img.seek(0)
                        c.drawImage(cm_img, self.margin + 3.5*inch, y - 2.2*inch, width=3*inch, height=2.2*inch, preserveAspectRatio=True)
                        cm_generated = True
                    except Exception as e:
                        print(f"Error drawing confusion matrix image: {e}")
            except Exception as e:
                print(f"Confusion matrix chart error: {e}")
        
        if not cm_generated:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.grey)
            c.drawString(self.margin + 3.5*inch, y, "Confusion Matrix - Unable to generate visualization")
        
        y -= 2.5*inch
        
        # ===== PAGE 3: FEATURES & RECOMMENDATIONS =====
        c.showPage()
        y = self.page_height - self.margin
        
        # Feature Importance Chart
        features = data.get('feature_importance', [])
        feat_generated = False
        if features and len(features) > 0:
            try:
                feat_img = self._create_feature_importance_chart(features)
                if feat_img:
                    try:
                        # Ensure BytesIO is at the beginning
                        feat_img.seek(0)
                        c.drawImage(feat_img, self.margin, y - 2.5*inch, width=3.5*inch, height=2.5*inch, preserveAspectRatio=True)
                        feat_generated = True
                        y -= 3*inch
                    except Exception as e:
                        print(f"Error drawing feature importance image: {e}")
            except Exception as e:
                print(f"Feature importance chart error: {e}")
        
        if not feat_generated:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.grey)
            c.drawString(self.margin, y, "Feature Importance - Unable to generate visualization")
            y -= self.line_height * 2.5
        
        # Recommendations
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.HexColor('#1e40af'))
        c.drawString(self.margin, y, "Recommendations")
        y -= self.line_height * 1.3
        
        recs = data.get('recommendations', [])
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        for rec in recs[:5]:
            rec_text = self._safe_str(rec)[:80]
            c.drawString(self.margin + 20, y, f"• {rec_text}")
            y -= self.line_height
        
        # ===== FOOTER =====
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(self.margin, self.margin - 10, f"ML Fit Monitor | {datetime.now().strftime('%Y-%m-%d')}")
        
        c.save()
        buffer.seek(0)
        return buffer
