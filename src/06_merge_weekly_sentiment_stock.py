"""
Step 6: Weekly Sentiment and Stock Price Merge
--------------------------------------------------
Resamples both the sentiment scores and the stock prices to weekly
averages, aligns them on matching weeks (interpolating any gaps in
the sentiment series), and merges them into a single dataset used
for the correlation analysis and Power BI visualizations.

Requirements: pandas, yfinance, matplotlib
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# --- Load & resample weekly sentiment ---
df_sentiment = pd.read_excel("Cleaned_data.xlsx")
df_sentiment["created"] = pd.to_datetime(df_sentiment["created"])
df_sentiment.set_index("created", inplace=True)
weekly_sentiment = df_sentiment["compound"].resample("W").mean()

# --- Fetch & resample weekly stock price ---
vw_stock = yf.download("VOW3.DE", start="2024-07-01", end="2025-04-15")
weekly_stock = vw_stock["Close"].resample("W").mean()

# --- Align weeks and interpolate any gaps in sentiment ---
weekly_sentiment_aligned = weekly_sentiment.reindex(weekly_stock.index)
weekly_sentiment_aligned.interpolate(method="time", inplace=True)

# --- Combine into a single dataset ---
combined_df = pd.concat([weekly_sentiment_aligned, weekly_stock], axis=1)
combined_df.columns = ["Weekly Sentiment", "Weekly Stock Price"]
combined_df.dropna(inplace=True)

print(combined_df.head(10))

# --- Visualize ---
combined_df.plot(figsize=(12, 6), title="Weekly Sentiment vs VW Stock Price", grid=True)
plt.show()

# --- Export for Power BI / thesis appendix ---
combined_df.to_excel("interpolated_sentiment_vs_stock.xlsx", index=True)
print("Final merged dataset saved to 'interpolated_sentiment_vs_stock.xlsx'.")
