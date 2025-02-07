import numpy as np

def breakout_strategy(data, breakout_window=20, close_col="Close"):
    """
    Breakout strategy based on recent highs and lows.
    """
    # Calculate recent highs and lows
    data['recent_high'] = data[close_col].rolling(window=breakout_window).max()
    data['recent_low'] = data[close_col].rolling(window=breakout_window).min()

    # Generate buy/sell signals
    data['momentum_signal'] = np.where(data[close_col] > data['recent_high'], 1,  # Long
                                       np.where(data[close_col] < data['recent_low'], -1, 0))  # Short or Hold

    # Clean up signals for missing values
    data['momentum_signal'] = data['momentum_signal'].fillna(0)

    return data

