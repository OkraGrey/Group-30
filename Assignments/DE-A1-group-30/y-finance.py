import yfinance as yf
import pandas as pd

def collect_yfinance_data():
    tickers = ["ZM", "MSFT", "CRM", "GOOGL", "DBX", "XLK"]
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")
        data[ticker] = hist["Close"]
    df_yfinance = pd.DataFrame(data)
    df_yfinance = df_yfinance.dropna()
    df_yfinance.to_csv("datasets/raw/yfinance.csv")
    print("Yahoo Finance data collected, cleaned and stored")

def summarize_yfinance_data():
    df_yfinance = pd.read_csv("datasets/raw/yfinance.csv", index_col="Date", parse_dates=True)
    print("\nFirst 5 rows:")
    print(df_yfinance.head())
    print("\nSummary statistics for numeric columns:")
    print(df_yfinance.describe())
    print("\nStock performance over time:")
    for ticker in df_yfinance.columns:
        print(f"{ticker}:")
        print(f"  - Initial price: {df_yfinance[ticker].iloc[0]:.2f}")
        print(f"  - Final price: {df_yfinance[ticker].iloc[-1]:.2f}")
        print(f"  - Percentage change: {(df_yfinance[ticker].iloc[-1] - df_yfinance[ticker].iloc[0]) / df_yfinance[ticker].iloc[0] * 100:.2f}%")

if __name__ == "__main__":
    print("Collecting, cleaning and storing Yahoo Finance data")
    collect_yfinance_data()
    summarize_yfinance_data()