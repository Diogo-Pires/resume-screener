from collections import Counter
import json

with open("balanced_train_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

label_counts = Counter()
for item in data:
    for ent in item["entities"]:
        if len(ent) == 3:
            label_counts[ent[2]] += 1

print(label_counts)