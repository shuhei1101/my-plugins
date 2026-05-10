# PR4 — スキルへの rules/ テンプレート追加（wt / wiki / py）

## Overview

`wt` / `wiki` / `py` の各スキルに `rules/` サブフォルダを追加し、プロジェクト初期化時に `.claude/rules/` へデプロイするルールファイルテンプレートを同梱する。
各 SKILL.md にはテンプレート内容をインラインで埋め込んだ「Project Rule Deployment」セクションを追加。

## Scope

### Includes

- `plugins/wt/skills/wt/rules/pr-docs.md` — PR ドキュメント + index.yaml ルールテンプレート
- `plugins/wiki/skills/wiki/rules/wiki-work.md` — wiki 管理ルールテンプレート
- `plugins/py/skills/py/rules/implementation.md` — Python 実装前チェックルールテンプレート
- 各 SKILL.md に「Project Rule Deployment」セクション追加（テンプレート内容インライン埋め込み）
- CLAUDE.md / CLAUDE.jp.md に `rules/` サブフォルダ例外を追記
- wt / wiki / py バージョン 1.0.x → 1.1.0

### Excludes

- `claude-rule` / `yaml-rule` スキル（対応するプロジェクト汎用ルールなし）
- SKILL.jp.md の対訳更新（別途対応）

## Changed Files

- `plugins/wt/skills/wt/rules/pr-docs.md` — 新規作成
- `plugins/wiki/skills/wiki/rules/wiki-work.md` — 新規作成
- `plugins/py/skills/py/rules/implementation.md` — 新規作成
- `plugins/wt/skills/wt/SKILL.md` — Project Rule Deployment セクション追加
- `plugins/wiki/skills/wiki/SKILL.md` — Project Rule Deployment セクション追加
- `plugins/py/skills/py/SKILL.md` — Project Rule Deployment セクション追加
- `plugins/wt/.claude-plugin/plugin.json` — 1.0.3 → 1.1.0
- `plugins/wiki/.claude-plugin/plugin.json` — 1.0.0 → 1.1.0
- `plugins/py/.claude-plugin/plugin.json` — 1.0.0 → 1.1.0
- `.claude-plugin/marketplace.json` — 各バージョン更新
- `CLAUDE.md` / `CLAUDE.jp.md` — `rules/` 例外ルール追記
