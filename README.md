## Disclaimer
This tool is for educational and research purposes only. It does not constitute financial advice, investment recommendations, or trading strategies. Use at your own risk.

Trading Tool

Overview

This project is a backtesting framework for trading strategies, including Mean Reversion and Momentum-based strategies. It fetches financial data from Yahoo Finance, runs simulations, evaluates performance, and generates visualizations.

Features

Fetch real-time stock data using yfinance

Implement and test multiple trading strategies:

Mean Reversion: Buys assets when they are undervalued and sells when they are overvalued

Momentum Trading: Rides the trend by buying high and selling higher

Backtesting engine to evaluate historical performance

Performance analysis with key metrics

Data visualization for better insights

Installation

To set up the project, install the dependencies:

pip install -r requirements.txt

Usage

Run the main script to execute backtesting with predefined strategies:

Drag the folder to your desktop then type "cd desktop/MarketEdge-Backtester" or "cd desktop/MarketEdge-Backtester-main" (if you downloaded the zip file)

Run the program by typing "python3 main.py"

If you want to change the ticker open the "main.py" file and look for this section.

#Parameters
ticker = "BTC"

Change the ticker to any asset you want to use the program for.

Requirements

This project requires:

pandas

numpy

matplotlib

yfinance

Contributing

Feel free to open issues or pull requests to enhance the strategies or improve the backtesting engine.

License

This project is open-source and available under the MIT License.

