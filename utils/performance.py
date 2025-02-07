import pandas as pd
import numpy as np

def calculate_performance_metrics(data, risk_free_rate=0.02):
    """
    Calculate key performance metrics for the backtested strategy.

    Parameters:
        data (pd.DataFrame): Data containing portfolio values and signals.
        risk_free_rate (float): Risk-free rate for Sharpe ratio calculation (default 2%).

    Returns:
        dict: A dictionary of performance metrics including Sharpe Ratio, total return, etc.
    """
    metrics = {}

    # Ensure 'portfolio_value' column exists
    if 'portfolio_value' not in data.columns:
        raise ValueError("DataFrame must contain 'portfolio_value' column.")

    # Calculate daily returns
    data['daily_returns'] = data['portfolio_value'].pct_change()

    # Total return
    initial_value = data['portfolio_value'].iloc[0]
    final_value = data['portfolio_value'].iloc[-1]
    total_return = (final_value - initial_value) / initial_value * 100
    metrics['Total Return (%)'] = total_return

    # Annualized return
    trading_days = 252 if 'hour' not in data.index.name.lower() else len(data) / 24
    annualized_return = ((1 + total_return / 100) ** (trading_days / len(data))) - 1
    metrics['Annualized Return (%)'] = annualized_return * 100

    # Annualized volatility
    annualized_volatility = data['daily_returns'].std() * np.sqrt(trading_days)
    metrics['Annualized Volatility (%)'] = annualized_volatility * 100

    # Sharpe Ratio
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    metrics['Sharpe Ratio'] = sharpe_ratio

    # Maximum Drawdown
    cumulative_max = data['portfolio_value'].cummax()
    drawdown = (data['portfolio_value'] - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min() * 100
    metrics['Max Drawdown (%)'] = max_drawdown

    # Display metrics
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    return metrics

# Example Usage:
# Assuming `data` is a DataFrame with a 'portfolio_value' column:
# metrics = calculate_performance_metrics(data)
# print(metrics)

