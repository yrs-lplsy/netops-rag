class BgeTokenCounter:
    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        from transformers import AutoTokenizer

        self._tok = AutoTokenizer.from_pretrained(model_name)

    def count(self, text: str) -> int:
        return len(self._tok(text)["input_ids"])


class CachedTokenCounter:
    """带 memo 缓存的计数器：切分器对行/块重复计数（表头/命令行/页眉大量重复），
    大语料（数万页）下逐条 tokenize 是瓶颈，缓存可砍掉大头。"""

    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        self._inner = BgeTokenCounter(model_name)
        self._cache: dict[str, int] = {}

    def count(self, text: str) -> int:
        v = self._cache.get(text)
        if v is None:
            v = self._inner.count(text)
            self._cache[text] = v
        return v
