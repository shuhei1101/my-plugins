"""`features/session/types.py` の単体テスト。"""
from __future__ import annotations

from inject_rules.features.session.types import SessionState

A = "https://example.com/a.md"


# =========================
# is_injected
# =========================


def test_is_injected():
    """注入済みの判定（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_injected(A)
    # 実行・検証
    assert state.is_injected(A) is True


def test_is_injected_when_not_injected():
    """未注入の判定（正常系）。"""
    # 準備
    state = SessionState()
    # 実行・検証
    assert state.is_injected(A) is False


def test_is_injected_when_partial():
    """部分注入中の判定（正常系）。"""
    # 準備: 続き位置だけ記録した状態
    state = SessionState()
    state.mark_partial(A, 100)
    # 実行・検証: 途中を完了と誤認しない
    assert state.is_injected(A) is False


# =========================
# offset_of
# =========================


def test_offset_of():
    """記録済み位置の取得（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_partial(A, 100)
    # 実行・検証
    assert state.offset_of(A) == 100


def test_offset_of_when_unset():
    """未記録の既定値（正常系）。"""
    # 準備
    state = SessionState()
    # 実行・検証
    assert state.offset_of(A) == 0


# =========================
# mark_injected
# =========================


def test_mark_injected():
    """注入済みの記録（正常系）。"""
    # 準備
    state = SessionState()
    # 実行
    state.mark_injected(A)
    # 検証
    assert state.is_injected(A) is True


def test_mark_injected_when_partial_exists():
    """続き位置の消去（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_partial(A, 100)
    # 実行
    state.mark_injected(A)
    # 検証: 完了後に続きが残らない
    assert state.offset_of(A) == 0


# =========================
# mark_partial
# =========================


def test_mark_partial():
    """続き位置の記録（正常系）。"""
    # 準備
    state = SessionState()
    # 実行
    state.mark_partial(A, 100)
    # 検証: 完了扱いにしない
    assert state.offset_of(A) == 100
    assert state.is_injected(A) is False


def test_mark_partial_when_overwrite():
    """位置の更新（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_partial(A, 100)
    # 実行
    state.mark_partial(A, 200)
    # 検証
    assert state.offset_of(A) == 200


# =========================
# mark_notified
# =========================


def test_mark_notified():
    """初回は送出要（正常系）。"""
    # 準備
    state = SessionState()
    # 実行・検証
    assert state.mark_notified("indexes_unset") is True
    assert "indexes_unset" in state.notified


def test_mark_notified_when_already_notified():
    """2 回目は送出不要（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_notified("indexes_unset")
    # 実行・検証
    assert state.mark_notified("indexes_unset") is False


def test_mark_notified_when_other_key():
    """別事象は独立（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_notified("indexes_unset")
    # 実行・検証: 事象ごとに 1 回ずつ出る
    assert state.mark_notified("index_missing") is True
