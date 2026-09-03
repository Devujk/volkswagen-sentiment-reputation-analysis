"""
Step 3: Comment Extraction from Relevant Posts
-------------------------------------------------
Extracts all comments from the filtered, highly relevant Reddit posts
(df_relevant) using their post IDs.

Output: df_comments -> a DataFrame of comments with post_id, comment
text, score, and created date. This raw scrape is deduplicated and
cleaned in 04_sentiment_analysis_vader.py — see the README's
"Limitations" section for a data-quality note found while assembling
this repository.

Requires: praw, pandas; reddit_posts_relevant.csv from 02_filter_relevant_posts.py
"""

import os
import pandas as pd
from datetime import datetime
import praw

df_relevant = pd.read_csv("reddit_posts_relevant.csv")

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="reddit-vw-shutdown-scraper",
)

relevant_comments = []

for post_id in df_relevant["id"]:
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        relevant_comments.append({
            "post_id": post_id,
            "comment": comment.body,
            "score": comment.score,
            "created": datetime.fromtimestamp(comment.created_utc),
        })

df_comments = pd.DataFrame(relevant_comments)
print(f"Total comments collected: {len(df_comments)}")

# --- Data-integrity check: confirm every comment belongs to a filtered post ---
unmatched_ids = df_comments[~df_comments["post_id"].isin(df_relevant["id"])]

if unmatched_ids.empty:
    print("All comments are from filtered relevant posts.")
else:
    print("Warning: some comments are from unrelated posts!")
    print(unmatched_ids.head())

df_comments.to_excel("Cleaned_data.xlsx", index=False)
print("Saved to Cleaned_data.xlsx (input for 04_sentiment_analysis_vader.py)")
