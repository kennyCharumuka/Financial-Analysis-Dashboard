from pathlib import Path
from Scripts.qqq_prepare_and_run_correlation import create_clean_qqq, run_correlation


def calculate_correlation():
    """Ensure clean qqq CSV exists and compute the correlation.

    Returns (merged_df, correlation)
    """
    repo_root = Path(__file__).resolve().parents[1]
    qqq_clean = repo_root / 'qqq_clean.csv'
    qqq_raw = repo_root / 'qqq.csv'

    if not qqq_clean.exists():
        if qqq_raw.exists():
            create_clean_qqq(str(qqq_raw.name), str(qqq_clean.name))
        else:
            raise FileNotFoundError('qqq.csv not found; run the downloader')

    merged, corr = run_correlation(str(qqq_clean), str(repo_root / 'fed_funds_rate.csv'))
    return merged, corr
