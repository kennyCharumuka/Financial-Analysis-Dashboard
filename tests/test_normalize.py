import os
from pathlib import Path
from Scripts.normalize_qqq import normalize_qqq_csv


def test_normalize_qqq_exists(tmp_path):
    # Copy the existing qqq.csv into tmp_path and run normalization
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "qqq.csv"
    dst = tmp_path / "qqq.csv"
    with src.open("r", encoding="utf-8") as fsrc:
        dst.write_text(fsrc.read(), encoding="utf-8")

    normalized = normalize_qqq_csv(str(dst))
    assert Path(normalized).exists()
    # Ensure only one header line at the top
    with open(normalized, "r", encoding="utf-8") as f:
        first = f.readline().strip()
        second = f.readline().strip()
    assert first != second  # header should not repeat
