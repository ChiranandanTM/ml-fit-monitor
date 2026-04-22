"""PDF generator using Canvas API for clean text rendering - FIXED"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


class PDFReportGenerator:
    def __init__(self):
        self.margin = 0.5 * inch
        self.page_width = letter[0]
        self.page_height = letter[1]
        self.line_height = 14
        self.normal_font_size = 10
        self.heading_font_size = 13
        self.title_font_size = 18
        
    def _safe_str(self, value):
        """Convert to safe ASCII string"""
        if value is None:
            return "N/A"
        s = str(value)
        s = ''.join(c for c in s if ord(c) < 128)
        return s.strip()[:150]
    
    def generate_report(self, data):
        """Generate PDF using Canvas API"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setTitle("ML Fit Monitor Report")
        
        y = self.page_height - self.margin
        
        # Title
        c.setFont("Helvetica-Bold", self.title_font_size)
        c.setFillColor(colors.HexColor('#1e40af'))
        title = self._safe_str("ML Fit Monitor")
        c.drawString(self.margin, y, title)
        y -= self.line_height * 1.5
        
        # Subtitle
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.grey)
        subtitle = self._safe_str("Comprehensive ML Model Analysis Report")
        c.drawString(self.margin, y, subtitle)
        y -= self.line_height * 0.7
        
        # Date
        c.setFont("Helvetica", 9)
        date_str = self._safe_str(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(self.margin, y, date_str)
        y -= self.line_height * 2
        
        # Executive Summary Section
        summary = data.get('summary', {})
        if summary:
            c.setFont("Helvetica-Bold", self.heading_font_size)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Executive Summary")
            y -= self.line_height * 1.5
            
            c.setFont("Helvetica", self.normal_font_size)
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
        
        # Model Performance Section
        models = data.get('models', [])
        if models:
            if y < self.margin + 2*inch:
                c.showPage()
                y = self.page_height - self.margin
            
            c.setFont("Helvetica-Bold", self.heading_font_size)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Model Performance")
            y -= self.line_height * 1.5
            
            # Draw table header
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.rect(self.margin, y - 15, 5*inch, 15, stroke=1, fill=1)
            c.setFillColor(colors.white)
            
            headers = ["Model", "Train", "Val", "Gap", "Status"]
            x_positions = [self.margin + 5, self.margin + 90, self.margin + 140, self.margin + 180, self.margin + 220]
            
            for header, x_pos in zip(headers, x_positions):
                c.drawString(x_pos, y - 12, header)
            
            y -= 25
            
            # Draw table rows
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
        
        # Feature Importance Section
        features = data.get('feature_importance', [])
        if features:
            if y < self.margin + 2*inch:
                c.showPage()
                y = self.page_height - self.margin
            
            c.setFont("Helvetica-Bold", self.heading_font_size)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Feature Importance (Top 10)")
            y -= self.line_height * 1.5
            
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.rect(self.margin, y - 15, 3*inch, 15, stroke=1, fill=1)
            c.setFillColor(colors.white)
            c.drawString(self.margin + 5, y - 12, "Feature")
            c.drawString(self.margin + 200, y - 12, "Importance")
            
            y -= 25
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            row_height = 16
            
            for i, f in enumerate(features[:10]):
                if i % 2 == 1:
                    c.setFillColor(colors.HexColor('#f0f4f8'))
                    c.rect(self.margin, y - row_height, 3*inch, row_height, stroke=0, fill=1)
                
                c.setFillColor(colors.black)
                
                feat_name = self._safe_str(f.get('name', f'Feature {i}'))[:25]
                feat_val = f"{float(f.get('importance', 0)):.4f}"
                
                c.drawString(self.margin + 5, y - 12, feat_name)
                c.drawString(self.margin + 200, y - 12, feat_val)
                
                c.setLineWidth(0.5)
                c.line(self.margin, y - row_height, self.margin + 3*inch, y - row_height)
                
                y -= row_height
            
            y -= self.line_height
        
        # Confusion Matrix
        cm = data.get('confusion_matrix')
        if cm and len(cm) == 2:
            if y < self.margin + 2.5*inch:
                c.showPage()
                y = self.page_height - self.margin
            
            c.setFont("Helvetica-Bold", self.heading_font_size)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Confusion Matrix")
            y -= self.line_height * 1.5
            
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#1e40af'))
            
            cell_width = 80
            cell_height = 20
            
            c.rect(self.margin, y - cell_height, cell_width * 3, cell_height, stroke=1, fill=1)
            c.setFillColor(colors.white)
            c.drawString(self.margin + 5, y - 15, "")
            c.drawString(self.margin + cell_width + 5, y - 15, "Predicted Neg")
            c.drawString(self.margin + cell_width * 2 + 5, y - 15, "Predicted Pos")
            
            y -= cell_height
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            
            labels = ["Actual Neg", "Actual Pos"]
            for i, label in enumerate(labels):
                c.rect(self.margin, y - cell_height, cell_width * 3, cell_height, stroke=1, fill=0)
                c.drawString(self.margin + 5, y - 15, label)
                c.drawString(self.margin + cell_width + 30, y - 15, str(int(cm[i][0])))
                c.drawString(self.margin + cell_width * 2 + 30, y - 15, str(int(cm[i][1])))
                y -= cell_height
            
            y -= self.line_height
        
        # Recommendations
        recs = data.get('recommendations', [])
        if recs:
            if y < self.margin + 1.5*inch:
                c.showPage()
                y = self.page_height - self.margin
            
            c.setFont("Helvetica-Bold", self.heading_font_size)
            c.setFillColor(colors.HexColor('#1e40af'))
            c.drawString(self.margin, y, "Recommendations")
            y -= self.line_height * 1.5
            
            c.setFont("Helvetica", self.normal_font_size)
            c.setFillColor(colors.black)
            
            for rec in recs[:5]:
                rec_text = self._safe_str(rec)[:90]
                c.drawString(self.margin + 20, y, f"• {rec_text}")
                y -= self.line_height
        
        # Footer
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        footer = self._safe_str(f"ML Fit Monitor | {datetime.now().strftime('%Y-%m-%d')}")
        c.drawString(self.margin, self.margin - 10, footer)
        
        c.save()
        buffer.seek(0)
        return buffer
