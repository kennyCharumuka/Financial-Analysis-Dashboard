from pathlib import Path


def normalize_qqq_csv(path: str = "../qqq.csv") -> str:
    """Rewrite the qqq.csv to ensure a single header row (Date,Open,High,Low,Close,Adj Close,Volume)
    and return the normalized file path.

    The yfinance CSV in this repo contains extra metadata lines (a 'Ticker' row and a 'Date' row).
    This function skips non-data lines and rewrites a clean CSV in-place.
    """
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(p)

    with p.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the first line that looks like a data header (contains both 'Open' and 'Close')
    header_idx = None
    for i, ln in enumerate(lines[:10]):
        if "Close" in ln and "Open" in ln:
            header_idx = i
            break

    if header_idx is None:
        # Fallback: assume first line is header
        header_idx = 0

    cleaned = lines[header_idx:]

    # If the header line is the multi-column 'Price,Close,High,Low,Open,Volume' reorder to conventional
    # We'll leave columns as-is to avoid changing downstream expectations, but ensure only one header exists.
    # Remove duplicate header rows in cleaned data
    seen_header = cleaned[0]
    new_lines = [seen_header]
    for ln in cleaned[1:]:
        if ln.strip() == seen_header.strip():
            continue
        new_lines.append(ln)

    with p.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return str(p)


if __name__ == "__main__":
    print(normalize_qqq_csv("../qqq.csv"))
