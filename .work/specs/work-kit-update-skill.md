---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成（PR45）
related_specs:
  - work-kit-stop-hook.md
related_prs:
  - PR45
---

# work-kit:update スキル — .work/ テンプレート同期

## 概要

`/work-kit:update` は、カレントプロジェクトの `.work/` ディレクトリを最新の work-kit テンプレートに同期するスキル。
**ファイル変更・コミットを伴うため、必ず PR ブランチ上で実行する必要がある。**

## ワークフロー（8ステップ）

| ステップ | 内容 |
|---|---|
| 1 | テンプレートと `.work/` の存在を確認 |
| **2** | **`/work-kit:work-start` を実行して PR ブランチを準備** |
| 3 | `CLAUDE.md` / `CLAUDE.jp.md` を上書きコピー |
| 4 | `.gitignore` を同期 |
| 5 | `index.yaml` マイグレーション（`last_id` がなければ追加） |
| 6 | `QA.md` テンプレートの差分を適用 |
| 7 | `TODO.md` テンプレートの差分を適用 |
| 8 | 完了報告 |

## 重要な設計上の決定

### work-start を先に実行する（PR45 修正）

ステップ2で `/work-kit:work-start` を呼び出し、PRブランチとワークツリーを先に作成する。
これにより、以降のファイル変更・コミットがすべてPRブランチ内に収まることが保証される。

**修正前の問題**: ステップ1完了後に直接ファイルを変更し、master へコミットしようとしていた。

### ファイル更新戦略

- `CLAUDE.md` / `CLAUDE.jp.md` / `.gitignore` → テンプレートを直接上書き
- `QA.md` / `TODO.md` → 既存エントリを保護し、構造・フォーマット変更のみ適用

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `plugins/work-kit/skills/update/SKILL.md` | スキル定義（英語、Claude Code に読み込まれる） |
| `plugins/work-kit/skills/update/SKILL.jp.md` | 日本語ミラー（人間参照用） |
