"""観測基盤へのログ送出。"""
from __future__ import annotations

import logging
from typing import Literal

SERVICE_NAME = "inject-rules"
SDK_LOGGER_NAME = "opentelemetry"
EXPORT_TIMEOUT_SEC = 2


def emit_log(
    level: Literal["WARNING", "ERROR"],
    message: str,
    attributes: dict[str, str] | None = None,
    *,
    endpoint: str,
) -> None:
    """観測基盤へログを 1 件送る。"""
    try:
        from opentelemetry._logs import SeverityNumber
        from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
        from opentelemetry.sdk._logs import LoggerProvider
        from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        # SDK を入れていない環境は観測基盤を使わない構成とみなす
        return

    # 送信先が落ちているときの SDK 自身のエラー出力をフックの標準エラーに混ぜない
    sdk_logger = logging.getLogger(SDK_LOGGER_NAME)
    sdk_logger.addHandler(logging.NullHandler())
    sdk_logger.propagate = False

    provider = LoggerProvider(
        resource=Resource.create({"service.name": SERVICE_NAME}), shutdown_on_exit=False
    )
    try:
        # 短命プロセスなのでバッチ送信を挟まずその場で送り切る
        # 送信先が落ちていても編集を待たせないよう待ち時間を短く抑える
        provider.add_log_record_processor(
            SimpleLogRecordProcessor(
                OTLPLogExporter(endpoint=endpoint, timeout=EXPORT_TIMEOUT_SEC)
            )
        )
        provider.get_logger(SERVICE_NAME).emit(
            severity_text=level,
            severity_number=SeverityNumber.ERROR if level == "ERROR" else SeverityNumber.WARN,
            body=message,
            attributes=attributes or {},
        )
        provider.shutdown()
    except Exception:
        # 送信できなくてもフックの処理は続ける
        return
