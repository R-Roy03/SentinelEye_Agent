import io
from pypdf import PdfReader

def read_pdf_from_bytes(pdf_data: bytes) -> str:
    """
    Raw PDF bytes se text extract karta hai.
    """
    try:
        # BytesIO ka use karke memory mein file open karte hain
        reader = PdfReader(io.BytesIO(pdf_data))
        text = ""
        
        # Har page ka text nikaal kar jodte jao
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
            
        return text.strip()
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return "Error: Could not read the PDF document. File might be corrupted."