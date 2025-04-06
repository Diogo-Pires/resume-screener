import random
import json
import pandas as pd

# Load lists
names = pd.read_csv("names.csv", header=None, low_memory=False)[0].dropna().tolist()
job_titles = pd.read_csv('job-titles.csv', header=None, low_memory=False)[0].dropna().tolist()
orgs = pd.read_csv('orgs.csv', header=None, low_memory=False)[0].dropna().tolist()
emails = pd.read_csv('emails.csv', header=None, low_memory=False)[0].dropna().tolist()
phones = pd.read_csv('phones.csv', header=None, low_memory=False)[0].dropna().tolist()
skills = pd.read_csv('skills.csv', header=None, low_memory=False)[0].dropna().tolist()

def find_span(text, substring):
    """Finds the first non-overlapping occurrence of a substring and returns (start, end)"""
    start = text.index(substring)
    return (start, start + len(substring))

def generate_synthetic_data():
    name = random.choice(names)
    job_title = random.choice(job_titles)
    org = random.choice(orgs)
    email = random.choice(emails)
    phone = random.choice(phones)
    skill1 = random.choice(skills)
    skill2 = random.choice(skills)
    skill3 = random.choice(skills)

    text = f"{name} is a {job_title} at {org}. You can contact he/she at {email} or {phone}. Skills: {skill1}, {skill2}, {skill3}."

    # Ensure unique skills
    skills_used = list(set([skill1, skill2, skill3]))
    
    entities = []
    for value, label in [(name, "PERSON"), (job_title, "JOB_TITLE"), (org, "ORG"),
                         (email, "EMAIL"), (phone, "PHONE")] + [(s, "SKILL") for s in skills_used]:
        try:
            start, end = find_span(text, value)
            entities.append([start, end, label])
        except ValueError:
            continue  # skip if not found

    return {"text": text, "entities": entities}

# Generate data
data = [generate_synthetic_data() for _ in range(2000)]

# Save
with open("../model-training/synthetic_ner_data_train.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("2000 records generated and saved.")