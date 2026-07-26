"""単体 / 結合テスト共通の fixture。"""
from __future__ import annotations

import sys
import urllib.error
from dataclasses import dataclass
from pathlib import Path

import pytest

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "plugins" / "inject-rules"
sys.path.insert(0, str(PLUGIN_DIR / "src"))

TEMPLATE_DIR = PLUGIN_DIR / "templates"


@dataclass(frozen=True, slots=True, kw_only=True)
class TmpDirs:
    """エントリポイントの実行に使う一時ディレクトリ一式。"""

    cache: Path
    session: Path
    templates: Path


class _NullExporter:
    """観測基盤へ送らない Exporter。"""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def export(self, batch: object) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


@pytest.fixture(autouse=True)
def no_otlp_export(monkeypatch: pytest.MonkeyPatch) -> None:
    """テスト中に観測基盤へ実接続しないよう Exporter を無効化する。"""
    try:
        from opentelemetry.exporter.otlp.proto.grpc import _log_exporter
    except ImportError:
        # SDK 未導入の環境ではログ送出そのものが行われない
        return
    monkeypatch.setattr(_log_exporter, "OTLPLogExporter", _NullExporter)


@pytest.fixture
def template_dir() -> Path:
    """配布物のテンプレートディレクトリを返す。"""
    return TEMPLATE_DIR


@pytest.fixture
def tmp_template_dir(tmp_path: Path) -> Path:
    """テンプレートファイルを配置した一時ディレクトリを返す。"""
    target = tmp_path / "templates"
    target.mkdir()
    (target / "ヘッダー.txt").write_text("[ヘッダー]\n", encoding="utf-8")
    (target / "ブロック.txt").write_text(
        "\n---\n\n> 適用ルール: $url\n> 適用パターン: $patterns\n\n$body\n", encoding="utf-8"
    )
    (target / "読み込み中.txt").write_text(
        "\n---\n\n読み込み中（$loaded/$total ファイル）。残り $remaining 件。\n", encoding="utf-8"
    )
    (target / "完了.txt").write_text(
        "\n---\n\n$loaded/$total ファイル読み込み完了\n", encoding="utf-8"
    )
    return target


@pytest.fixture
def tmp_dirs(tmp_path: Path, tmp_template_dir: Path, monkeypatch: pytest.MonkeyPatch) -> TmpDirs:
    """キャッシュ・セッション状態・テンプレートの置き場所を一時ディレクトリへ差し替える。"""
    cache = tmp_path / "cache"
    session = tmp_path / "session"
    monkeypatch.setenv("INJECT_RULES_CACHE_DIR", str(cache))
    monkeypatch.setenv("INJECT_RULES_SESSION_DIR", str(session))
    monkeypatch.setattr("inject_rules.main.TEMPLATE_DIR", tmp_template_dir)
    return TmpDirs(cache=cache, session=session, templates=tmp_template_dir)


@pytest.fixture
def fetch_stub():
    """URL → 本文の辞書から取得関数を作る factory（呼び出し URL を記録する）。"""

    def _make(pages: dict[str, str], *, errors: dict[str, Exception] | None = None):
        calls: list[str] = []

        def _fetch(url: str) -> str:
            calls.append(url)
            if errors and url in errors:
                raise errors[url]
            if url not in pages:
                raise urllib.error.URLError(f"not found: {url}")
            return pages[url]

        _fetch.calls = calls  # type: ignore[attr-defined]
        return _fetch

    return _make


@pytest.fixture
def rule_index():
    """ルール索引 YAML を組み立てる factory（ルールは索引からの相対パスで書く）。"""

    def _make(entries: list[tuple[str, list[str]]]) -> str:
        lines = ["rules:"]
        for rule, patterns in entries:
            lines.append(f"  - rule: {rule}")
            lines.append("    paths:")
            lines.extend(f'      - "{p}"' for p in patterns)
        return "\n".join(lines) + "\n"

    return _make
