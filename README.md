# Helios field parts

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/parts/recommend.py`](src/parts/recommend.py) | Functions: `recommend` |
| [`src/parts/eval.py`](src/parts/eval.py) | Functions: `run` |
| [`src/parts/policy.py`](src/parts/policy.py) | Functions: `render` |
| [`src/parts/ingest.py`](src/parts/ingest.py) | Functions: `load_assets`, `load_faults`, `load_bins`, `load_cases` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/parts/__init__.py`](src/parts/__init__.py) | Implementation or supporting configuration |
| [`src/parts/__main__.py`](src/parts/__main__.py) | Functions: `main` |
| [`Dockerfile`](Dockerfile) | Container build/service configuration |
| [`tests/test_policy.py`](tests/test_policy.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |
| [`docs/01-discovery.md`](docs/01-discovery.md) | Project explanations or operating notes |
| [`docs/02-security.md`](docs/02-security.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

<!-- project-guide:end -->

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
