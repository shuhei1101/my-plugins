---
paths:
  - "**/frontend/pages/**/_shared/**"
---

# pages/{domain}/_shared

そのドメイン内（複数画面・複数タブ）でだけ使い回す部品を置く。`_` 接頭辞。

- 1 画面でしか使わないものは画面直下に書く。ドメインをまたいで使うものは `shared/` へ上げる（`共通化の判断.md`）。
- 作法は shared と同じ。UI 部品は Custom Element を .ts + .css セットで、純ロジックは関数で置く。
