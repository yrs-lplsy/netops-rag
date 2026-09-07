def _hit_rank(ranked: list[str], expected: list[str], k: int) -> int:
    for rank, rid in enumerate(ranked[:k], start=1):
        if rid in expected:
            return rank
    return 0


def recall_at_k(ranked: list[list[str]], expected: list[list[str]], k: int) -> float:
    if not ranked:
        return 0.0
    hits = sum(1 for r, e in zip(ranked, expected) if _hit_rank(r, e, k) > 0)
    return hits / len(ranked)


def mrr(ranked: list[list[str]], expected: list[list[str]]) -> float:
    if not ranked:
        return 0.0
    total = 0.0
    for r, e in zip(ranked, expected):
        rank = _hit_rank(r, e, len(r))
        if rank:
            total += 1 / rank
    return total / len(ranked)
