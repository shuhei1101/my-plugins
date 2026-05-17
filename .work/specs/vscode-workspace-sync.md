---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成 (PR31)
related_specs: []
related_prs:
  - PR31
---

# vscode-workspace-sync — VS Codeワークスペースとworktreeを同期するスキル

## 概要

`git worktree add` / `git worktree remove` 実行時に VS Code の `.code-workspace` ファイルを自動更新する PostToolUse フックを、プロジェクトの `.claude/settings.json` に登録するスキル。

スキル実行は初回セットアップ時の一度だけ行い、以降は Claude Code がフックを自動実行する。

## 動作フロー

### スキル実行時（初期セットアップ）

1. カレントディレクトリおよび1階層上のフォルダで `*.code-workspace` を検索
2. 候補をユーザーに提示し、使用するファイルを確認
3. `.claude/settings.json` に以下の2つのフックを追加

### フック1: worktree 作成時

- **トリガー**: PostToolUse (Bash) — コマンドに `git worktree add` が含まれる
- **処理**: コマンドから新しいworktreeパスを抽出し、`.code-workspace` の `folders` 配列に追加

### フック2: worktree 削除時

- **トリガー**: PostToolUse (Bash) — コマンドに `git worktree remove` が含まれる
- **処理**: コマンドから削除対象のworktreeパスを抽出し、`.code-workspace` の `folders` 配列から削除

## スクリプト設計

- 実装言語: Python（`json` モジュール使用）
- `.code-workspace` のパスはフック内にハードコード（スキル実行時に確定）
- `folders` 配列の各要素は `{"path": "..."}` 形式

## 確定事項

- スキル名: `vscode-workspace-sync`
- フックの種別: PostToolUse (Bash)
- マッチング: `tool_input.command` に `git worktree add` / `git worktree remove` が含まれるか文字列チェック
- スクリプト言語: Python (`json` モジュール)
- ワークスペースが見つからない場合: エラー表示 + ユーザーにパス入力を求める
