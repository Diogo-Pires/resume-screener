import random
import json

# Lists to choose random elements from
names = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis", "David Brown", "Sophia Wilson", "Liam Martinez", "Olivia Hernandez"]
job_titles = ["Software Engineer", "Data Scientist", "Project Manager", "Backend Developer", "Machine Learning Engineer", "Cybersecurity Analyst", "Cloud Architect", "Senior Software Developer"]
orgs = ["Google", "Facebook", "Amazon", "Microsoft", "Tesla", "IBM", "Oracle", "Adobe"]
emails = ["john.doe@gmail.com", "jane.smith@fb.com", "michael.johnson@amazon.com", "emily.davis@microsoft.com", "david.brown@tesla.com", "sophia.wilson@ibm.com", "liam.martinez@oracle.com", "olivia.hernandez@adobe.com"]
phones = ["+1-555-123-4567", "987-654-3210", "444-555-6666", "159-753-4862", "321-654-9870", "800-555-1212", "617-555-1313", "818-555-1414"]
skills = ["Python", "SQL", "Docker", "Machine Learning", "Agile", "Scrum", "Cloud Computing", "Network Security"]

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
        [text.lower().find(skill1), text.lower().find(skill1)+len(skill1), "SKILL"],
        [text.lower().find(skill2), text.lower().find(skill2)+len(skill2), "SKILL"]
    ]
    
    return {"text": text, "entities": entities}

# Generate 200 records
data = [generate_synthetic_data() for _ in range(200)]

# Save data to JSON
with open("synthetic_ner_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("200 synthetic records have been generated and saved to 'synthetic_ner_data.json'.")