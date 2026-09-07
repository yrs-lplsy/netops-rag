"""审批门单测：完整生命周期、错误 token、一次性消费、坏行容错。

全离线：审批记录落 tmp_path，不碰真实 data/approvals.jsonl。
"""

import json
import threading

import pytest

from netrag.tools_mcp import approval


@pytest.fixture()
def store(tmp_path):
    return tmp_path / "approvals.jsonl"


def test_full_lifecycle_pending_approved_consumed(store):
    rid = approval.request_approval("acc1", ["interface eth0", "description X"], path=store)
    assert rid and store.exists()

    # pending 阶段：token 不可消费
    rec = approval.get(rid, path=store)
    assert rec["status"] == "pending"
    assert rec["host"] == "acc1"
    assert rec["planned_lines"] == ["interface eth0", "description X"]
    assert "token" not in rec  # token 绝不落盘明文
    assert approval.consume_token(rid, "anything", path=store) is False

    token = approval.approve(rid, "ops-admin", path=store)
    assert token  # 一次性明文 token 只返回这一次

    # 错误 token 拒绝且不改变状态
    assert approval.consume_token(rid, "wrong-token", path=store) is False
    assert approval.get(rid, path=store)["status"] == "approved"

    # 正确 token 恰好消费一次
    assert approval.consume_token(rid, token, path=store) is True
    assert approval.get(rid, path=store)["status"] == "consumed"

    # 双花拒绝
    assert approval.consume_token(rid, token, path=store) is False


def test_token_stored_hashed_not_plaintext(store):
    rid = approval.request_approval("core1", ["router ospf"], path=store)
    token = approval.approve(rid, "ops", path=store)
    raw = store.read_text(encoding="utf-8")
    assert token not in raw
    assert approval.get(rid, path=store)["token_hash"]  # sha256 落盘


def test_reapprove_rotates_token(store):
    rid = approval.request_approval("core1", ["!"], path=store)
    t1 = approval.approve(rid, "a", path=store)
    t2 = approval.approve(rid, "b", path=store)
    assert t1 != t2
    assert approval.consume_token(rid, t1, path=store) is False  # 旧 token 失效
    assert approval.consume_token(rid, t2, path=store) is True


def test_append_only_history_preserved(store):
    rid = approval.request_approval("core1", ["!"], path=store)
    token = approval.approve(rid, "ops", path=store)
    approval.consume_token(rid, token, path=store)
    lines = [json.loads(l) for l in store.read_text().splitlines() if l.strip()]
    assert len(lines) == 3  # pending → approved → consumed 审计链（追加式，不改写旧行）
    assert [r["status"] for r in lines if r["approval_id"] == rid] == [
        "pending", "approved", "consumed"]


def test_unknown_approval_id(store):
    with pytest.raises(ValueError, match="unknown approval_id"):
        approval.approve("nope", "ops", path=store)
    with pytest.raises(ValueError, match="unknown approval_id"):
        approval.get("nope", path=store)


def test_malformed_jsonl_tolerated(store):
    store.write_text(
        "not json at all\n"
        + json.dumps({"approval_id": "x1", "status": "pending", "host": "h",
                      "planned_lines": [], "ts": "2026-01-01T00:00:00Z"}) + "\n"
        + '{"broken": \n',
        encoding="utf-8",
    )
    assert approval.get("x1", path=store)["status"] == "pending"
    rid = approval.request_approval("h", ["!"], path=store)  # 追加不受坏行影响
    token = approval.approve(rid, "ops", path=store)
    assert approval.consume_token(rid, token, path=store) is True
    # 坏行仍在文件里（只跳过不修复，保留现场）
    assert "not json at all" in store.read_text(encoding="utf-8")


def test_consume_requires_approved_status(store):
    rid = approval.request_approval("h", ["!"], path=store)
    assert approval.consume_token(rid, "", path=store) is False


def test_verify_token_checks_without_consuming(store):
    rid = approval.request_approval("h", ["!"], path=store)
    token = approval.approve(rid, "ops", path=store)
    # pending 阶段不可验证
    rid_pending = approval.request_approval("h", ["!"], path=store)
    assert approval.verify_token(rid_pending, "x", path=store) is False
    # approved/consumed 均可验证（供同一变更的后续动作复用），且验证不改变状态
    assert approval.verify_token(rid, token, path=store) is True
    assert approval.consume_token(rid, token, path=store) is True
    assert approval.verify_token(rid, token, path=store) is True  # 已消费仍可验证
    assert approval.verify_token(rid, "wrong", path=store) is False


# ---------------------------------------------------------------------------
# token ↔ (host, planned_lines) 绑定（评审 Finding 1）
# ---------------------------------------------------------------------------

def test_consume_rejects_host_mismatch_and_does_not_consume(store):
    rid = approval.request_approval("acc1", ["interface eth1", "description X"],
                                    path=store)
    token = approval.approve(rid, "ops", path=store)
    # acc1 的良性变更 token 拿去 core1 → 拒绝且不被消费（token 未烧掉）
    assert approval.consume_token(rid, token, path=store, expected_host="core1") is False
    assert approval.get(rid, path=store)["status"] == "approved"
    assert approval.consume_token(rid, token, path=store,
                                  expected_host="acc1") is True  # 正确 host 仍可用


def test_consume_rejects_lines_mismatch_and_does_not_consume(store):
    rid = approval.request_approval("acc1", ["interface eth1", "description X"],
                                    path=store)
    token = approval.approve(rid, "ops", path=store)
    # 实际下发计划与登记不一致（含被改成危险行）→ 拒绝且不消费
    assert approval.consume_token(rid, token, path=store, expected_host="acc1",
                                  expected_lines=["interface eth1", "description Y"]) is False
    assert approval.consume_token(rid, token, path=store, expected_host="acc1",
                                  expected_lines=["no router ospf"]) is False
    assert approval.get(rid, path=store)["status"] == "approved"
    # 规范化等价（空白/空行/! 差异）视为同一计划
    assert approval.consume_token(rid, token, path=store, expected_host="acc1",
                                  expected_lines=["  interface eth1  ", "!",
                                                  "description X", ""]) is True


def test_verify_token_also_binds_host_and_lines(store):
    rid = approval.request_approval("acc1", ["description X"], path=store)
    token = approval.approve(rid, "ops", path=store)
    assert approval.verify_token(rid, token, path=store, expected_host="core1") is False
    assert approval.verify_token(rid, token, path=store, expected_host="acc1",
                                 expected_lines=["description X"]) is True
    assert approval.verify_token(rid, token, path=store, expected_host="acc1",
                                 expected_lines=["description X", "extra"]) is False


def test_concurrent_consume_single_winner(store):
    """fcntl.flock 串行化读改写：并发双花恰有一次成功（评审 Minor 3）。"""
    rid = approval.request_approval("h", ["!"], path=store)
    token = approval.approve(rid, "ops", path=store)
    n = 4
    barrier = threading.Barrier(n)
    results: list[bool] = []
    lock = threading.Lock()

    def worker():
        barrier.wait()
        ok = approval.consume_token(rid, token, path=store)
        with lock:
            results.append(ok)

    threads = [threading.Thread(target=worker) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results.count(True) == 1, results
    assert approval.get(rid, path=store)["status"] == "consumed"
