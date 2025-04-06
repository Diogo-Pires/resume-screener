import json
import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import random

# Load base model
nlp = spacy.load("en_core_web_sm")

# Get NER pipeline
ner = nlp.get_pipe("ner")

# Add new entity labels
labels = ["PERSON", "JOB_TITLE", "ORG", "EMAIL", "PHONE", "SKILL"]
for label in labels:
    ner.add_label(label)

# Disable other components
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

def has_overlap(entities):
    spans = []
    for start, end, label in entities:
        for s, e, _ in spans:
            if start < e and end > s:
                return True
        spans.append((start, end, label))
    return False

# Load training data
with open('synthetic_ner_data_train.json', 'r', encoding='utf-8') as f:
    training_data = json.load(f)

# Training
overlap_counter = 0
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()

    for epoch in range(20):
        random.shuffle(training_data)
        losses = {}

        batches = minibatch(training_data, size=8)

        for batch in batches:
            examples = []
            for item in batch:
                text = item["text"]
                entities = item["entities"]

                if has_overlap(entities):
                    overlap_counter = overlap_counter + 1
                    continue
                
                annotations = {"entities": [tuple(ent) for ent in entities]}
                
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            print(f"Loss: {losses}")

            nlp.update(examples, drop=0.5, losses=losses)

print("Found " + str(overlap_counter) + " overlaps")

# Save trained model
nlp.to_disk("extract_name_ner_model")