# PR31 — add-vscode-workspace-worktree-sync-skill

## 概要

VS Codeワークスペースファイル（`.code-workspace`）と `git worktree` の作成・削除を同期するスキルを work-kit に追加する。

スキル実行時にプロジェクト内の `.code-workspace` ファイルを探し、ユーザーに確認後、以下のフックを `.claude/settings.json` に書き込む：
- worktree 作成時 → ワークスペースの `folders` にパスを追加
- worktree 削除時 → ワークスペースの `folders` からパスを削除

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | スキル定義 SKILL.md を作成 | - `plugins/work-kit/skills/vscode-workspace-sync/SKILL.md` |
| - | スキル定義 SKILL.jp.md を作成 | - `plugins/work-kit/skills/vscode-workspace-sync/SKILL.jp.md` |
| - | plugin.json のスキル一覧に追加 | - `plugins/work-kit/.claude-plugin/plugin.json` |
| - | marketplace.json のバージョンを更新 | - `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/specs/vscode-workspace-sync.md`: スキルの設計仕様
- QA.md: スキル名・フック設計など未決定事項

## スキル設計メモ

### Step 1: ワークスペースファイルを探す
- 検索対象: カレントディレクトリ・1階層上のフォルダ
- パターン: `*.code-workspace`
- ユーザーに候補を提示して確認

### Step 2: フックを作成
- フック種別: PostToolUse (Bash) — `git worktree add` にマッチ
  - スクリプト: `.code-workspace` の `folders` 配列にパスを追加
- フック種別: PostToolUse (Bash) — `git worktree remove` にマッチ
  - スクリプト: `.code-workspace` の `folders` 配列からパスを削除
- 保存先: プロジェクトの `.claude/settings.json`
