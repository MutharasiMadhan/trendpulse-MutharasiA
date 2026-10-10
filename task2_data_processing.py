
import json
from pathlib import Path

import pandas as pd

# Step 1: Find the latest JSON file in the data folder
data_folder = Path("data")
json_files = sorted(data_folder.glob("trends_*.json"))

if not json_files:
    print("No JSON files found in the data folder.")
    raise SystemExit(1)

input_file = json_files[-1]

# Load the JSON file into a Pandas DataFrame
try:
    with input_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} rows from {input_file}")

except (OSError, json.JSONDecodeError) as error:
    print(f"Failed to load JSON file: {error}")
    raise SystemExit(1)


# Step 2: Clean the data

# Remove duplicate stories based on post_id
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# Drop rows missing required values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Strip leading and trailing whitespace from titles
df["title"] = df["title"].astype(str).str.strip()

# Remove empty titles after stripping whitespace
df = df[df["title"] != ""]

# Convert score and num_comments to numeric values
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"], errors="coerce"
)

# Drop rows with invalid or missing numeric values
df = df.dropna(subset=["score", "num_comments"])

# Ensure both columns contain integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove stories with a score below 5
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

print(f"Rows remaining after cleaning: {len(df)}")


# Step 3: Save the cleaned data as CSV
output_file = data_folder / "trends_clean.csv"

try:
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(
        f"Saved {len(df)} cleaned rows to {output_file}"
    )

except OSError as error:
    print(f"Failed to save CSV file: {error}")
    raise SystemExit(1)


# Step 4: Print a summary of stories per category
print("\nStories per category:")

category_summary = df["category"].value_counts()

print(category_summary.to_string())
