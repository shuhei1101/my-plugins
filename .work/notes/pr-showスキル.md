---
created_at: 2026-05-25
updates:
  - 2026-05-25 — PR120: disable-model-invocation を削除
related_specs:
related_prs:
  - PR109
  - PR120
---

# pr-show スキル — 次 PR 候補一覧の状況表示

## 概要

`/work-kit:pr-show` は merge の Step 12 から切り出された独立スキル。
TODO.md の `## 次PR候補` テーブルを読んで候補を3カテゴリに分類して表示する。

## disable-model-invocation の経緯

- **PR109 で追加**: merge Step 12 切り出し時に、他の creator 系スキルと同様に `disable-model-invocation: true` を付与した
- **PR120 で削除**: pr-show はユーザーが直接呼ぶだけでなく、モデルが自律的に呼び出す場面（作業完了時の次PR確認など）があると判断して削除

## 設計メモ

- データソースは TODO.md の `## 次PR候補` テーブルのみ（`git branch --list 'PR*'` は使わない）
- カテゴリ判定: コミット数 ≤1 → 着手可能、≥2 → 他セッション進行中、実施条件あり → 条件あり
