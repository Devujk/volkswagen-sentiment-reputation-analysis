"""
Step 7: Top Commented Post by Sentiment Category
-----------------------------------------------------
Identifies, for each sentiment category (positive / negative /
neutral), the Reddit post that generated the most comments. Used to
support the discussion-based insights in the results chapter (e.g.
one post driving a disproportionate share of the reaction across all
three sentiment categories).

Requirements: pandas
"""

import pandas as pd

df = pd.read_excel("Cleaned_data.xlsx")

sentiment_counts = (
    df.groupby(["title", "sentiment"]).size().reset_index(name="Comment_Count")
)

top_positive = sentiment_counts[sentiment_counts["sentiment"] == "positive"] \
    .sort_values(by="Comment_Count", ascending=False).head(1)
top_negative = sentiment_counts[sentiment_counts["sentiment"] == "negative"] \
    .sort_values(by="Comment_Count", ascending=False).head(1)
top_neutral = sentiment_counts[sentiment_counts["sentiment"] == "neutral"] \
    .sort_values(by="Comment_Count", ascending=False).head(1)

top_posts = pd.concat([top_positive, top_negative, top_neutral])

print("Top Posts by Sentiment Category:")
print(top_posts)
