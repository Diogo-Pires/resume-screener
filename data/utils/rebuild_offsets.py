import json

# Function to check and fix overlapping spans
def has_overlap(a, b):
    """Check if two spans overlap."""
    return a[0] < b[1] and b[0] < a[1]

def rebuild_offsets(text, annotations):
    """Rebuild the offsets for each annotation based on the exact text match."""
    new_annotations = []
    for label, entity in annotations:
        start = text.lower().find(entity.lower())
        if start != -1:
            end = start + len(entity)
            new_annotations.append((start, end, label))
    return new_annotations

def fix_overlaps(annotations):
    """Fix overlapping spans by keeping the longer or more relevant entity."""
    unique_annotations = []
    for annotation in annotations:
        if not any(has_overlap(annotation, existing) for existing in unique_annotations):
            unique_annotations.append(annotation)
    return unique_annotations

def check_offsets(text, annotations):
    """Check if the annotation offsets match the actual text."""
    errors = []
    for start, end, label in annotations:
        extracted = text[start:end]
        if len(text) < end:
            errors.append((start, end, label, "<out of range>"))
        elif label.split(":")[-1].strip().lower() not in extracted.lower():
            errors.append((start, end, label, extracted))
    return errors

def process_resume_data(data):
    text = data["text"]
    annotations = data["annotations"]
    
    # Rebuild the offsets for annotations based on exact matching text
    fixed_annotations = rebuild_offsets(text, [(entry[2], entry[2].split(":")[1].strip()) for entry in annotations])
    
    # Remove overlapping annotations
    fixed_annotations = fix_overlaps(fixed_annotations)
    
    # Check for errors in the offsets
    errors = check_offsets(text, fixed_annotations)
    if errors:
        for error in errors:
            print(f"❌ Offset {error[0]}–{error[1]} for {error[2]} -> Extracted: `{error[3]}`")
    
    # Update the annotations in the original data
    data["annotations"] = fixed_annotations
    return data

# Load your dataset
with open('../dataset.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# Process all data entries
fixed_data = [process_resume_data(entry) for entry in all_data]

# Save the fixed dataset to a new file
with open('fixed_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(fixed_data, f, indent=4)

print("Finished processing and saved fixed dataset to 'fixed_dataset.json'")
