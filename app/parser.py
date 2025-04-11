import re
from fastapi import UploadFile
from transformers import pipeline
import pdfplumber

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text from a PDF resume."""
    with pdfplumber.open(pdf_file.file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text


def extract_entities(text: str) -> dict:
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
    results = {
        "NAME": [],
        "ORG": [],
        "EMAIL": [],
        "PHONE": []
    }

    # NER model entities
    entities = ner_pipeline(text)
    for ent in entities:
        if ent["entity_group"] == "PER":
            results["NAME"].append(ent["word"])
        elif ent["entity_group"] == "ORG":
            results["ORG"].append(ent["word"])

    # Regex for email
    email_matches = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    results["EMAIL"].extend(email_matches)

    # Regex for phone numbers
    phone_matches = re.findall(r'\+?\d[\d\s\-().]{7,}\d', text)
    results["PHONE"].extend(phone_matches)

    #results["SKILLS"] = extract_skills(text)

    return results

# def extract_skills(text: str) -> list:
#     skill_pipeline = pipeline("ner", model="extraction_ner_model", aggregation_strategy="simple")
#     skills = []
#     entities = skill_pipeline(text)

#     for ent in entities:
#         if ent["entity_group"] == "SKILL":
#             skills.append(ent["word"])

#     return skills