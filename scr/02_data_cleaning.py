"""
Noets:
- This script will load the raw data stock data previously downloaded from Yahoo Finance.
- Keeps only the adjusted close prices.
- Saves the processed data as a CSV in the 'data/processed' directory.
"""

import pandas as pd
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
file = [f for f in os.listdir(RAW_DIR) if f.endswith(".csv")]

def compute_returns(file):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    ticker = file.replace(".csv", "")

    df = pd.read_csv(
        os.path.join(RAW_DIR, file),
        skiprows=3,
        header=None,
        names = ["Date", "Close", "High", "Low", "Open", "Volume"],
        index_col=0,
        parse_dates=True)
    
    df = df[["Close"]].copy()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df["Return"] = df["Close"].pct_change()
    df = df.dropna()

    df.to_csv(f"{PROCESSED_DIR}/{ticker}_processed.csv")
    print(f"Saved processed data for {ticker}")

for t in file:
    compute_returns(t)