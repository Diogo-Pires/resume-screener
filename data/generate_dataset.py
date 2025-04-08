import random
import json
import pandas as pd
import spacy

nlp = spacy.blank("en")

def load_list(filename):
    return pd.read_csv(filename, header=None, low_memory=False)[0].dropna().tolist()

names = load_list("names.csv")
job_titles = load_list("job-titles.csv")
orgs = load_list("orgs.csv")
emails = load_list("emails.csv")
phones = load_list("phones.csv")
skills = load_list("skills.csv")

TEMPLATES = [
    "{name} currently works as a {job_title} at {org}. {contact} Core skills include {skills}.",
    "Contact {name}, a {job_title} from {org}, {contact} Key expertise: {skills}.",
    "Meet {name} - {job_title} @ {org}. {contact} Proficient in {skills}.",
    "{name} is a seasoned {job_title} working at {org}. {contact} Experienced in {skills}.",
    "{org} employs {name} as a {job_title}. {contact} Skills: {skills}.",
    "You can reach {name} ({job_title} at {org}) {contact} They specialize in {skills}.",
    "{name}, a {job_title} affiliated with {org}, {contact} Technical skills: {skills}.",
]

# Optional: typo generator (very basic)
def introduce_typo(s):
    if len(s) < 4 or random.random() > 0.15:  # only 15% get typos
        return s
    i = random.randint(1, len(s)-2)
    return s[:i] + s[i+1] + s[i] + s[i+2:]

def generate_contact(email, phone):
    parts = []
    if random.random() > 0.2:
        label = random.choice(["Email:", "Reach at", "email", "Email at"])
        parts.append(f"{label} {email}")  # No typo here!
    if random.random() > 0.2:
        label = random.choice(["Phone:", "Tel:", "Call", "Phone number"])
        parts.append(f"{label} {phone}")
    return " ".join(parts) if parts else "No contact provided."

def generate_skills(skills_list):
    selected = random.sample(skills_list, k=random.randint(1, 3))
    noisy_skills = [s for s in selected]  # Keep skill entities clean!
    display_skills = [introduce_typo(s) for s in selected]
    return ", ".join(display_skills), noisy_skills

def generate_synthetic_data():
    name = random.choice(names)
    job_title = random.choice(job_titles)
    org = random.choice(orgs)
    email = random.choice(emails)
    phone = random.choice(phones)

    skills_text, selected_skills = generate_skills(skills)

    template = random.choice(TEMPLATES)
    contact = generate_contact(email, phone)
    text = template.format(
        name=name,
        job_title=job_title,
        org=org,
        contact=contact,
        skills=skills_text
    )

    doc = nlp(text)
    entities = []

    def try_add_entity(value, label):
        start = text.lower().find(value.lower())
        if start == -1:
            return
        end = start + len(value)
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if not span:
            return
        for ent in entities:
            if not (end <= ent[0] or start >= ent[1]):
                return
        entities.append([start, end, label])

    try_add_entity(name, "PERSON")
    try_add_entity(job_title, "JOB_TITLE")
    try_add_entity(org, "ORG")

    # Only tag email/phone if present and no typo
    if email in text:
        try_add_entity(email, "EMAIL")
    if phone in text:
        try_add_entity(phone, "PHONE")

    # Add each skill (try noisy and clean match)
    for skill in selected_skills:
        if skill in text:
            try_add_entity(skill, "SKILL")

    known_skills = set(s.lower() for s in skills)  # Load from your dataset

    for ent in doc.ents:
        if ent.label_ == "ORG" and ent.text.lower() in known_skills:
            print(f"[Fixing label] {ent.text} was ORG -> SKILL")
            ent.label_ = "SKILL"

    return {"text": text, "entities": entities}

# Generate dataset
data = [generate_synthetic_data() for _ in range(3000)]

# Save to JSON
with open("../model-training/synthetic_ner_data_train.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"{len(data)} noisy + diverse NER records generated!")
