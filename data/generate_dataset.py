import random
import json
import pandas as pd
import spacy

# Load a blank spaCy model for token alignment
nlp = spacy.blank("en")

# Load data from CSVs (no headers expected)
def load_list(filename):
    return pd.read_csv(filename, header=None, low_memory=False)[0].dropna().tolist()

names = load_list("names.csv")
job_titles = load_list("job-titles.csv")
orgs = load_list("orgs.csv")
emails = load_list("emails.csv")
phones = load_list("phones.csv")
skills = load_list("skills.csv")

def generate_synthetic_data():
    name = random.choice(names)
    job_title = random.choice(job_titles)
    org = random.choice(orgs)
    email = random.choice(emails)
    phone = random.choice(phones)
    skill1, skill2, skill3 = random.sample(skills, 3)

    text = (
        f"{name} is a {job_title} at {org}. "
        f"You can contact them at {email} or {phone}. "
        f"Skills: {skill1}, {skill2}, {skill3}."
    )

    doc = nlp(text)
    entities = []

    # Helper: Safely find non-overlapping entity spans
    def try_add_entity(value, label):
        start = text.lower().find(value.lower())
        if start == -1:
            return
        end = start + len(value)
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if not span:
            return
        # Check for overlap
        for ent in entities:
            if not (end <= ent[0] or start >= ent[1]):
                return
        entities.append([start, end, label])

    try_add_entity(name, "PERSON")
    try_add_entity(job_title, "JOB_TITLE")
    try_add_entity(org, "ORG")
    try_add_entity(email, "EMAIL")
    try_add_entity(phone, "PHONE")
    try_add_entity(skill1, "SKILL")
    try_add_entity(skill2, "SKILL")
    try_add_entity(skill3, "SKILL")

    return {"text": text, "entities": entities}

# Generate 3000 records
data = [generate_synthetic_data() for _ in range(3000)]

# Save to JSON
with open("../model-training/synthetic_ner_data_train.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("3000 synthetic NER records generated and saved!")
