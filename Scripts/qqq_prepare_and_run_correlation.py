import re
from pathlib import Path
import pandas as pd

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2},")


def create_clean_qqq(src_path: str = "../qqq.csv", dst_path: str = "../qqq_clean.csv") -> str:
    # Resolve paths relative to the repository root (two levels up from this script)
    repo_root = Path(__file__).resolve().parents[1]

    p_src = Path(src_path)
    p_dst = Path(dst_path)

    if not p_src.is_absolute():
        p_src = (repo_root / p_src).resolve()
    else:
        p_src = p_src.resolve()

    if not p_dst.is_absolute():
        p_dst = (repo_root / p_dst).resolve()
    else:
        p_dst = p_dst.resolve()

    if not p_src.exists():
        raise FileNotFoundError(p_src)

    lines = p_src.read_text(encoding="utf-8").splitlines()

    # find first data line
    data_start = None
    for i, ln in enumerate(lines):
        if DATE_RE.match(ln):
            data_start = i
            break
    if data_start is None:
        # fallback: try reading with pandas; if fails, raise
        raise ValueError("No data lines found in qqq.csv")

    # guess header line: look above data_start for first line containing alphabetic column names
    header_line = None
    for i in range(max(0, data_start - 3), data_start):
        if any(c.isalpha() for c in lines[i]):
            header_line = i
            break
    if header_line is None:
        header_line = 0

    raw_header = lines[header_line].strip()
    data_lines = lines[data_start:]
    cols = [c.strip() for c in raw_header.split(",")]

    # If the header does not include 'Date' but the data rows start with a date, insert 'Date'
    if not any(c.lower() == 'date' for c in cols):
        # test first data line for a leading YYYY-MM-DD,
        if DATE_RE.match(data_lines[0]):
            cols = ['Date'] + cols

    # Normalize columns: ensure 'Adj Close' exists. If not, map from 'Close' or 'Price'
    has_adj = any(c.lower() in ("adj close", "adj_close", "price") for c in cols)
    # We'll construct a new header that always starts with Date then 'Adj Close' then the rest (unique)
    # First, find index of 'Close' or 'Price' to grab values
    col_names = cols.copy()
    # Parse into list of lists
    parsed = [ln.split(",") for ln in data_lines]
    # Ensure consistent column counts by trimming/padding rows and padding header names
    max_cols = max(len(row) for row in parsed)
    for row in parsed:
        if len(row) < max_cols:
            row.extend([""] * (max_cols - len(row)))
        elif len(row) > max_cols:
            max_cols = len(row)
    # If header has fewer columns than max_cols, pad header names
    if len(col_names) < max_cols:
        col_names.extend([f"col_{i}" for i in range(len(col_names), max_cols)])
    # If header has more columns than rows, pad rows
    for row in parsed:
        if len(row) < len(col_names):
            row.extend([""] * (len(col_names) - len(row)))

    df = pd.DataFrame(parsed, columns=col_names)
    # treat first column as Date
    # Remove possible empty columns
    df = df.loc[:, ~df.columns.str.match(r"^Unnamed")] if any(df.columns.str.match(r"^Unnamed")) else df

    # Create 'Adj Close' if missing
    if 'Adj Close' not in df.columns:
        if 'Close' in df.columns:
            df['Adj Close'] = df['Close']
        elif 'Price' in df.columns:
            df['Adj Close'] = df['Price']
        else:
            # If neither exists, try to use first numeric column
            for c in df.columns:
                try:
                    pd.to_numeric(df[c].iloc[0])
                    df['Adj Close'] = df[c]
                    break
                except Exception:
                    continue

    # Rebuild a CSV with Date as first column and Adj Close and any numeric columns
    # Add header: Date,Adj Close,<others...>
    out_cols = ['Date']
    if 'Adj Close' in df.columns:
        out_cols.append('Adj Close')
    # include other existing columns except Date
    for c in df.columns:
        if c not in out_cols:
            out_cols.append(c)

    # Convert to proper types where possible
    for c in out_cols:
        if c != 'Date':
            df[c] = pd.to_numeric(df[c], errors='coerce')

    df.to_csv(p_dst, index=False, columns=out_cols)
    return str(p_dst)


def run_correlation(qqq_path: str = '../qqq_clean.csv', fed_path: str = '../fed_funds_rate.csv'):
    qqq = pd.read_csv(qqq_path, parse_dates=['Date'])
    qqq = qqq.set_index('Date')
    fed = pd.read_csv(fed_path, index_col='DATE', parse_dates=True)

    # Ensure Adj Close exists
    if 'Adj Close' not in qqq.columns:
        raise KeyError('Adj Close not in qqq data')

    # Resample to annual returns
    qqq_annual_returns = qqq['Adj Close'].resample('YE').ffill().pct_change().dropna()
    qqq_annual_returns.name = 'QQQ Annual Return'

    fed_annual_avg = fed['FEDFUNDS'].resample('YE').mean()
    fed_annual_avg.name = 'Average Fed Funds Rate'

    merged = pd.concat([qqq_annual_returns, fed_annual_avg], axis=1, join='inner')
    corr = merged['QQQ Annual Return'].corr(merged['Average Fed Funds Rate'])
    print(f"Correlation between QQQ Annual Return and Average Fed Funds Rate: {corr:.4f}")
    return merged, corr


if __name__ == '__main__':
    # Use repository-root-relative paths (the helper resolves these against repo root)
    clean = create_clean_qqq('qqq.csv', 'qqq_clean.csv')
    print(f"Created clean qqq at: {clean}")
    run_correlation(clean, 'fed_funds_rate.csv')
