import yfinance as yf
import pandas_datareader as pdr
import pandas as pd

def download_data():
    """
    Downloads historical data for QQQ from Yahoo Finance and
    the Federal Funds Rate from FRED.
    """
    # Download QQQ data
    qqq_df = yf.download('QQQ', start='1999-01-01')
    qqq_df.to_csv('qqq.csv')
    print("QQQ data downloaded and saved to qqq.csv")

    # Download Federal Funds Rate data
    fed_funds_df = pdr.get_data_fred('FEDFUNDS', start='1999-01-01')
    fed_funds_df.to_csv('fed_funds_rate.csv')
    print("Federal Funds Rate data downloaded and saved to fed_funds_rate.csv")

if __name__ == '__main__':
    download_data()
