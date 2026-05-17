---
created_at: 2026-05-16
updates:
  - 2026-05-16 — 初版作成（PR13）
  - 2026-05-18 — フックのインライン Python を `hooks/scripts/git-guard.py` に分離（PR52）
related_specs: []
related_prs:
  - PR13
  - PR52
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
- **実装**: `hooks/scripts/git-guard.py`
- **プロンプト**: `hooks/prompts/git-guard.md`

## ディレクトリ構成

```
plugins/guard-kit/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    ├── scripts/
    │   └── git-guard.py
    └── prompts/
        ├── git-guard.md
        └── git-guard.jp.md
```

## フック実装の方針

`hooks.json` には Python のワンライナーを埋め込まず、`hooks/scripts/*.py` に切り出す。
理由:

- JSON にはコメントが書けない一方、Python ファイルなら docstring とコメントで「何のフックか」を残せる
- ワンライナーは複数行に展開できないため可読性・テスト容易性が下がる
- `hooks.json` 側は `args` 配列で `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/<name>.py` を指すだけにする
