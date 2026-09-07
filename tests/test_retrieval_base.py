from netrag.retrieval.base import MetadataFilter


def test_filter_expr_and():
    f = MetadataFilter(vendor="cisco", sw_version="17.9")
    assert f.to_milvus_expr() == 'vendor == "cisco" and sw_version == "17.9"'


def test_filter_expr_none():
    assert MetadataFilter().to_milvus_expr() is None
