<<<<<<< HEAD
# Financial-Analysis-Dashboard
Analyzes correlation between U.S. Fed Funds Rate and NASDAQ-100 (QQQ) returns using Python, Pandas, DuckDB, Streamlit, and Plotly. Includes data download, functional programming for metrics (ATH, ATL, drawdown, YOY returns), and an interactive dashboard visualizing macro-financial trends.
=======
# Financial analysis dashboard
- `qqq.csv`, `qqq_clean.csv`, `fed_funds_rate.csv` — data files in repo root
# Financial analysis dashboard

This repository contains scripts to download market and macro data, normalize it, run analyses, and launch a Streamlit dashboard.

## Contents
- `Scripts/` — scripts and helpers (downloader, normalization, analysis, Streamlit app)
- `qqq.csv`, `qqq_clean.csv`, `fed_funds_rate.csv` — data files (repo root)
- `tests/` — pytest tests
- `requirements.txt` — Python dependencies
- `Dockerfile` — container image for the Streamlit app
- `.github/workflows/` — CI and publish workflows

## Quick start (PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Download data (writes `qqq.csv` and `fed_funds_rate.csv` to repo root):

```powershell
python "Scripts/Data Downloader.py"
# or the cleaner entrypoint
python Scripts/data_downloader.py
```

4. Normalize and run correlation / analysis (creates `qqq_clean.csv`):

```powershell
python Scripts/qqq_prepare_and_run_correlation.py
```

5. Run the functional analysis CLI (optional):

```powershell
python Scripts/functional_analysis.py
```

6. Launch the Streamlit dashboard:

```powershell
streamlit run "Scripts/Financial Analysis App.py"
```

7. Run tests (pytest):

```powershell
python -m pytest -q
```

## Troubleshooting
- If you see an error about `distutils` when importing `pandas_datareader`, run:

```powershell
python -m pip install --upgrade setuptools wheel
```

- Plotly trendlines require `statsmodels`; it's included in `requirements.txt`.

- If a script can't import `Scripts.*` modules when running directly, prefer running from the repository root. The code includes temporary `sys.path` insertions to make running scripts directly easier during development.

## Deployment

Repository name suggestion: `Financial analysis dashboard` (use this name for the GitHub repo if you like).

### Build & run locally with Docker

```powershell
# build
docker build -t financial-analysis-dashboard:latest .

# run (maps port 8501)
docker run -p 8501:8501 financial-analysis-dashboard:latest
```

### Publish image to GitHub Container Registry (GHCR)
- Push a tag (e.g., `v1.0.0`) to trigger `.github/workflows/publish-image.yml`.
- The workflow publishes to `ghcr.io/<your-username>/financial-analysis-dashboard:latest`.

### Streamlit Community Cloud
- Connect your GitHub repository in Streamlit Cloud and set the entrypoint to `Scripts/Financial Analysis App.py`.
- Ensure `requirements.txt` is present so dependencies are installed automatically.

## CI
- The CI workflow `.github/workflows/ci.yml` installs dependencies and runs `pytest` on pushes and PRs to `main`.

## Next steps (optional)
- Add `tasks.json` (VS Code) or a `Makefile` for convenient local commands.
- Convert repo to an installable package (`pyproject.toml`) to avoid `sys.path` insertion hacks.
- Add a mocked test for `data_downloader.py` to avoid network calls in CI.

If you'd like I can open a repo on your GitHub (you'll need to give me the repo name and confirm) and push these changes, or I can provide the exact git commands you can run locally to publish the project. Which would you prefer?
