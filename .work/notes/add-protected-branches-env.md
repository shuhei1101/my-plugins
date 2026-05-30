---
created_at: 2026-05-30
updates:
  - 2026-05-30 — 初版（PR177 pr-handoff から着手）
related_specs:
  - integrate-guard-kit-into-workspace.md
  - env-toggles-for-hooks-and-steps.md
related_prs:
  - PR177
  - PR169
  - PR164
  - PR163
---

# 保護ブランチ env 化 — PR177

## 概要

`master-commit-guard.py` の保護対象ブランチを env var `WORKSPACE_PROTECTED_BRANCHES`（カンマ区切り）で上書き可能にする。デフォルトは現状維持の `master,main,develop`。

## 動機

- ユーザー要望「ガード対象ブランチも env で指定可能に。カンマ区切りでいいかな」
- プロジェクトによっては保護したいブランチが違う:
  - `master` だけ → `WORKSPACE_PROTECTED_BRANCHES=master`
  - リリースブランチも守りたい → `WORKSPACE_PROTECTED_BRANCHES=master,main,release/prod`
  - 検証ブランチで guard を切りたい → `WORKSPACE_PROTECTED_BRANCHES=` （空文字 = 全パス）
- `WORKSPACE_GUARD` （PR169）は push/merge 全体の on/off だが、`master-commit-guard` は **どのブランチを守るか**の細かさが欲しい

## パース仕様

```python
raw = os.environ.get("WORKSPACE_PROTECTED_BRANCHES", "master,main,develop")
PROTECTED_BRANCHES = tuple(b.strip() for b in raw.split(",") if b.strip())
```

ポイント:
- 空文字 / 全要素空 → `PROTECTED_BRANCHES = ()` → 全ブランチ素通り（guard 全停止に近い、ただし `WORKSPACE_GUARD=false` の方が意図表明として明示的）
- 前後 strip で `master, main, develop` のようなスペース許容
- `release/prod` などスラッシュ含むブランチ名も OK（`,` をセパレータにしているだけ）

## デフォルト維持

env 未設定時は `master,main,develop` で**完全な後方互換**。

## env スコープ優先順位（再掲）

`settings.json` 優先順位（高→低）:

1. Enterprise managed policies
2. CLI 引数
3. `.claude/settings.local.json`（プロジェクト個人、git-ignore 対象）
4. `.claude/settings.json`（プロジェクト共有）
5. `~/.claude/settings.json`（ユーザーグローバル）

→ プロジェクト毎に `.claude/settings.json` で上書き可。

## バージョン bump

- workspace: 2.40.0 → 2.41.0（MINOR: 新機能・後方互換）

## glossary 更新

- 新エントリ: `WORKSPACE_PROTECTED_BRANCHES`
- `env トグル一覧 (PR164)` に追記
