import sys
import pandas as pd

if len(sys.argv) < 3:
    print("No arguments were provided. First argument should be a csv file and second a number of common words to be removed(default 5).")
    exit(1)

file_to_clean = '../' + sys.argv[1] + '.csv'
file_to_find = '../' + sys.argv[2] + '.csv'

# Load find list
finds = pd.read_csv(file_to_find, header=None)[0].dropna().str.strip().str.lower().tolist()

# Load file list
dataset_df = pd.read_csv(file_to_clean, header=None, names=["dataset"])
clean_data = []
removed_words = []

for data in dataset_df["dataset"].dropna():
    words = data.split()
    filtered_words = [word for word in words if word.lower() not in finds]
    if filtered_words:
        clean_data.append(" ".join(filtered_words))
    
    found_words = [word for word in words if word.lower() in finds]
    if found_words:
        removed_words.append(" ".join(found_words))

# Save cleaned
pd.Series(clean_data).drop_duplicates().to_csv(file_to_clean, index=False, header=False)
print(f"Were found {removed_words} in {file_to_find} and {file_to_clean} and they were removed from {file_to_clean}")