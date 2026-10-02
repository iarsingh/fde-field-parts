from __future__ import annotations

import csv
import json
from pathlib import Path

from parts.policy import Asset, Bin, Fault

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EVALS_PATH = ROOT / "evals" / "questions.jsonl"


def load_assets() -> dict[str, Asset]:
    assets = {}
    with (DATA_DIR / "assets.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            asset = Asset(row["asset_id"], row["model"], row["site"])
            assets[asset.asset_id] = asset
    return assets


def load_faults() -> list[Fault]:
    with (DATA_DIR / "faults.csv").open(newline="") as handle:
        return [Fault(row["fault_code"], row["model"], row["sku"], row["step"]) for row in csv.DictReader(handle)]


def load_bins() -> list[Bin]:
    with (DATA_DIR / "stock.csv").open(newline="") as handle:
        return [Bin(row["sku"], row["bin"], int(row["qty"])) for row in csv.DictReader(handle)]


def load_cases(path: Path | None = None) -> list[dict]:
    return [json.loads(line) for line in (path or EVALS_PATH).read_text().splitlines() if line.strip()]
