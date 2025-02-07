import pandas as pd
import matplotlib.pyplot as plt
from utils.data_fetcher import fetch_minute_data
from strategies.mean_reversion import mean_reversion_with_bands
from strategies.momentum import breakout_strategy
from backtester.backtester import backtest

def main():
    print("Starting the main script...")

    # Parameters
    ticker = "BTC"
    currency = "USD"
    total_points = 2000  # Total data points to fetch
    interval = "minute"  # Fetch minute data

    # Fetch historical data
    print(f"Fetching data for {ticker}-{currency} from CryptoCompare...")
    data = fetch_minute_data(symbol=ticker, currency=currency, limit=total_points)

    print(f"Fetched data sample:\n{data.head()}")

    # Ensure column naming consistency
    close_col = "close"

    # Apply mean reversion strategy
    print("Applying mean reversion strategy with Bollinger Bands...")
    data = mean_reversion_with_bands(
        data=data,
        window=15,
        z_threshold=1.2,
        rsi_low=30,
        rsi_high=70,
        ema_short=7,
        ema_long=21,
        atr_window=10,
        close_col=close_col,
        volume_filter=True
    )

    # Apply breakout strategy
    print("Applying breakout strategy...")
    data = breakout_strategy(data, breakout_window=20, close_col=close_col)

    # Combine signals
    print("Combining signals...")
    data['signal'] = data[['mean_reversion_signal', 'momentum_signal']].sum(axis=1).clip(-1, 1)
    print(f"Signal column:\n{data['signal'].value_counts()}")

    # Backtest the combined strategy
    print("Starting backtest...")
    data = backtest(data, close_col=close_col)

    # Annotate and print the last 5 days of signals
    annotated_data = data[[close_col, 'z_score', 'RSI', 'signal']].tail().copy()
    annotated_data['z_score_annotation'] = pd.cut(
        annotated_data['z_score'],
        bins=[-float('inf'), -1.5, 1.5, float('inf')],
        labels=['(bullish)', '(neutral)', '(bearish)']
    )
    annotated_data['RSI_annotation'] = pd.cut(
        annotated_data['RSI'],
        bins=[0, 30, 70, 100],
        labels=['(oversold)', '(neutral)', '(overbought)']
    )
    annotated_data['signal_annotation'] = annotated_data['signal'].map({1: '(buy)', -1: '(sell)', 0: '(hold)'})
    print("\nAnnotated signals for the last 5 rows:")
    print(
        annotated_data.to_string(
            formatters={
                close_col: '{:.6f}'.format,
                'z_score': '{:.6f}'.format,
                'RSI': '{:.6f}'.format,
            },
            columns=[
                close_col, 'z_score', 'z_score_annotation',
                'RSI', 'RSI_annotation', 'signal', 'signal_annotation'
            ],
            index=True
        )
    )

    # Plot portfolio value with buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['portfolio_value'], label='Portfolio Value', color='blue')
    buy_signals = data[data['signal'] == 1]
    sell_signals = data[data['signal'] == -1]
    plt.scatter(buy_signals.index, buy_signals['portfolio_value'], label='Buy Signal', color='green', marker='^', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['portfolio_value'], label='Sell Signal', color='red', marker='v', alpha=1)
    plt.title(f"Portfolio Value Over Time ({ticker}-{currency})")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot Z-Score with buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['z_score'], label='Z-Score', color='green')
    plt.axhline(y=1.5, color='red', linestyle='--', label='Upper Threshold')
    plt.axhline(y=-1.5, color='red', linestyle='--', label='Lower Threshold')
    plt.scatter(buy_signals.index, buy_signals['z_score'], label='Buy Signal', color='green', marker='^', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['z_score'], label='Sell Signal', color='red', marker='v', alpha=1)
    plt.title(f"Z-Score Over Time ({ticker}-{currency})")
    plt.xlabel("Date")
    plt.ylabel("Z-Score")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot price with buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[close_col], label='Price', color='blue')
    plt.scatter(buy_signals.index, buy_signals[close_col], label='Buy Signal', color='green', marker='^', alpha=1)
    plt.scatter(sell_signals.index, sell_signals[close_col], label='Sell Signal', color='red', marker='v', alpha=1)
    plt.title(f"Price with Buy/Sell Signals ({ticker}-{currency})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

    # Save the final dataset to a CSV for further analysis
    output_file = f"backtest_results_{ticker}-{currency}.csv"
    data.to_csv(output_file)
    print(f"Backtest results saved to {output_file}")

if __name__ == "__main__":
    main()

