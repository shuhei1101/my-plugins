# PR169 — integrate-guard-kit-into-workspace

## 概要

`guard-kit` プラグイン（`git push` / `git merge` 検出 PreToolUse(Bash) フック）を `workspace`（旧 work-kit、PR172 でリネーム）に統合する。env 変数 `WORKSPACE_GUARD`（デフォルト有効、falsy で無効）で起動可否を切り替えられるようにし、`guard-kit` プラグイン本体は削除する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR172 | work-kit → workspace リネーム（本 PR で master 適合済み） |
| #PR167 | config スキル追加・workspace 2.39.0 bump（本 PR でバージョン衝突解決のため 2.40.0 に再 bump） |
| #PR165 | provenance スタンプ全廃（本 PR の追加ファイルにスタンプを付けない） |
| #PR164 | 常時発火フック/ステップに env トグルを追加（同パターンの先行事例） |
| #PR163 | worktree-kit を workspace に統合（プラグイン統合の先行事例） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（QA なし） | - `.work/tasks/.../PR169/QA.md` |
| 済 | `.work/notes/integrate-guard-kit-into-workspace.md` を作成 | - `.work/notes/integrate-guard-kit-into-workspace.md` |
| 済 | `git-guard.py` を workspace にコピーし `WORKSPACE_GUARD` env チェックを追加 | - `plugins/workspace/hooks/scripts/git-guard.py` |
| 済 | `git-guard.md` / `git-guard.jp.md` を workspace にコピー | - `plugins/workspace/hooks/prompts/git-guard.md` / `git-guard.jp.md` |
| 済 | `workspace/hooks/hooks.json` の PreToolUse(Bash) 配列に git-guard エントリを追加 | - `plugins/workspace/hooks/hooks.json` |
| 済 | `plugins/guard-kit/` フォルダを削除 | - `plugins/guard-kit/` |
| 済 | `marketplace.json` から guard-kit エントリを除外 | - `.claude-plugin/marketplace.json` |
| 済 | workspace のバージョンを 2.39.0 → 2.40.0 に bump（plugin.json と marketplace.json 両方） | - `plugins/workspace/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |
| 済 | changelog 追加（v2.40.0.md） | - `plugins/workspace/changelogs/v2.40.0.md` |
| 済 | `glossary.md` に「guard-kit 統合 (PR169)」「WORKSPACE_GUARD」エントリ追加、`env トグル一覧 (PR164)` に WORKSPACE_GUARD を追記 | - `.claude/rules/core/glossary.md` |
| 済 | JP ミラー同期（rules-jp/core/glossary.md） | - `.claude/rules-jp/core/glossary.md` |
| 済 | master 適合（PR172 リネーム / PR167 バージョン衝突 / PR165 provenance 廃止 等への対応） | - 各種 |
| 済 | 動作確認（push/merge 時にプロンプト挟まる、`WORKSPACE_GUARD=false` で挟まらない） | - 手動確認 |

## 参考ドキュメント

- `.work/notes/integrate-guard-kit-into-workspace.md`: 統合方針・env スコープ優先順位・master 適合作業の整理
- `.work/notes/env-toggles-for-hooks-and-steps.md`: PR164 で確立した env トグル設計パターン

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| add-protected-branches-env | ガード対象ブランチ名を env var（カンマ区切り）で指定可能にする。現状 `master-commit-guard.py` の `PROTECTED_BRANCHES = ("master", "main", "develop")` ハードコードを `WORKSPACE_PROTECTED_BRANCHES=master,main,develop` 等で上書き可能にする | 即時実施可 |
