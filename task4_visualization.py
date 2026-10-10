
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Setup: load data and create output folder
input_file = Path("data/trends_analysed.csv")
output_folder = Path("outputs")
output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

# Ensure the popularity column is interpreted as Boolean
if df["is_popular"].dtype == object:
    df["is_popular"] = (
        df["is_popular"].astype(str).str.lower() == "true"
    )

print(f"Loaded {len(df)} stories from {input_file}")


# Helper function to shorten long story titles
def shorten_title(title):
    title = str(title)
    if len(title) > 50:
        return title[:47] + "..."
    return title


# 2. Chart 1: Top 10 stories by score
top_stories = df.nlargest(10, "score").copy()
top_stories["short_title"] = top_stories["title"].apply(shorten_title)

fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(top_stories["short_title"], top_stories["score"])
ax.set_title("Top 10 Stories by Score")
ax.set_xlabel("Score")
ax.set_ylabel("Story Title")
ax.invert_yaxis()
fig.tight_layout()

fig.savefig(output_folder / "chart1_top_stories.png", dpi=300)
plt.show()
plt.close(fig)


# 3. Chart 2: Stories per category
category_counts = df["category"].value_counts()

fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.Set2(
    [i / max(len(category_counts) - 1, 1)
     for i in range(len(category_counts))]
)

ax.bar(category_counts.index, category_counts.values, color=colors)
ax.set_title("Number of Stories per Category")
ax.set_xlabel("Category")
ax.set_ylabel("Number of Stories")
ax.tick_params(axis="x", rotation=30)
fig.tight_layout()

fig.savefig(output_folder / "chart2_categories.png", dpi=300)
plt.show()
plt.close(fig)


# 4. Chart 3: Score vs comments
fig, ax = plt.subplots(figsize=(9, 6))

non_popular = df[~df["is_popular"]]
popular = df[df["is_popular"]]

ax.scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)
ax.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

ax.set_title("Story Score vs Number of Comments")
ax.set_xlabel("Score")
ax.set_ylabel("Number of Comments")
ax.legend()
fig.tight_layout()

fig.savefig(output_folder / "chart3_scatter.png", dpi=300)
plt.show()
plt.close(fig)


# 5. Bonus: Dashboard containing all three charts
fig, axes = plt.subplots(1, 3, figsize=(21, 7))
fig.suptitle("TrendPulse Dashboard", fontsize=16)

# Dashboard chart 1: Top stories
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()
axes[0].tick_params(axis="y", labelsize=8)

# Dashboard chart 2: Category counts
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=colors
)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Dashboard chart 3: Score vs comments
axes[2].scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)
axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

fig.tight_layout(rect=[0, 0, 1, 0.93])

fig.savefig(output_folder / "dashboard.png", dpi=300)
plt.show()
plt.close(fig)

print("\nAll charts saved successfully in the outputs/ folder.")
