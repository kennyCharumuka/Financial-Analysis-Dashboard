import sys
import pandas as pd
from pathlib import Path

# Ensure repository root is on sys.path so `Scripts` package imports work when running this file directly
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from Scripts.qqq_prepare_and_run_correlation import create_clean_qqq


def functional_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """
    Performs a functional analysis on the QQQ dataframe to calculate
    all-time high, all-time low, max drawdown, and average YOY return.

    Args:
        df: The QQQ dataframe.

    Returns:
        A tuple containing the dataframe with new columns, the max drawdown,
        and the average YOY return.
    """
    df = (df.assign(all_time_high=lambda x: x['Adj Close'].cummax(),
                   all_time_low=lambda x: x['Adj Close'].cummin())
            .assign(drawdown=lambda x: (x['Adj Close'] - x['all_time_high']) / x['all_time_high']))

    max_drawdown = df['drawdown'].min()
    
    # Calculate YOY return
    # use 'YE' (year-end) to avoid pandas FutureWarning for 'Y'
    yoy_return = df['Adj Close'].resample('YE').ffill().pct_change().mean()

    return df, max_drawdown, yoy_return

def analyze_qqq():
    """
    Loads QQQ data and runs the functional analysis.
    """
    repo_root = Path(__file__).resolve().parents[1]
    qqq_clean = repo_root / 'qqq_clean.csv'
    qqq_raw = repo_root / 'qqq.csv'

    # If qqq_clean doesn't exist, try to create it from qqq.csv
    if not qqq_clean.exists():
        if qqq_raw.exists():
            print("Creating qqq_clean.csv from qqq.csv...")
            create_clean_qqq(str(qqq_raw.name), str(qqq_clean.name))
        else:
            raise FileNotFoundError('qqq.csv not found in repository root; run the downloader first')

    qqq_df = pd.read_csv(str(qqq_clean), parse_dates=['Date']).set_index('Date')

    # Ensure Adj Close column exists
    if 'Adj Close' not in qqq_df.columns:
        if 'Close' in qqq_df.columns:
            qqq_df['Adj Close'] = qqq_df['Close']
        elif 'Price' in qqq_df.columns:
            qqq_df['Adj Close'] = qqq_df['Price']
        else:
            raise KeyError('Adj Close column missing from qqq data')

    analyzed_df, max_drawdown, avg_yoy_return = functional_analysis(qqq_df.copy())
    
    print("QQQ Analysis:")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Average YOY Return: {avg_yoy_return:.2%}")

if __name__ == '__main__':
    analyze_qqq()
