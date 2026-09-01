"""
Step 2: Filtering for Factory Shutdown Relevance
--------------------------------------------------
Applies a stricter keyword filter to the post titles collected in
step 1, keeping only posts that are highly likely to be discussing
the factory shutdown, closures, or layoffs directly.

Output: df_relevant -> a DataFrame of highly relevant posts. In the
original run this narrowed 1,337 posts down to 73 highly relevant ones.

Requires: df_reddit from 01_reddit_post_collection.py
"""

strict_keywords = [
    "factory shutdown", "plant closure", "factory closure", "vw shutdown",
    "audi shutdown", "volkswagen layoffs", "job cuts", "production halt",
    "vw plant closure", "volkswagen to close", "brussels factory",
    "major layoffs",
]

df_relevant = df_reddit[
    df_reddit["title"].str.lower().str.contains("|".join(strict_keywords))
]

print(f"Highly relevant posts found: {len(df_relevant)}")
print(df_relevant[["title", "created", "subreddit"]].head(10))
