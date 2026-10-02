from __future__ import annotations

import sys

from parts.eval import run
from parts.ingest import load_assets, load_bins, load_faults
from parts.policy import AssetNotFound
from parts.recommend import recommend


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        return run()
    asset_id = sys.argv[1] if len(sys.argv) > 1 else "AST-7"
    fault_code = sys.argv[2] if len(sys.argv) > 2 else "E42"
    try:
        result = recommend(load_assets(), load_faults(), load_bins(), asset_id, fault_code)
    except AssetNotFound:
        print(f"Unknown asset {asset_id}", file=sys.stderr)
        return 1
    print(result.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
