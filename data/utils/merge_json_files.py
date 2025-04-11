import os
import json

# Directory containing the JSON files
input_dir = "../dataset"
output_file = "../dataset.json"

merged_data = []

for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                merged_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode {filename}: {e}")

# Save merged content to a single JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=2, ensure_ascii=True)

print(f"Merged {len(merged_data)} files into {output_file}")