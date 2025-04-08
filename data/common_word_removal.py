import pandas as pd
import re
from collections import Counter

# === CONFIGURATION ===
input_file = "input.csv"
output_file = "cleaned.csv"
num_common_words_to_remove = 20  # Adjust as needed

# === LOAD CSV ===
df = pd.read_csv(input_file, header=None, names=["text"])

# === TOKENIZE & COUNT WORDS ===
all_text = " ".join(df["text"].astype(str)).lower()
tokens = re.findall(r'\b\w+\b', all_text)
word_counts = Counter(tokens)
most_common = set(word for word, _ in word_counts.most_common(num_common_words_to_remove))

# === FUNCTION TO REMOVE COMMON WORDS FROM TEXT ===
def remove_common_words(text, common_words):
    tokens = re.findall(r'\b\w+\b', text.lower())
    filtered_tokens = [word for word in tokens if word not in common_words]
    return " ".join(filtered_tokens)

# === APPLY CLEANING ===
df["cleaned"] = df["text"].astype(str).apply(lambda x: remove_common_words(x, most_common))

# === SAVE TO FILE ===
df["cleaned"].to_csv(output_file, index=False, header=False)

print(f"Top {num_common_words_to_remove} common words removed.")
print(f"Cleaned CSV saved to '{output_file}'.")