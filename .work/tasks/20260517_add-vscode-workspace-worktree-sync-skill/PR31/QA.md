# QA — PR31 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: スキル名

**背景**: work-kit に追加するスキルの名前が未決定。

| 案 | 内容 |
|---|---|
| A | `vscode-workspace-sync` — 機能を直接表す名前 |
| B | `workspace-setup` — セットアップ操作であることを強調 |
| C | `add-worktree-hook` — フック追加であることを強調 |

**推奨方式**: A (`vscode-workspace-sync`) — 何をするスキルかが最も明確

**決定したら反映先**: TODO.md のファイルパス・plugin.json のスキル一覧

---

## QA-002: フックのイベントとマッチングパターン

**背景**: worktree 作成・削除を検知するフックの種別とマッチング方法が未確定。

| 案 | 内容 |
|---|---|
| A | PostToolUse (Bash) + `tool_input.command` に `git worktree add` / `git worktree remove` が含まれるかチェック |
| B | PostToolUse (Bash) + 正規表現で `git\s+worktree\s+(add\|remove)` にマッチ |

**推奨方式**: A — シンプルで読みやすい。マッチング失誤のリスクは低い

**決定したら反映先**: SKILL.md のフック定義ステップ

---

## QA-003: フックスクリプトの言語

**背景**: `.code-workspace`（JSON）を読み書きするスクリプトの実装言語。

| 案 | 内容 |
|---|---|
| A | Python (`json` モジュール) — 既存の work-kit スクリプトと統一 |
| B | PowerShell (`ConvertFrom-Json` / `ConvertTo-Json`) — Windows 環境に最適 |
| C | Node.js (`fs` + `JSON.parse`) — VS Code 環境なら確実に使える |

**推奨方式**: A (Python) — 既存 work-kit スクリプトと言語統一でき保守しやすい

**決定したら反映先**: SKILL.md のフックスクリプト定義

---

## QA-004: ワークスペースファイルが見つからない場合の挙動

**背景**: `.code-workspace` が見つからなかったときスキルをどう終了させるか。

| 案 | 内容 |
|---|---|
| A | エラーを表示してスキル終了（ユーザーに手動で指定してもらう） |
| B | ファイルパスをユーザーに入力してもらう |

**推奨方式**: A — シンプル。ファイルが存在しない環境では機能しないことを明示

**決定したら反映先**: SKILL.md の Step 1

---
