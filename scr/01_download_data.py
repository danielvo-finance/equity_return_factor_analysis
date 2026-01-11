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
tickers.split(",")

start_date = input("Enter the start date of the data (e.g. 2015-01-01): ")
end_date = input("Enter the end date: ")

def download_data(ticker, start, end):
    os.makedirs(RAW_DIR, exist_ok=True)

    # takes input from user and receive data from Yahoo Finance
    df = yf.download(ticker, start=start, end=end, progress=False, group_by="column", auto_adjust=True)

    df.to_csv(f"{RAW_DIR}/{ticker}.csv")

for t in tickers:
    download_data(tickers, start_date, end_date)