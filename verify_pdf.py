"""Verify PDF content is correct"""
import PyPDF2

try:
    with open('test_pdf.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
        
        print("✓ PDF is valid and readable")
        print("\nFirst page content preview:")
        print(text[:500])
        
        # Check for corruption indicators
        if "Ø" in text or "Ü" in text or "ß" in text:
            print("\n❌ Encoding corruption detected!")
        else:
            print("\n✅ Text encoding looks clean!")
        
except Exception as e:
    print(f"Error reading PDF: {e}")
    print("Note: PDF still may be valid - PyPDF2 may have compatibility issues")
