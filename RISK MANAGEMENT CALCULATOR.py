import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def risk_calculator(tickers, start_date, end_date, confidence_level, risk_free_rate):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

    if data.empty:
        raise ValueError("No data fetched. Please check the stock tickers and date range.")

    returns = data.pct_change().dropna()

    if returns.empty:
        raise ValueError("Insufficient data to calculate returns.")

    portfolio_return = returns.mean() * 252
    portfolio_std = returns.std() * np.sqrt(252)

    z_score = norm.ppf(confidence_level)

    VaR = -(portfolio_return - z_score * portfolio_std)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std

    return VaR, sharpe_ratio, data, returns


def calculate_risk():
    try:
        tickers = [ticker.strip() for ticker in tickers_entry.get().split(',')]
        if not tickers or any(not ticker for ticker in tickers):
            raise ValueError("Stock tickers cannot be empty.")

        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        confidence_level = float(confidence_level_entry.get())
        risk_free_rate = float(risk_free_rate_entry.get())

        if not (0 < confidence_level < 1):
            raise ValueError("Confidence level must be between 0 and 1.")

        VaR, sharpe_ratio, data, returns = risk_calculator(tickers, start_date, end_date, confidence_level,
                                                           risk_free_rate)
        result_text.set(f"Value at Risk (VaR): {VaR:.2f}\nSharpe Ratio: {sharpe_ratio:.2f}")

        plot_graph(data, returns)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def plot_graph(data, returns):
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    data.plot(ax=ax[0])
    ax[0].set_title("Stock Prices")
    ax[0].set_ylabel("Price")

    returns.plot(ax=ax[1])
    ax[1].set_title("Stock Returns")
    ax[1].set_ylabel("Return")

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.draw()
    canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)


app = tk.Tk()
app.title("Risk Management Calculator")

ttk.Label(app, text="Stock Tickers (comma separated):").grid(row=0, column=0, padx=10, pady=5)
tickers_entry = ttk.Entry(app)
tickers_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(app, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
start_date_entry = ttk.Entry(app)
start_date_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(app, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
end_date_entry = ttk.Entry(app)
end_date_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(app, text="Confidence Level (0-1):").grid(row=3, column=0, padx=10, pady=5)
confidence_level_entry = ttk.Entry(app)
confidence_level_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(app, text="Risk-Free Rate (e.g., 0.01):").grid(row=4, column=0, padx=10, pady=5)
risk_free_rate_entry = ttk.Entry(app)
risk_free_rate_entry.grid(row=4, column=1, padx=10, pady=5)

calculate_button = ttk.Button(app, text="Calculate Risk", command=calculate_risk)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

result_text = tk.StringVar()
result_label = ttk.Label(app, textvariable=result_text)
result_label.grid(row=6, column=0, columnspan=2, pady=10)

app.mainloop()