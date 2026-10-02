from __future__ import annotations

from pathlib import Path

from parts.ingest import load_assets, load_bins, load_cases, load_faults
from parts.recommend import recommend


def run(path: Path | None = None) -> int:
    assets, faults, bins = load_assets(), load_faults(), load_bins()
    failures = []
    cases = load_cases(path)
    for case in cases:
        result = recommend(assets, faults, bins, case["asset_id"], case["fault_code"])
        if result.status != case["expected_status"]:
            failures.append(f"{case['asset_id']} {case['fault_code']}: {result.status}")
        if case.get("expected_bin") and result.bin_id != case["expected_bin"]:
            failures.append(f"{case['asset_id']}: bin {result.bin_id}")
        if "purchase order" not in result.render().lower() and result.status != "escalate":
            failures.append(f"{case['asset_id']}: missing purchase-order refusal")
    if failures:
        print(f"{len(failures)} eval failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"{len(cases)} eval cases passed")
    return 0
