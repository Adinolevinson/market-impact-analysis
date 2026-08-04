import pandas as pd
import yfinance as yf


def download_stock_data(ticker, start_date, end_date):

    stock = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    # Remove ticker level if yfinance returns MultiIndex columns
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    # Turn Date index into a normal column
    stock = stock.reset_index()

    # Make sure Date is datetime
    stock["Date"] = pd.to_datetime(stock["Date"])

    # Keep required columns
    stock = stock[
        ["Date", "Close", "High", "Low", "Open", "Volume"]
    ]

    return stock