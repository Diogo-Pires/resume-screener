from fastapi import UploadFile
from transformers import pipeline
import pdfplumber

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text from a PDF resume."""
    with pdfplumber.open(pdf_file.file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def extract_name(text: str) -> str:
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    entities = ner_pipeline(text)
    for entity in entities:
        if entity["entity"].startswith("B-PER"):
            return entity["word"]
    return "Name not found"