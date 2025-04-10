import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")
doc_bin = DocBin()

with open("../synthetic_ner_data_train.json", "r", encoding="utf-8") as f:
    training_data = json.load(f)

for record in training_data:
    doc = nlp.make_doc(record["text"])
    ents = []
    for start, end, label in record["entities"]:
        span = doc.char_span(start, end, label=label)
        if span is None:
            print(f"Skipping misaligned entity: {start}-{end} in '{record['text']}'")
        else:
            ents.append(span)
    doc.ents = ents
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")