---
paths:
  - ".claude/rules/**/*.md"
---

# ルールマーケット管理ルール（Rule Market Managed）

> このファイルは人間向けの日本語ミラーです。Claude には読み込まれません。本体は `rules/rule-market-managed.md`。

## 概要

このプロジェクトの一部のルールは `claude-rule` プラグインのルールマーケットライブラリからインストールされています。マーケット経由でインストールしたルールを編集した場合、改善をライブラリに同期できます。

## 同期方法

```
/claude-rule:rule-market sync <rule-name>
```

または同期スクリプトを直接実行する。**キャッシュではなくプラグインのソースリポジトリに書き込む**こと。

1. マーケットプレイスのソースリポジトリを探す（よくある場所で `marketplace.json` を検索）。
2. キャッシュ内のスクリプトを探す:
   ```bash
   # Bash
   find ~/.claude -name "sync_rules.py" -path "*claude-rule*" 2>/dev/null | head -1
   ```
   ```powershell
   # PowerShell
   Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" | Where-Object { $_.FullName -like "*claude-rule*" } | Select-Object -First 1 -ExpandProperty FullName
   ```
3. 実行する:
   ```bash
   python <script-path> sync <project-root> <rule-name> --plugin-repo <marketplace-repo-root>
   ```
4. ソースリポジトリで JP ミラー更新・バージョンバンプ・コミット。

## このプロジェクトにインストールされたマーケットルール

<!-- インストール時に追記してください: -->
<!-- - cascade-sync -->
<!-- - auto-register -->
