from parts.eval import run
from parts.ingest import EVALS_PATH, load_assets, load_bins, load_faults
from parts.recommend import recommend


def test_eval_file_passes():
    assert run(EVALS_PATH) == 0


def test_in_stock_bin_wins_and_no_purchase_order_is_created():
    result = recommend(load_assets(), load_faults(), load_bins(), "AST-7", "E42")
    assert result.bin_id == "B-14"
    assert result.sku == "BRG-19"
    rendered = result.render().lower()
    assert "does not create a purchase order" in rendered


def test_unknown_fault_does_not_guess_a_sku():
    result = recommend(load_assets(), load_faults(), load_bins(), "AST-8", "E99")
    assert result.status == "escalate"
    assert result.sku is None
