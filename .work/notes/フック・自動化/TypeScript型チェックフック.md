# TypeScript 型チェックフック (PR143)

## 概要

next-kit に PostToolUse フック (`ts_check.py`) を追加し、`*.ts` / `*.tsx` 編集後に自動で型チェックを実行する。

## 背景

PR135 で next-kit の規約として `Awaited<ReturnType<typeof fetchResource>>` パターンを採用。
内部関数の signature を変えると `Awaited<ReturnType<...>>` 型が壊れる脆さがある。
ユーザーの「TS の lint みたいなやつを最後に絶対実行するようにしたい」という発言が本 PR の動機。

## 実装内容

### ファイル構成

| ファイル | 役割 |
|---|---|
| `plugins/next-kit/hooks/ts_check.py` | PostToolUse フック本体 |
| `plugins/next-kit/hooks/hooks.json` | PostToolUse(Edit/Write/MultiEdit) エントリ追加 |
| `plugins/next-kit/references/CLAUDE.md` | フック説明セクション追加 |
| `plugins/next-kit/references/CLAUDE.jp.md` | JP ミラー更新 |
| `plugins/next-kit/.claude-plugin/plugin.json` | v3.1.0 → v3.2.0 |
| `.claude-plugin/marketplace.json` | next-kit v3.1.0 → v3.2.0 |

### 設計決定

| 項目 | 決定 |
|---|---|
| フック種別 | PostToolUse(Edit/Write/MultiEdit) |
| 対象ファイル | `*.ts` / `*.tsx` のみ |
| tsconfig.json 検出 | 編集ファイルから上方向探索（モノレポ対応） |
| tsc コマンド | `tsc --noEmit --incremental` |
| エラー時の挙動 | stdout に出力（decision: block は使わない） |
| 配置 plugin | next-kit（TS 規約がまとまっている場所） |

## 動作フロー

1. Claude が `*.ts` / `*.tsx` を Edit/Write/MultiEdit
2. PostToolUse フックが発火 → `ts_check.py` が実行
3. 編集ファイルから `tsconfig.json` を上方向に探索（最大 20 階層）
4. `tsc --noEmit --incremental` を `tsconfig.json` のあるディレクトリで実行
5. エラーあり → stdout に出力（Claude がツール結果として受け取り修正に活用）
6. エラーなし → 何も出力せず終了
