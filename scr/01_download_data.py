"""
Note:
- The sole purpose of this script is for the user to input the asset ticker(s) that they desire to analyze.
- Once the ticker is inputted, the data will be downloaded as a csv in data/raw/.
- The data should NOT be modified once downloaded.
"""

import yfinance as yf
import os

RAW_DIR = "data/raw"

tickers = input("Enter stock ticker(s) to analyze (comma seperated): ").upper()
tickers = [t.strip() for t in tickers.split(",")]

start_date = input("Enter the start date of the data (e.g. 2015-01-01): ")
end_date = input("Enter the end date: ")

def download_data(ticker, start, end):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = f"{RAW_DIR}/{ticker}.csv"

    if os.path.exists(path):
        return
    
    # Takes input from user and download data from Yahoo Finance
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

    # Creates a csv for the downloaded data in data/raw/
    df.to_csv(path)

for t in tickers:
    download_data(t, start_date, end_date)
