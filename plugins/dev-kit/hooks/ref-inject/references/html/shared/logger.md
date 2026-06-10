---
paths:
  - "**/frontend/shared/lib/logger.{ts,js}"
---

# logger.ts

ログ出力を集約する。画面・共通層は `console.*` を直書きせず logger 経由で出す。

- レベル（error / warn / info / debug）で出し分ける。
- エラーは握りつぶさず `logger.error` で残す（`core/エラーは握りつぶさない.md`）。デバッグ FAB のログバッファ連携もここに置く。
