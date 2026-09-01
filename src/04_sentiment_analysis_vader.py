"""
Step 4: Sentiment Analysis with VADER
-----------------------------------------
Applies VADER (Valence Aware Dictionary and sEntiment Reasoner) to the
deduplicated Reddit comments. VADER is a lexicon/rule-based model
well suited to short, informal social-media text (handles slang,
emojis, and punctuation-based intensity well).

Each comment is scored (pos / neu / neg / compound) and classified as
positive, negative, or neutral. Output in the original run: 1,533
unique, labeled comments.

Requirements: pandas, vaderSentiment (pip install vaderSentiment)
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_excel("Cleaned_data.xlsx")
df["comment"] = df["comment"].astype(str).str.lower()
df_unique = df.drop_duplicates(subset="comment")

analyzer = SentimentIntensityAnalyzer()
df_unique["compound"] = df_unique["comment"].apply(
    lambda text: analyzer.polarity_scores(text)["compound"]
)


def classify_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"


df_unique["sentiment"] = df_unique["compound"].apply(classify_sentiment)

df_unique.to_excel("Cleaned_data_deduplicated.xlsx", index=False)
print("Sentiment-labeled file saved.")

# --- Attach post title/subreddit context to each comment (optional) ---
# df_final = df_unique.merge(
#     df_reddit[["id", "title", "subreddit"]],
#     left_on="post_id", right_on="id", how="left",
# )
# df_final.drop(columns=["id"], inplace=True)
# df_final.to_excel("reddit_comments_sentiment_with_titles.xlsx", index=False)
