"""
Notes:
- This script will allow us to compute:
    - volatility
    - variance
    - cumulative returns
    - maximum drawdowns
"""
import numpy as np 

def vol(returns, annualize=True):
    """
    Compute volatility (standard deviation) of returns.

    Parameters:
        returns: pd.Series or pd.DataFrame of daily returns
        annualize: bool, whether to annualize volatility using 252 trading days

    Returns:
        pd.Series of volatility values for each asset
    """
    # Compute standard deviation of daily returns
    volatility = returns.std()
    
    # We are using 252 for trading days
    if annualize:
        volatility *= np.sqrt(252)
    
    # Return volatility
    return volatility


def var(returns, alpha=0.05):
    """
    Compute historical Value at Risk (VaR).

    Parameters:
        returns: pd.Series or pd.DataFrame of returns
        alpha: confidence level for VaR (default 0.05 for 5% worst-case loss)

    Returns:
        pd.Series of VaR values for each asset
    """
    # Use quantile to find the alpha-percentile loss
    return returns.quantile(alpha)


def cumulative_returns(returns):
    """
    Compute cumulative returns over time (growth of $1 invested).

    Parameters:
        returns: pd.Series or pd.DataFrame of daily returns

    Returns:
        pd.Series or pd.DataFrame of cumulative returns
    """
    # Multiply (1 + daily return) cumulatively
    return (1 + returns).cumprod()


def max_drawdown(returns):
    """
    Compute maximum drawdown for each asset.

    Parameters:
        returns: pd.Series or pd.DataFrame of daily returns

    Returns:
        pd.Series with maximum drawdown (largest peak-to-trough drop) for each asset
    """
    # Compute cumulative returns
    cumulative = cumulative_returns(returns)
    
    # Track running peak values
    peak = cumulative.cummax()
    
    # Compute drawdown at each point: (current value - peak) / peak
    drawdown = (cumulative - peak) / peak
    
    # Return the most negative drawdown (largest loss)
    return drawdown.min()