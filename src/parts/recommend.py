from __future__ import annotations

from parts.policy import Asset, AssetNotFound, Bin, Fault, Recommendation


def recommend(assets: dict[str, Asset], faults: list[Fault], bins: list[Bin], asset_id: str, fault_code: str) -> Recommendation:
    try:
        asset = assets[asset_id]
    except KeyError as exc:
        raise AssetNotFound(asset_id) from exc
    match = next((fault for fault in faults if fault.fault_code == fault_code and fault.model == asset.model), None)
    if match is None:
        return Recommendation(asset_id, "escalate", None, None, None, (f"data/assets.csv#{asset_id}",))
    stocked = [bin_row for bin_row in bins if bin_row.sku == match.sku and bin_row.qty > 0]
    citations = (f"data/faults.csv#{fault_code}", f"data/assets.csv#{asset_id}")
    if not stocked:
        empty = [bin_row.bin_id for bin_row in bins if bin_row.sku == match.sku]
        cites = citations + tuple(f"data/stock.csv#{bin_id}" for bin_id in empty)
        return Recommendation(asset_id, "stockout", match.sku, None, None, cites)
    chosen = max(stocked, key=lambda bin_row: bin_row.qty)
    return Recommendation(
        asset_id,
        "recommend",
        match.sku,
        chosen.bin_id,
        match.step,
        citations + (f"data/stock.csv#{chosen.bin_id}",),
    )
