from collections import defaultdict
import random
import json

with open("../synthetic_ner_data_train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

balanced_data = []
label_buckets = defaultdict(list)

for item in data:
    for ent in item["entities"]:
        label_buckets[ent[2]].append(item)
        break  # Assumes each item has 1 dominant entity — adjust if needed

# Cap all labels to 3000
target = 3000
for label, examples in label_buckets.items():
    balanced_data.extend(random.sample(examples, min(len(examples), target)))

# Save new file
with open("synthetic_ner_data_train.json", "w", encoding="utf-8") as f:
    json.dump(balanced_data, f, indent=2)