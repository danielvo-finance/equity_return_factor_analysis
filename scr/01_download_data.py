"""
Note:
- The sole purpose of this script is for the user to input the asset ticker(s) that they desire to analyze.
- Once the ticker is inputted, the data will be downloaded as a csv in data/raw/.
- The data should NOT be modified once downloaded.
"""

import yfinance as yf
import os

def download_data(ticker, start, end):
    pass