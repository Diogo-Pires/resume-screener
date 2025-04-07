import json
import spacy
from spacy.training.example import Example
from spacy.util import minibatch
from spacy.training import offsets_to_biluo_tags
from sklearn.model_selection import train_test_split
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

def is_valid_example(text, entities):
    doc = nlp.make_doc(text)
    try:
        tags = offsets_to_biluo_tags(doc, entities)
        return "-" not in tags
    except Exception:
        return False

# Load training data
with open('synthetic_ner_data_train.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

train_data, eval_data = train_test_split(all_data, test_size=0.2, random_state=42)

# Training
overlap_counter = 0
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()

    for epoch in range(20):
        random.shuffle(train_data)
        losses = {}

        batches = minibatch(train_data, size=8)

        for batch in batches:
            examples = []
            for item in batch:
                text = item["text"]
                entities = item["entities"]

                if is_valid_example(text, entities):
                    overlap_counter = overlap_counter + 1
                    continue
                
                annotations = {"entities": [tuple(ent) for ent in entities]}
                
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
                total_loss += losses['ner']

            print(f"Epoch {epoch + 1} - Loss: {losses}")

            dropout = max(0.2, 0.5 - (epoch * 0.02))
            nlp.update(examples, drop=dropout, losses=losses)
            
print(f"Epoch 20 finished - Avg NER loss: {total_loss / batches}")
print("Found " + str(overlap_counter) + " overlaps")

examples = [Example.from_dict(nlp.make_doc(d["text"]), {"entities": d["entities"]}) for d in eval_data]
scorer = nlp.evaluate(examples)
print(scorer)

# Save trained model
nlp.to_disk("extract_name_ner_model")

#python -m spacy init config config.cfg --lang en --pipeline ner
#python -m spacy debug data config.cfg --paths.train train.spacy --paths.dev train.spacy
