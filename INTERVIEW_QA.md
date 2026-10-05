# fde-field-parts — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-field-parts address, and what can you demonstrate?

Simulated forward deployed engagement for Helios Equipment. Depot techs at a site with no reliable uplink were guessing spare parts from a PDF. The depot lead will not let the tool create a purchase order, and the catalog cannot call a vendor API.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/parts/recommend.py`](src/parts/recommend.py): Implementation or supporting configuration.
- [`src/parts/eval.py`](src/parts/eval.py): Implementation or supporting configuration.
- [`src/parts/policy.py`](src/parts/policy.py): Implementation or supporting configuration.
- [`src/parts/ingest.py`](src/parts/ingest.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/parts/__init__.py`](src/parts/__init__.py): Implementation or supporting configuration.
- [`src/parts/__main__.py`](src/parts/__main__.py): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `recommend` and explain the decision it makes?

The main walkthrough here is `recommend(assets: dict[str, Asset], faults: list[Fault], bins: list[Bin], asset_id: str, fault_code: str)` in [`src/parts/recommend.py`](src/parts/recommend.py#L6).

```python
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
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `AssetNotFound`, `Recommendation`, `max`, `next`, `tuple`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `run` have?

`run(path: Path | None=None)` is defined in [`src/parts/eval.py`](src/parts/eval.py#L9).

Its return expressions include:

- `0`
- `1`

It uses `case.get`, `failures.append`, `len`, `load_assets`, `load_bins`, `load_cases`, `load_faults`, `print`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `SystemExit(main())` in [`src/parts/__main__.py`](src/parts/__main__.py#L26).
- `AssetNotFound(asset_id)` in [`src/parts/recommend.py`](src/parts/recommend.py#L10).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_policy.py`](tests/test_policy.py#L6) contains `test_eval_file_passes`:

```python
def test_eval_file_passes():
    assert run(EVALS_PATH) == 0
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. How do you separate the current design from a future production design?

The current design is the source/component map in [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md). A future deployment needs explicit input contracts, persistence decisions, authentication, monitoring, and rollback. I would present these as proposed work until the corresponding implementation and verification exist.

## 8. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `recommend`?

In [`src/parts/recommend.py`](src/parts/recommend.py#L6), `recommend(assets: dict[str, Asset], faults: list[Fault], bins: list[Bin], asset_id: str, fault_code: str)` receives the inputs. The function computes these intermediate values:

- `match = next((fault for fault in faults if fault.fault_code == fault_code and fault.model == asset.model), None)`
- `stocked = [bin_row for bin_row in bins if bin_row.sku == match.sku and bin_row.qty > 0]`
- `citations = (f'data/faults.csv#{fault_code}', f'data/assets.csv#{asset_id}')`
- `chosen = max(stocked, key=lambda bin_row: bin_row.qty)`

Its result is defined by:

- `Recommendation(asset_id, 'recommend', match.sku, chosen.bin_id, match.step, citations + (f'data/stock.csv#{chosen.bin_id}',))`
- `Recommendation(asset_id, 'escalate', None, None, None, (f'data/assets.csv#{asset_id}',))`
- `Recommendation(asset_id, 'stockout', match.sku, None, None, cites)`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/parts/recommend.py`](src/parts/recommend.py#L6) branches on:

- `match is None`
- `not stocked`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
