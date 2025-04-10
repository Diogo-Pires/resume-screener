import pandas as pd
import re
from collections import Counter
import sys
from nltk.corpus import stopwords
from nltk import download

if len(sys.argv) < 3:
    print("No arguments were provided. First argument should be a csv file and second a number of common words to be removed(default 5).")
    exit(1)

# Download stopwords if not already present
download('stopwords')
stop_words = set(stopwords.words('english'))

# === CONFIG ===
file = '../' + sys.argv[1] + '.csv'
top_n_common_to_remove = int(sys.argv[2])

# === LOAD FILE ===
dataset = pd.read_csv(file, header=None, names=["dataset"], low_memory=False)
dataset["dataset"] = dataset["dataset"].astype(str).str.strip().str.lower()

# === CLEAN TEXT & TOKENIZE ===
def clean_and_tokenize(token):
    # Remove punctuation, numbers, extra whitespace
    cleaned = re.sub(r'[^a-zA-Z\s]', '', token)
    tokens = cleaned.lower().split()
    return [word for word in tokens if word not in stop_words and len(word) > 1]

all_tokens = []
dataset["tokens"] = dataset["dataset"].apply(lambda x: clean_and_tokenize(x))
dataset["tokens"].apply(lambda tokens: all_tokens.extend(tokens))

# === GET MOST COMMON (NOISY) WORDS ===
word_freq = Counter(all_tokens)
common_words = set(word for word, _ in word_freq.most_common(top_n_common_to_remove))

# === FILTER OUT COMMON WORDS FROM TOKENS ===
def remove_common(tokens):
    return " ".join([token for token in tokens if token not in common_words])

dataset["cleaned"] = dataset["tokens"].apply(remove_common)

# === REMOVE EMPTY ENTRIES AFTER CLEANING ===
dataset = dataset[dataset["cleaned"].str.strip() != ""]

# === SAVE TO FILE ===
dataset["cleaned"].drop_duplicates().to_csv(file, index=False, header=False)

print(f"Cleaned skills saved to: {file}")
print(f"Removed top {top_n_common_to_remove} common/noisy words: {common_words}")