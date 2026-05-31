# vscode-workspace-syncスキル — VS Code ワークスペースと worktree の同期

## 概要

`git worktree add` / `git worktree remove` 実行時に VS Code の `.code-workspace` を自動更新する PostToolUse フックを、プロジェクトの `.claude/settings.json` に登録するスキル。スキル実行は初回セットアップ時の一度だけで、以降は Claude Code がフックを自動実行する。

## セットアップ（スキル実行時）

1. カレントディレクトリおよび 1 階層上で `*.code-workspace` を検索
2. 候補をユーザーに提示し、使用するファイルを確認
3. `.claude/settings.json` に 2 つのフックを追加

- ワークスペースが見つからない場合はエラー表示し、ユーザーにパス入力を求める。

## フック

| フック | トリガー | 処理 |
|---|---|---|
| フック1 | PostToolUse (Bash) でコマンドに `git worktree add` を含む | 新 worktree パスを抽出し `.code-workspace` の `folders` 配列に追加 |
| フック2 | PostToolUse (Bash) でコマンドに `git worktree remove` を含む | 削除対象パスを抽出し `folders` 配列から削除 |

- マッチングは `tool_input.command` の文字列チェック。

## スクリプト設計

- 実装言語: Python（`json` モジュール）
- `.code-workspace` のパスはフック内にハードコード（スキル実行時に確定）
- `folders` 配列の各要素は `{"path": "..."}` 形式

## トリガー文言

- `ワークスペース同期を設定して`
- `VS Codeのワークツリーを自動追加したい`
- `worktreeをワークスペースに自動登録したい`
- `/work:vscode-workspace-sync`

## 参考ドキュメント

- `plugins/work/skills/vscode-workspace-sync/SKILL.md`: スキル本体

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成（specsから統合） | 260531_notes-spec-and-ref-inject |
