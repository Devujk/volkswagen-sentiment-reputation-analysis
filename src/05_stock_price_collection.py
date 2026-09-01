"""
Step 5: Volkswagen Stock Price Data Collection
--------------------------------------------------
Downloads daily stock price data for Volkswagen AG (ticker: VOW3.DE,
Frankfurt Stock Exchange) from Yahoo Finance. The date range (July
2024 - April 2025) covers the period before, during, and after the
factory shutdown announcement (December 2024), matching the Reddit
sentiment collection window.

Requirements: yfinance, pandas
"""

import yfinance as yf
import pandas as pd

vw_stock = yf.download("VOW3.DE", start="2024-07-01", end="2025-04-15")
vw_stock.to_excel("volkswagen_stock_data.xlsx")

print("Stock data saved to 'volkswagen_stock_data.xlsx'")
