import random
import json
import pandas as pd

# Lists to choose random elements from
names = pd.read_csv("names.csv", header=None)[0].dropna().tolist()
job_titles = pd.read_csv('job-titles.csv', header=None)[0].dropna().tolist()
orgs = pd.read_csv('orgs.csv', header=None)[0].dropna().tolist()
emails = pd.read_csv('emails.csv', header=None)[0].dropna().tolist()
phones = pd.read_csv('phones.csv', header=None)[0].dropna().tolist()
skills = pd.read_csv('skills.csv', header=None)[0].dropna().tolist()

# Function to generate a synthetic record
def generate_synthetic_data():
    name = random.choice(names)
    job_title = random.choice(job_titles)
    org = random.choice(orgs)
    email = random.choice(emails)
    phone = random.choice(phones)
    skill1 = random.choice(skills)
    skill2 = random.choice(skills)
    
    text = f"{name} is a {job_title} at {org}. You can contact them at {email} or {phone}. Skills: {skill1}, {skill2}."
    entities = [
        [0, len(name), "PERSON"],
        [len(name)+5, len(name)+5+len(job_title), "JOB_TITLE"],
        [len(name)+5+len(job_title)+3, len(name)+5+len(job_title)+3+len(org), "ORG"],
        [len(name)+5+len(job_title)+3+len(org)+2, len(name)+5+len(job_title)+3+len(org)+2+len(email), "EMAIL"],
        [len(name)+5+len(job_title)+3+len(org)+2+len(email)+2, len(name)+5+len(job_title)+3+len(org)+2+len(email)+2+len(phone), "PHONE"],
        [text.lower().find(skill1), text.lower().find(skill1)+len(skill1), "SKILL"]
    ]
    
    return {"text": text, "entities": entities}

# Generate 200 records
data = [generate_synthetic_data() for _ in range(1000)]

# Save data to JSON
with open("synthetic_ner_data_train.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("1000 synthetic records have been generated and saved to 'synthetic_ner_data.json'.")