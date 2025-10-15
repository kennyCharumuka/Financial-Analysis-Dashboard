import yfinance as yf
import pandas_datareader as pdr
import pandas as pd
from pathlib import Path


def download_data(qqq_ticker: str = "QQQ", start: str = "1999-01-01", out_dir: str = None):
    """
    Downloads historical data for `qqq_ticker` from Yahoo Finance and
    the Federal Funds Rate from FRED and writes CSVs into `out_dir` (repo root by default).

    Returns tuple of file paths written: (qqq_csv_path, fed_csv_path)
    """
    out_path = Path(out_dir) if out_dir else Path(".")
    out_path = out_path.resolve()

    # Download QQQ data (explicit auto_adjust to avoid FutureWarning)
    qqq_df = yf.download(qqq_ticker, start=start, auto_adjust=False)
    qqq_csv = out_path / "qqq.csv"
    qqq_df.to_csv(qqq_csv)

    # Download Federal Funds Rate data
    fed_funds_df = pdr.get_data_fred("FEDFUNDS", start=start)
    fed_csv = out_path / "fed_funds_rate.csv"
    fed_funds_df.to_csv(fed_csv)

    return str(qqq_csv), str(fed_csv)


if __name__ == "__main__":
    download_data()
