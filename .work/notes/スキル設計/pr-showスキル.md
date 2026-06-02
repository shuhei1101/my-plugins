# work:branch-show スキル — 次ブランチ候補一覧の状況表示

## 概要

`/work:branch-show` は `work:merge` の Step 12 から切り出された独立スキル。
ブランチドキュメントの `## 次ブランチ候補` テーブルを読んで候補を 3 カテゴリに分類して表示する。

旧名: `work:pr-show`（`work:pr-show` → `work:branch-show` にリネーム済み）

## disable-model-invocation の経緯

- **追加時**: `merge` Step 12 切り出し時に、他の creator 系スキルと同様に `disable-model-invocation: true` を付与した
- **削除**: branch-show はユーザーが直接呼ぶだけでなく、モデルが自律的に呼び出す場面（作業完了時の次ブランチ確認など）があると判断して削除

## 設計メモ

- データソースはブランチドキュメントの `## 次ブランチ候補` テーブルのみ
- カテゴリ判定: コミット数 ≤1 → 着手可能、≥2 → 他セッション進行中、実施条件あり → 条件あり

## 変更履歴

| # | 日付 | 内容 |
|---|---|---|
| 1 | 2026-06-02 | `work:pr-show` → `work:branch-show` にリネーム反映、古い PR 番号参照を削除 |
