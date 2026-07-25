"""`shared/logger.py` の単体テスト。"""
from __future__ import annotations

import sys

from inject_rules.shared.logger import emit_log

ENDPOINT = "http://localhost:4317"
EXPORTER_PATH = "opentelemetry.exporter.otlp.proto.grpc._log_exporter.OTLPLogExporter"
INDEX_URL = "https://example.com/rules.yaml"


def _make_exporter(exported: list, *, error: Exception | None = None):
    """送出内容を記録する Exporter スタブのクラスを作る。"""

    class _StubExporter:
        def __init__(self, *args, **kwargs):
            pass

        def export(self, batch):
            if error is not None:
                raise error
            exported.extend(batch)

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis: int = 30000) -> bool:
            return True

    return _StubExporter


def test_emit_log(monkeypatch):
    """1 件の送出（正常系）。"""
    # 準備: Exporter をスタブに差し替える
    exported: list = []
    monkeypatch.setattr(EXPORTER_PATH, _make_exporter(exported))
    # 実行
    emit_log("WARNING", "索引を取得できませんでした", {"index_url": INDEX_URL}, endpoint=ENDPOINT)
    # 検証
    record = exported[0].log_record
    assert record.body == "索引を取得できませんでした"
    assert record.severity_text == "WARNING"
    assert record.attributes["index_url"] == INDEX_URL


def test_emit_log_when_sdk_missing(monkeypatch, capsys):
    """SDK 未導入時の無処理（正常系）。"""
    # 準備: SDK の読み込みを失敗させる
    monkeypatch.setitem(sys.modules, "opentelemetry.sdk._logs", None)
    # 実行
    emit_log("WARNING", "索引を取得できませんでした", endpoint=ENDPOINT)
    # 検証: 例外を投げず、何も出力しない
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_emit_log_when_send_failed(monkeypatch, capsys):
    """送信失敗の握りつぶし（正常系）。"""
    # 準備: Exporter が例外を投げる
    monkeypatch.setattr(EXPORTER_PATH, _make_exporter([], error=RuntimeError("送信に失敗")))
    # 実行: 例外が呼び出し元へ伝播しない
    emit_log("WARNING", "索引を取得できませんでした", endpoint=ENDPOINT)
    # 検証: 標準エラーにも出ない
    assert capsys.readouterr().err == ""
