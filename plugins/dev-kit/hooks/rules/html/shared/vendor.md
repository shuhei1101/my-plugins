---
paths:
  - "**/shared/vendor/**"
---

# shared/vendor

- 外部依存は vendoring してここに固定する（mermaid 等）。
  - CDN ランタイム依存にしない。
  - バンドルの代わりに、固定済みファイルをそのまま配信する。
