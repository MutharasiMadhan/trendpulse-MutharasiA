
import pandas as pd
import numpy as np
from pathlib import Path

# Define input and output file paths
input_file = Path("data/trends_clean.csv")
output_file = Path("data/trends_analysed.csv")

# 1. Load and explore the data
if not input_file.exists():
    print(f"File not found: {input_file}")
    raise SystemExit(1)

df = pd.read_csv(input_file)

# Print the shape of the DataFrame
print(f"Loaded data: {df.shape}")
print()

# Display the first 5 rows
print("First 5 rows:")
print(df.head())
print()

# Print average score and comments
print(f"Average score   : {df['score'].mean():,.0f}")
print(f"Average comments: {df['num_comments'].mean():,.0f}")
print()

# 2. Basic analysis with NumPy
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")
print()

# Find the category with the most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print(
    f"Most stories in: {top_category} "
    f"({top_category_count} stories)"
)
print()

# Find the story with the most comments
most_commented_index = df["num_comments"].idxmax()
most_commented_story = df.loc[most_commented_index]

print(
    f'Most commented story: "{most_commented_story["title"]}" '
    f'— {most_commented_story["num_comments"]:,} comments'
)
print()

# 3. Add new columns
average_score = np.mean(scores)

# Engagement: comments per upvote, using the required formula
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if its score is greater than the average score
df["is_popular"] = df["score"] > average_score

# 4. Save the analyzed DataFrame
try:
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Saved to {output_file}")
except OSError as error:
    print(f"Failed to save file: {error}")
    raise SystemExit(1)
