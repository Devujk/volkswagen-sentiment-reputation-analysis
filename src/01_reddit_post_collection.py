"""
Step 1: Reddit Post Collection
--------------------------------
Connects to Reddit's API (via PRAW) and searches a set of relevant
subreddits for posts discussing the Volkswagen factory shutdown /
layoffs announced in late 2024.

Output: df_reddit -> a DataFrame of post metadata (title, text, date,
subreddit, url, id).

Requirements: praw, pandas
"""

import os
import praw
from datetime import datetime
import pandas as pd

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="reddit-vw-shutdown-scraper",
)

subreddits = [
    "Volkswagen", "cars", "autos", "news", "europe", "germany",
    "electricvehicles", "worldnews", "autonews", "AskEurope",
]

keywords = [
    "Volkswagen factory shutdown", "VW factory closure",
    "Audi Brussels shutdown", "Volkswagen layoffs", "VW layoffs",
    "Volkswagen job cuts", "Audi plant closed", "VW production halt",
    "VW shutdown", "Audi factory shut down", "Volkswagen crisis",
    "Audi Belgium cuts", "auto industry layoffs", "EV factory slowdown",
    "EV demand drop Volkswagen", "Volkswagen to close factory",
    "Volkswagen shuts Brussels plant", "Volkswagen Brussels to be shut",
    "Volkswagen halts production",
    "Volkswagen boss wants to close European factories",
]

posts_data = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    for keyword in keywords:
        for post in subreddit.search(keyword, sort="new", time_filter="year", limit=200):
            post_date = datetime.fromtimestamp(post.created_utc)
            if post_date.year in [2024, 2025]:
                posts_data.append({
                    "title": post.title,
                    "text": post.selftext,
                    "created": post_date,
                    "subreddit": sub,
                    "url": post.url,
                    "id": post.id,
                })

df_reddit = pd.DataFrame(posts_data)
print(f"Total relevant posts collected: {len(df_reddit)}")

df_reddit.to_csv("reddit_posts_raw.csv", index=False)
print("Saved to reddit_posts_raw.csv")
