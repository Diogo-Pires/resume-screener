import json
import spacy
from spacy.training.example import Example
from spacy.util import minibatch
from spacy.training import offsets_to_biluo_tags
from sklearn.model_selection import train_test_split
from spacy.pipeline import EntityRuler
import random

# Load base model
nlp = spacy.load("en_core_web_sm")

ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [{"label": "EMAIL", "pattern": [{"TEXT": {"REGEX": r"^[^@\s]+@[^@\s]+\.[a-zA-Z]+$"}}]}]
ruler.add_patterns(patterns)

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
total_loss = 0.0

with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()

    for epoch in range(30):
        random.shuffle(train_data)
        losses = {}
        epoch_examples = []

        batches = list(minibatch(train_data, size=8))

        for batch in batches:
            examples = []
            for item in batch:
                text = item["text"]
                entities = item["entities"]

                if not is_valid_example(text, entities):
                    overlap_counter += 1
                    continue

                annotations = {"entities": [tuple(ent) for ent in entities]}
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)

            if examples:
                dropout = max(0.2, 0.5 - (epoch * 0.02))
                nlp.update(examples, drop=dropout, losses=losses)
                total_loss += losses.get("ner", 0.0)

        print(f"Epoch {epoch + 1} - Loss: {losses.get('ner', 0.0):.4f}")

print(f"\nTraining finished.")
print(f"Total skipped examples due to overlap/misalignment: {overlap_counter}")
print(f"Average NER loss per epoch: {total_loss / 20:.4f}")

# Evaluation
examples = [Example.from_dict(nlp.make_doc(d["text"]), {"entities": d["entities"]}) for d in eval_data]
scorer = nlp.evaluate(examples)
print("\nEvaluation:")
print(scorer)

# Save trained model
nlp.to_disk("extract_name_ner_model")


#python -m spacy init config config.cfg --lang en --pipeline ner
#python -m spacy debug data config.cfg --paths.train train.spacy --paths.dev train.spacy
