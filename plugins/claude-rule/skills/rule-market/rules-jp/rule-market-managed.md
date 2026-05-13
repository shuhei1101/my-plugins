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

または同期スクリプトを直接実行:
```powershell
Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" |
  Where-Object { $_.FullName -like "*claude-rule*" }
python <script-path> sync <project-root> <rule-name>
```

同期後は `rules-jp/` の JP ミラーも更新し、プラグインのバージョンをバンプしてください。

## このプロジェクトにインストールされたマーケットルール

<!-- インストール時に追記してください: -->
<!-- - cascade-sync -->
<!-- - auto-register -->
