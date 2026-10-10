
import requests
import json
import time
from datetime import datetime
from pathlib import Path

# Hacker News API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
headers = {"User-Agent": "TrendPulse/1.0"}

# Keywords used to classify story titles
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}

MAX_PER_CATEGORY = 25


def fetch_top_story_ids():
    """Fetch the top story IDs from Hacker News."""
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()[:500]

    except (requests.RequestException, ValueError) as error:
        print(f"Failed to fetch story IDs: {error}")
        return []


def fetch_story(story_id):
    """Fetch the details of one story."""
    try:
        url = STORY_URL.format(id=story_id)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        story = response.json()

        # Ignore missing or invalid story objects
        if not isinstance(story, dict) or not story.get("title"):
            return None

        return story

    except (requests.RequestException, ValueError) as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def categorize_story(title):
    """Assign a category by matching keywords without case sensitivity."""
    title_lower = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    # Ignore stories that do not match any category
    return None


def collect_stories():
    """Collect up to 25 stories for each category."""
    story_ids = fetch_top_story_ids()

    # Store collected stories separately for each category
    collected = {category: [] for category in categories}

    for category, keywords in categories.items():
        print(f"Collecting category: {category}")

        for story_id in story_ids:
            # Stop when this category has enough stories
            if len(collected[category]) >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            if story is None:
                continue

            # Check whether the story matches the current category
            assigned_category = categorize_story(story["title"])

            if assigned_category != category:
                continue

            # Store the seven required fields
            record = {
                "post_id": story.get("id", story_id),
                "title": story.get("title", ""),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat(timespec="seconds")
            }

            # Avoid adding the same story twice
            if not any(
                item["post_id"] == record["post_id"]
                for item in collected[category]
            ):
                collected[category].append(record)

        # Wait two seconds between category loops
        time.sleep(2)

    # Combine all category lists into one list
    all_stories = [
        story
        for category_stories in collected.values()
        for story in category_stories
    ]

    return all_stories


def save_to_json(stories):
    """Save the collected stories to a dated JSON file."""
    # Create the data folder if it does not exist
    data_folder = Path("data")
    data_folder.mkdir(parents=True, exist_ok=True)

    # Generate a filename using today's date
    date_string = datetime.now().strftime("%Y%m%d")
    file_path = data_folder / f"trends_{date_string}.json"

    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(stories, file, indent=4, ensure_ascii=False)

        print(f"Collected {len(stories)} stories. Saved to {file_path}")

    except OSError as error:
        print(f"Failed to save JSON file: {error}")


if __name__ == "__main__":
    stories = collect_stories()
    save_to_json(stories)
