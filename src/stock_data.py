import yfinance as yf
import pandas as pd


def download_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Download historical stock-price data from Yahoo Finance."""
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
    )

    return data