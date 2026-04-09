import pandas as pd
import numpy as np

np.random.seed(42)
n = 500

cgpa = np.round(np.random.uniform(5.0, 10.0, n), 2)
internships = np.random.randint(0, 4, n)
projects = np.random.randint(0, 6, n)
technical_score = np.random.randint(40, 101, n)
hackerrank_score = np.random.randint(30, 101, n)

# Placement logic: weighted score determines outcome (realistic bias)
score = (
    (cgpa - 5) / 5 * 30
    + internships * 8
    + projects * 4
    + (technical_score - 40) / 60 * 25
    + (hackerrank_score - 30) / 70 * 20
)

# Add noise, threshold at ~50th percentile
threshold = np.percentile(score, 45)
placement = (score + np.random.normal(0, 5, n) > threshold).astype(int)

df = pd.DataFrame({
    "CGPA": cgpa,
    "Internships": internships,
    "Projects": projects,
    "Technical_Skills_Score": technical_score,
    "HackerRank_Score": hackerrank_score,
    "Placement_Status": placement
})

df.to_csv("placement_data.csv", index=False)
print(f"Dataset saved. Shape: {df.shape}")
print(df["Placement_Status"].value_counts())
print(df.head())