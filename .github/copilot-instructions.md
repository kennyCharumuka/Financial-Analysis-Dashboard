## Repository overview

This repository contains a small scripts folder used for downloading financial data. The main script is `Scripts/Data Downloader.py` which:
- Uses `yfinance` to download historical data for the ticker `QQQ` (from 1999-01-01)
- Uses `pandas_datareader` to fetch the `FEDFUNDS` series from FRED
- Writes two CSVs to the repository root: `qqq.csv` and `fed_funds_rate.csv`

## Big-picture architecture and purpose

- This is a single-purpose data acquisition utility (not a service or library). The goal is to fetch raw data files for later analysis.
- There's no package or module structure; scripts are run directly.

## Important files

- `Scripts/Data Downloader.py` — entrypoint. Look here for data sources, date ranges, and output file names.

## Developer workflows (how to run and debug)

- Requirements: Python 3.8+ (assumed). Primary dependencies: `yfinance`, `pandas_datareader`, `pandas`.
- To run locally (PowerShell):

```powershell
python "Scripts/Data Downloader.py"
```

- The script writes `qqq.csv` and `fed_funds_rate.csv` into the repository root. When modifying the script, maintain these file names unless you update downstream consumers.

## Project-specific conventions and patterns

- Filenames may contain spaces (`Data Downloader.py`). When referencing files in code or commands, quote paths or rename the file if changing to avoid shell issues.
- The script uses direct top-level execution via `if __name__ == '__main__':` — treat it as the project's single CLI entry.

## External integrations

- Yahoo Finance via `yfinance` for equities data. Network access is required.
- FRED via `pandas_datareader` for macro series `FEDFUNDS`.

## Code changes guidance for AI agents

- Preserve the output CSV names and header formats to avoid breaking downstream analysis.
- If adding new tickers or series, add clear constants near the top of `Scripts/Data Downloader.py` and document them in comments.
- If splitting into modules, ensure the `download_data()` function remains callable and the CLI behavior is preserved.

## Example edits and patterns

- Adding a new ticker: append a new `yf.download(...)` call and write to `ticker.csv`.
- Changing date ranges: update the `start` argument in both `yf.download` and `pdr.get_data_fred` calls.

## Tests and linting

- This repository currently has no test harness or lint setup. Small edits should be verified by running the script and checking the generated CSVs.

## When to ask for clarification

- If modifications add new files, ask where outputs should be stored.
- If adding dependency changes, confirm that the environment used by the project supports installing packages (or request a `requirements.txt`).

If you'd like, I can:
- Rename `Data Downloader.py` to `data_downloader.py` and add a `requirements.txt`.
- Add a quick smoke test that validates the CSV outputs.

Please tell me which of the optional actions you'd prefer to have next.
