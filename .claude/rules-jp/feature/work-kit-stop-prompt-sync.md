---
paths:
  - "plugins/work-kit/hooks/prompts/stop.md"
  - "plugins/work-kit/hooks/prompts/stop-no-merge.md"
---

<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# work-kit Stop プロンプトペア同期

`stop.md`（ステップ1-4）と `stop-no-merge.md`（ステップ1-3）はペアのStopフックプロンプトです。
`stop-no-merge.md` は `stop.md` からステップ4（マージ提案）を除いたものです。
どちらかを編集する際は、ステップ1-3の内容を両ファイルで同期させてください。

## ファイルの関係

| ファイル | 内容 |
|---|---|
| `stop.md` | ステップ1-4: TODO/QA/ノートリマインダー + `/work-kit:merge` 提案 |
| `stop-no-merge.md` | ステップ1-3のみ: TODO/QA/ノートリマインダー（マージ提案なし） |

## 編集時の対応

- **`stop.md` のステップ1-3を編集** → 同じ変更を `stop-no-merge.md` にも適用する
- **`stop.md` のステップ4を編集** → `stop-no-merge.md` への変更は不要
- **`stop-no-merge.md` にステップ4を追加しない** — このファイルの目的はマージ提案を省略することのため

## 背景

`hooks.json` の Stopフックインライン Python が `WORK_KIT_MERGE_PROPOSAL` に基づいてファイルを選択します:
- truthy（デフォルト） → `stop.md` を読み込む
- falsy → `stop-no-merge.md` を読み込む

PR173 で追加。
