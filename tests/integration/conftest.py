"""結合テスト共通の fixture。"""
from __future__ import annotations

import io
import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from inject_rules.main import inject_conventions, main


@dataclass(frozen=True, slots=True, kw_only=True)
class HookDirs:
    """フック実行時のキャッシュとセッション状態の置き場所。"""

    cache: Path
    session: Path


@pytest.fixture
def hook_dirs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> HookDirs:
    """キャッシュとセッション状態を一時ディレクトリへ差し替える。"""
    cache = tmp_path / "cache"
    session = tmp_path / "session"
    monkeypatch.setenv("INJECT_RULES_CACHE_DIR", str(cache))
    monkeypatch.setenv("INJECT_RULES_SESSION_DIR", str(session))
    return HookDirs(cache=cache, session=session)


@pytest.fixture
def run_hook(monkeypatch: pytest.MonkeyPatch):
    """フックのペイロードを標準入力へ流してエントリポイントを実行する。"""

    def _run(payload: dict) -> int:
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
        return main()

    return _run


@pytest.fixture
def run_session_start(monkeypatch: pytest.MonkeyPatch):
    """セッション開始フックのペイロードを標準入力へ流してエントリポイントを実行する。"""

    def _run(payload: dict) -> int:
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
        return inject_conventions()

    return _run
