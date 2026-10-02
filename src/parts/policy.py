from __future__ import annotations

from dataclasses import dataclass


class AssetNotFound(KeyError):
    pass


@dataclass(frozen=True)
class Asset:
    asset_id: str
    model: str
    site: str


@dataclass(frozen=True)
class Fault:
    fault_code: str
    model: str
    sku: str
    step: str


@dataclass(frozen=True)
class Bin:
    sku: str
    bin_id: str
    qty: int


@dataclass(frozen=True)
class Recommendation:
    asset_id: str
    status: str
    sku: str | None
    bin_id: str | None
    step: str | None
    citations: tuple[str, ...]

    def render(self) -> str:
        if self.status == "recommend":
            action = f"Pull {self.sku} from bin {self.bin_id}. {self.step} This does not create a purchase order."
        elif self.status == "stockout":
            action = f"{self.sku} has no bin with quantity above zero. Do not create a purchase order from this screen."
        else:
            action = "Fault is not on the signed list for this model. Escalate to the depot lead. Do not guess a part."
        cites = "\n".join(f"- {citation}" for citation in self.citations)
        return f"Asset {self.asset_id} status: {self.status}.\n{action}\nCitations:\n{cites}\n"
