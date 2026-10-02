# Helios field parts

Simulated forward deployed engagement for Helios Equipment. Depot techs at a site with no reliable uplink were guessing spare parts from a PDF. The depot lead will not let the tool create a purchase order, and the catalog cannot call a vendor API.

## What the tech gets

| Asset | Fault | Result |
| --- | --- | --- |
| AST-7 HX-200 | E42 | Pull BRG-19 from bin B-14, the bin with quantity 2. B-02 is empty and is not chosen |
| AST-3 HX-90 | E17 | FLT-3 is a stockout. No purchase order |
| AST-8 HX-200 | E99 | Not on the signed fault list. Escalate. No guessed part |

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest
python -m parts eval
python -m parts AST-7 E42
```

## Docs

- [Discovery](docs/01-discovery.md)
- [Security](docs/02-security.md)
- [Readout](docs/03-readout.md)

The pilot does not claim less downtime. It claims the recommended bin has quantity, and an unknown fault does not invent a SKU.
