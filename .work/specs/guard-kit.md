---
created_at: 2026-05-16
updates:
  - 2026-05-16 — 初版作成（PR13）
related_specs: []
related_prs:
  - PR13
---

# guard-kit — セキュリティ・安全作業ガードプラグイン

## 概要

危険な操作（不可逆 git 操作、意図しない副作用を持つコマンド等）を実行前にインターセプトし、ユーザー確認を強制するフック・スキルをまとめるプラグイン。

## フック一覧

### git-guard（PreToolUse: Bash）

`git push` / `git merge` が含まれる Bash コマンドを検出し、実行前に毎回ユーザー確認を求める。

- **トリガー**: `Bash` ツールの `command` に `\bgit\s+(push|merge)\b` がマッチする場合
- **動作**: `decision: block` + プロンプト注入で確認を要求
- **ループ防止**: 一時トークンファイル（`/tmp/work-kit-git-guard-{session_id}`）で1回のブロック後は通過
- **プロンプト**: `hooks/prompts/git-guard.md`

## ディレクトリ構成

```
plugins/guard-kit/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── prompts/
        ├── git-guard.md
        └── git-guard.jp.md
```
