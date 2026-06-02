# issue-resolve スキル — 設計メモ

## 概要

`work:issue-resolve` は `/loop` 駆動でレビュー済みイシューを消化するスキル。
1 起動 = 対応可能なイシュー 1 件を処理する。

## Step 1: 対応可能イシューの探索フロー

`_index.yaml` を先に読み、`status: not_started` のエントリだけに絞ってからイシューファイルを開く。

```
_index.yaml を読む
  → status: not_started のエントリをイシュー番号昇順で収集
    → 各イシューファイルを順に開く
      - ## 意思 = 否定 → REJECT (Step 2)
      - ## 意思 = 肯定 → ACCEPT (Step 3)
      - ## 意思 = 未記入 → スキップ
```

**以前の設計**（変更前）: 全 ISSUE-*.md を glob してから `_index.yaml` でステータス照合していた。
`_index.yaml` を先に読む方が自然で、`in_progress` イシューのファイルを無駄に開かなくて済む。

## status と decision の分担

| 情報 | 場所 | 概要 |
|---|---|---|
| `status` | `_index.yaml` | not_started / in_progress / closed（work 管理状態） |
| `decision` (意思) | イシューファイル `## 意思` | 対応する / 対応しない / 未記入（人間のレビュー結果） |

status が `not_started` のイシューのみが処理対象。`in_progress` はロック中なのでスキップ。

## 変更履歴

| # | バージョン | 日付 | 変更内容 |
|---|---|---|---|
| 1 | 2.63.0 | 2026-06-02 | イシューフォーマット刷新: フロントマター廃止・2 分割 Markdown・status を `_index.yaml` へ移動 |
| 2 | — | 2026-06-02 | Step 1 を `_index.yaml` 優先読み込みに変更（glob 先行 → index 先行） |
