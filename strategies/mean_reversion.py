import numpy as np

def mean_reversion_with_bands(data, window, z_threshold, rsi_low, rsi_high, ema_short, ema_long, atr_window, close_col, volume_filter=False):
    """
    Implements a mean reversion strategy with Bollinger Bands and trend filtering.
    """
    # Calculate rolling mean and standard deviation
    data['rolling_mean'] = data[close_col].rolling(window=window).mean()
    data['rolling_std'] = data[close_col].rolling(window=window).std()

    # Calculate z-score
    data['z_score'] = (data[close_col] - data['rolling_mean']) / data['rolling_std']

    # Calculate RSI
    delta = data[close_col].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Add EMAs
    data['EMA_short'] = data[close_col].ewm(span=ema_short, adjust=False).mean()
    data['EMA_long'] = data[close_col].ewm(span=ema_long, adjust=False).mean()

    # Calculate ATR
    if 'High' in data.columns and 'Low' in data.columns:
        data['TR'] = np.maximum(
            data['High'] - data['Low'],
            np.maximum(
                abs(data['High'] - data[close_col].shift()),
                abs(data['Low'] - data[close_col].shift())
            )
        )
        data['ATR'] = data['TR'].rolling(window=atr_window).mean()
    else:
        data['ATR'] = 1  # Default value if High and Low are not present

    # Trend filter
    data['Trend'] = np.where(data['EMA_short'] > data['EMA_long'], 1, -1)

    # Generate signals
    data['mean_reversion_signal'] = np.where(
        (data[close_col] < data['rolling_mean'] - z_threshold * data['rolling_std']) &
        (data['RSI'] < rsi_low) & (data['Trend'] == 1), 1,  # Long
        np.where(
            (data[close_col] > data['rolling_mean'] + z_threshold * data['rolling_std']) &
            (data['RSI'] > rsi_high) & (data['Trend'] == -1), -1,  # Short
            0  # Hold
        )
    )

    # Optional volume filter
    if volume_filter and 'Volume' in data.columns:
        volume_col = 'Volume'
        avg_volume = data[volume_col].rolling(window=window).mean()
        data['mean_reversion_signal'] = np.where(data[volume_col] < avg_volume * 0.5, 0, data['mean_reversion_signal'])

    return data

