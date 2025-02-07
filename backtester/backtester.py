import pandas as pd
import numpy as np

def backtest(data, close_col="close", fee=0.001):
    """
    Backtesting function for a trading strategy.

    Parameters:
        data (pd.DataFrame): Data with 'signal' column indicating buy/sell/hold signals (1, -1, 0).
        close_col (str): Name of the column representing the close price.
        fee (float): Transaction fee percentage (e.g., 0.001 for 0.1%).

    Returns:
        pd.DataFrame: Data with added portfolio value and trade statistics.
    """
    # Initialize variables
    initial_balance = 10000  # Starting balance
    balance = initial_balance
    position = 0  # Current holdings
    data['portfolio_value'] = balance

    # Track trades
    for idx in range(len(data)):
        signal = data['signal'].iloc[idx]
        price = data[close_col].iloc[idx]

        if signal == 1:  # Buy signal
            if position == 0:  # Only buy if no position is held
                # Use all available balance to buy (minus fees)
                position = (balance * (1 - fee)) / price
                balance = 0  # No cash left after buying

        elif signal == -1:  # Sell signal (or short)
            if position > 0:  # Only sell if holding a long position
                # Sell all holdings (minus fees)
                balance = position * price * (1 - fee)
                position = 0  # No holdings left

        # Update portfolio value (cash + holdings)
        data.loc[data.index[idx], 'portfolio_value'] = balance + (position * price if position > 0 else 0)

    # Calculate returns
    data['daily_returns'] = data['portfolio_value'].pct_change()

    # Calculate performance metrics
    final_balance = data['portfolio_value'].iloc[-1]
    total_trades = len(data[data['signal'] != 0])
    total_return = (final_balance - initial_balance) / initial_balance * 100
    sharpe_ratio = (
        data['daily_returns'].mean() / data['daily_returns'].std() * np.sqrt(252)
        if data['daily_returns'].std() > 0 else 0
    )

    # Print summary
    print(f"Backtest Complete:")
    print(f"Initial Portfolio Value: ${initial_balance:.2f}")
    print(f"Final Portfolio Value: ${final_balance:.2f}")
    print(f"Total Trades: {total_trades}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    return data

