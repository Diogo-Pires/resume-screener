import pandas as pd

# Load orgs list
org_names = pd.read_csv("orgs.csv", header=None)[0].dropna().str.strip().str.lower().tolist()

# Load skills list
skills_df = pd.read_csv("job-titles.csv", header=None, names=["skill"])
clean_skills = []

for skill in skills_df["skill"].dropna():
    words = skill.split()
    filtered_words = [word for word in words if word.lower() not in org_names]
    if filtered_words:
        clean_skills.append(" ".join(filtered_words))

# Save cleaned skills
pd.Series(clean_skills).drop_duplicates().to_csv("skills.csv", index=False, header=False)