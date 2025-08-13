import io
from typing import Union
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

def extract_text_from_uploaded_file(uploaded_file) -> str:
    # uploaded_file is a Streamlit UploadedFile object (file-like)
    content = uploaded_file.read()
    # check type
    if uploaded_file.type == 'text/plain' or uploaded_file.name.lower().endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    if uploaded_file.type == 'application/pdf' or uploaded_file.name.lower().endswith('.pdf'):
        if fitz is None:
            raise RuntimeError("PyMuPDF (fitz) not installed. Install 'pymupdf' to extract from PDFs.")
        doc = fitz.open(stream=content, filetype='pdf')
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)
    # fallback
    return content.decode('utf-8', errors='ignore')
