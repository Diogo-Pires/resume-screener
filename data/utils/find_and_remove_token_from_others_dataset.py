import sys
import pandas as pd

if len(sys.argv) < 2:
    print("No enough arguments were provided. First argument should be the csv file to be cleaned and second the one to look for tokens.")
    exit

file_to_clean = sys.argv[0]
file_to_find = sys.argv[1]

# Load orgs list
org_names = pd.read_csv(file_to_find, header=None)[0].dropna().str.strip().str.lower().tolist()

# Load dataset list
dataset_df = pd.read_csv(file_to_clean, header=None, names=["dataset"])
clean_data = []

for data in dataset_df["dataset"].dropna():
    words = data.split()
    filtered_words = [word for word in words if word.lower() not in org_names]
    if filtered_words:
        clean_data.append(" ".join(filtered_words))

# Save cleaned skills
pd.Series(clean_data).drop_duplicates().to_csv(file_to_clean, index=False, header=False)