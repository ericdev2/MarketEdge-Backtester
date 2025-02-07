import matplotlib.pyplot as plt

def plot_equity_curve(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['portfolio_value'], label="Portfolio Value")
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.show()