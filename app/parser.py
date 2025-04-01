from fastapi import UploadFile
import pdfplumber

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text from a PDF resume."""
    with pdfplumber.open(pdf_file.file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text