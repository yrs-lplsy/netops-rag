from netrag.eval.metrics import mrr, recall_at_k


def test_recall_hit_and_miss():
    ranked = [["a", "b"], ["c", "d"]]
    expected = [["b"], ["z"]]
    assert recall_at_k(ranked, expected, k=2) == 0.5


def test_recall_k_truncates():
    assert recall_at_k([["a", "b", "c"]], [["c"]], k=2) == 0.0


def test_mrr():
    ranked = [["x", "a"], ["a"]]
    assert mrr(ranked, [["a"], ["a"]]) == (1 / 2 + 1 / 1) / 2


def test_mrr_no_hit():
    assert mrr([["x"]], [["y"]]) == 0.0
