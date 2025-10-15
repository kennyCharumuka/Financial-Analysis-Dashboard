import sys
import pandas as pd
from pathlib import Path

# Ensure repo root is importable when running this module directly
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from Scripts.qqq_prepare_and_run_correlation import create_clean_qqq


def functional_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    df = (df.assign(all_time_high=lambda x: x['Adj Close'].cummax(),
                   all_time_low=lambda x: x['Adj Close'].cummin())
            .assign(drawdown=lambda x: (x['Adj Close'] - x['all_time_high']) / x['all_time_high']))

    max_drawdown = df['drawdown'].min()
    yoy_return = df['Adj Close'].resample('YE').ffill().pct_change().mean()

    return df, max_drawdown, yoy_return


# Helper to load clean qqq
def load_clean_qqq(repo_root: Path):
    qqq_clean = repo_root / 'qqq_clean.csv'
    qqq_raw = repo_root / 'qqq.csv'
    if not qqq_clean.exists():
        if qqq_raw.exists():
            create_clean_qqq(str(qqq_raw.name), str(qqq_clean.name))
        else:
            raise FileNotFoundError('qqq.csv not found; run the downloader')
    qqq_df = pd.read_csv(qqq_clean, parse_dates=['Date']).set_index('Date')
    if 'Adj Close' not in qqq_df.columns:
        if 'Close' in qqq_df.columns:
            qqq_df['Adj Close'] = qqq_df['Close']
        elif 'Price' in qqq_df.columns:
            qqq_df['Adj Close'] = qqq_df['Price']
        else:
            raise KeyError('Adj Close column missing from qqq data')
    return qqq_df


if __name__ == '__main__':
    # run a quick CLI analysis
    repo_root = Path(__file__).resolve().parents[1]
    df = load_clean_qqq(repo_root)
    analyzed_df, max_drawdown, avg_yoy = functional_analysis(df.copy())
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Average YOY Return: {avg_yoy:.2%}")
