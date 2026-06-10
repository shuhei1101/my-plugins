---
paths:
  - "**/frontend/shared/lib/fmt.{ts,js}"
---

# fmt.ts

日付・数値・通貨などの整形関数を集約する。画面ごとに整形関数を再定義しない。

- 日時表示は JST に変換して出す（`Intl.DateTimeFormat("ja-JP", { timeZone: "Asia/Tokyo" })`）。引数なしの `toLocaleString()` は環境依存なので使わない（`dev/タイムスタンプ規約`）。
- 純関数。DOM を触らない。
