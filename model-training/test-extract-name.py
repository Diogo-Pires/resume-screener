import spacy

nlp = spacy.load("extract_name_ner_model")

text = "Claude Bruce is a machine learning engineer at Facebook. Contact: david.davis@facebook.com, 987-654-7878. Skills: TensorFlow, Kubernetes, SQL, Python."
doc = nlp(text)

for ent in doc.ents:
    if ent.label_ == "PERSON":
        print(f"Detected Name: {ent.text}")
    if ent.label_ == "JOB_TITLE":
        print(f"Detected Job title: {ent.text}")
    if ent.label_ == "ORG":
        print(f"Detected ORG: {ent.text}")
    if ent.label_ == "EMAIL":
        print(f"Detected Email: {ent.text}")
    if ent.label_ == "PHONE":
        print(f"Detected Phone: {ent.text}")
    if ent.label_ == "SKILL":
        print(f"Detected Skills: {ent.text}")