"""`features/session/store.py` の単体テスト。"""
from __future__ import annotations

from inject_rules.features.session.store import clear_state, load_state, save_state
from inject_rules.features.session.types import SessionState

SESSION = "9f2c1b"
A = "https://example.com/a.md"


# =========================
# load_state
# =========================


def test_load_state(tmp_path):
    """保存済み状態の復元（正常系）。"""
    # 準備: 3 キーが揃った状態を保存する
    state = SessionState()
    state.mark_injected(A)
    state.mark_partial("https://example.com/b.md", 100)
    state.mark_notified("indexes_unset")
    save_state(SESSION, state, base_dir=tmp_path)
    # 実行
    restored = load_state(SESSION, base_dir=tmp_path)
    # 検証
    assert restored.is_injected(A) is True
    assert restored.offset_of("https://example.com/b.md") == 100
    assert restored.mark_notified("indexes_unset") is False


def test_load_state_when_file_missing(tmp_path):
    """ファイルなし（正常系）。"""
    # 実行
    state = load_state("未作成のセッション", base_dir=tmp_path)
    # 検証: 空の状態
    assert state.injected == set()
    assert state.offsets == {}
    assert state.notified == set()


def test_load_state_when_broken_json(tmp_path):
    """壊れた JSON（正常系）。"""
    # 準備
    (tmp_path / f"{SESSION}.json").write_text("{壊れている", encoding="utf-8")
    # 実行
    state = load_state(SESSION, base_dir=tmp_path)
    # 検証: 例外を投げずに空の状態
    assert state.injected == set()


def test_load_state_when_unexpected_type(tmp_path):
    """型不一致キーの無視（正常系）。"""
    # 準備: injected が文字列
    (tmp_path / f"{SESSION}.json").write_text('{"injected": "文字列"}', encoding="utf-8")
    # 実行
    state = load_state(SESSION, base_dir=tmp_path)
    # 検証
    assert state.injected == set()


# =========================
# save_state
# =========================


def test_save_state(tmp_path):
    """保存と読み込みの往復（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_injected(A)
    state.mark_partial("https://example.com/b.md", 100)
    # 実行
    save_state(SESSION, state, base_dir=tmp_path)
    # 検証: 集合と配列の変換を経ても同一内容になる
    restored = load_state(SESSION, base_dir=tmp_path)
    assert restored.injected == state.injected
    assert restored.offsets == state.offsets


def test_save_state_when_dir_missing(tmp_path):
    """ディレクトリの自動作成（正常系）。"""
    # 準備
    target = tmp_path / "未作成" / "配下"
    # 実行
    save_state(SESSION, SessionState(), base_dir=target)
    # 検証
    assert (target / f"{SESSION}.json").exists()


# =========================
# clear_state
# =========================


def test_clear_state(tmp_path):
    """ファイルの削除（正常系）。"""
    # 準備
    state = SessionState()
    state.mark_injected(A)
    save_state(SESSION, state, base_dir=tmp_path)
    # 実行
    clear_state(SESSION, base_dir=tmp_path)
    # 検証
    assert load_state(SESSION, base_dir=tmp_path).injected == set()


def test_clear_state_when_file_missing(tmp_path):
    """未作成の無視（正常系）。"""
    # 実行・検証: 冪等操作なので例外を投げない
    clear_state("未保存のセッション", base_dir=tmp_path)
