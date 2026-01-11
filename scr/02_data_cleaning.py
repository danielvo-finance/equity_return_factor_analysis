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

def compute_returns(ticker):
    pass