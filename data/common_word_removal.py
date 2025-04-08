import pandas as pd
import re
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk import download

# Download stopwords if not already present
download('stopwords')
stop_words = set(stopwords.words('english'))

# === CONFIG ===
input_file = "job-titles.csv"
output_file = "job-titles.csv"
top_n_common_to_remove = 5  # adjust based on your dataset size

# === LOAD SKILLS ===
skills = pd.read_csv(input_file, header=None, names=["skill"], low_memory=False)
skills["skill"] = skills["skill"].astype(str).str.strip().str.lower()

# === CLEAN TEXT & TOKENIZE ===
def clean_and_tokenize(skill):
    # Remove punctuation, numbers, extra whitespace
    cleaned = re.sub(r'[^a-zA-Z\s]', '', skill)
    tokens = cleaned.lower().split()
    return [word for word in tokens if word not in stop_words and len(word) > 1]

all_tokens = []
skills["tokens"] = skills["skill"].apply(lambda x: clean_and_tokenize(x))
skills["tokens"].apply(lambda tokens: all_tokens.extend(tokens))

# === GET MOST COMMON (NOISY) WORDS ===
word_freq = Counter(all_tokens)
common_words = set(word for word, _ in word_freq.most_common(top_n_common_to_remove))

# === FILTER OUT COMMON WORDS FROM TOKENS ===
def remove_common(tokens):
    return " ".join([token for token in tokens if token not in common_words])

skills["cleaned"] = skills["tokens"].apply(remove_common)

# === REMOVE EMPTY ENTRIES AFTER CLEANING ===
skills = skills[skills["cleaned"].str.strip() != ""]

# === SAVE TO FILE ===
skills["cleaned"].drop_duplicates().to_csv(output_file, index=False, header=False)

print(f"Cleaned skills saved to: {output_file}")
print(f" Removed top {top_n_common_to_remove} common/noisy words.")