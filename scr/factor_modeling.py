"""
Notes:
- Implements:
    - CAPM
    - Fama-French 3-Factor Model
    - PCA-based factor model

- Imput:
    - data/combined_returns.csv
    -data/factors.csv
"""

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Downloads factor data
def download_factors(start = "2015-01-01", end = "2025-01-01"):
    """
    Factors:
        - MKT: Using S&P500 daily returns
        - SMB: IWM - SPY
        - HML: VTV - VUG
        - RF: IRX
    """
    # Download adjusted close prices for all tickers
    sp500 = yf.download("^GSPC", start=start, end=end, auto_adjust=True)["Close"].squeeze()
    iwm   = yf.download("IWM", start=start, end=end, auto_adjust=True)["Close"].squeeze()
    spy   = yf.download("SPY", start=start, end=end, auto_adjust=True)["Close"].squeeze()
    vtv   = yf.download("VTV", start=start, end=end, auto_adjust=True)["Close"].squeeze()
    vug   = yf.download("VUG", start=start, end=end, auto_adjust=True)["Close"].squeeze()
    irx   = yf.download("^IRX", start=start, end=end, auto_adjust=True)["Close"].squeeze()

    # Compute daily returns for factors
    mkt_return = sp500.pct_change()
    smb = iwm.pct_change() - spy.pct_change()
    hml = vtv.pct_change() - vug.pct_change()
    
    # Risk-free rate: forward-fill missing values, convert to daily decimal
    rf = (irx.ffill() / 100) / 252

    # Combine all series into one DataFrame and drop rows with missing data
    factors = pd.concat([mkt_return, smb, hml, rf], axis=1)
    factors.columns = ["MKT", "SMB", "HML", "RF"]
    factors = factors.dropna()

    # Print shape and first few rows for verification
    print("Factors shape:", factors.shape)
    print(factors.head())
    
    return factors

# Aligns returns and factors on common dates
def align_returns_factors(returns, factors):
    common_index = returns.index.intersection(factors.index)
    return returns.loc[common_index], factors.loc[common_index]


# CAPM regression to estimate alpha and beta for each asset
def capm(returns, factors):
    # Compute excess returns
    excess_returns = returns.sub(factors["RF"], axis=0)

    # Prep regression matrix for CAPM
    X = factors["MKT"].values
    X = np.vstack([np.ones(len(X)), X]).T

    alphas = []
    betas = []

    # OLS regression for each asset
    for col in excess_returns:
        y = excess_returns[col].values
        # [alpha, beta]
        beta_alpha = np.linalg.lstsq(X, y, rcond=None)[0]
        alphas.append(beta_alpha[0])
        betas.append(beta_alpha[1])
    
    return pd.DataFrame({"Alpha": alphas, "Beta": betas}, index=returns.columns)


def ffm(returns, factors):
    excess_returns = returns.sub(factors["RF"], axis=0)
    X = factors[["MKT", "SMB", "HML"]].values
    X = np.hstack([np.ones((len(X), 1)), X])  # add constant for alpha

    alphas = []
    betas_mkt = []
    betas_smb = []
    betas_hml = []

    for col in excess_returns:
        y = excess_returns[col].values
        coef = np.linalg.lstsq(X, y, rcond=None)[0]  # [alpha, beta_mkt, beta_smb, beta_hml]
        alphas.append(coef[0])
        betas_mkt.append(coef[1])
        betas_smb.append(coef[2])
        betas_hml.append(coef[3])

    return pd.DataFrame({
        "Alpha": alphas,
        "Beta_MKT": betas_mkt,
        "Beta_SMB": betas_smb,
        "Beta_HML": betas_hml
    }, index=returns.columns)


# Performs PCA on returns and extract main factors
def pca(returns, n_factors=3):
    R = returns.fillna(0).values
    # Center the returns
    R_centered = R - R.mean(axis=0)
    # Covariance matrix
    cov = np.cov(R_centered, rowvar=False)
    # Eigen decomposition
    eig_vals, eig_vecs = np.linalg.eigh(cov)
    # Sort by largest eigenvalues
    idx = np.argsort(eig_vals)[::-1]
    eig_vals = eig_vals[idx][:n_factors]
    eig_vecs = eig_vecs[:, idx][:, :n_factors]
    return eig_vals, eig_vecs

# Plot the explained variance of each PCA factor
def plot_pca_variance(eig_vals):
    total = np.sum(eig_vals)
    explained = eig_vals / total
    plt.bar(range(1, len(eig_vals)+1), explained)
    plt.xlabel("Factor")
    plt.ylabel("Explained Variance")
    plt.title("PCA Factor Explained Variance")
    plt.show()