---
created_at: 2026-05-24
updates:
  - 2026-05-24 — 初版作成
  - 2026-05-24 — 実装完了・未決事項を解決済みに更新
  - 2026-05-24 — PR110: 冗長ルール・CLAUDE.mdセクション削除
  - 2026-05-24 — PR121: UserPromptSubmit の限界を補う PreToolUse ブロック追加
  - 2026-05-25 — PR124: dev-kit/ui-kit/work-kit から skill-creator-dispatch 重複削除
related_specs: []
related_prs:
  - PR103
  - PR110
  - PR121
  - PR124
---

# claude-kit creator-skill-hook — UserPromptSubmit フック設計メモ

## 概要

CLAUDE.md / SKILL.md / ルール / フックを編集・作成しようとするプロンプトを検知し、
対応するクリエイタースキルを使うよう促すメッセージを UserPromptSubmit でインジェクションする。

## なぜルールではなくフックか

- `.claude/rules/feature/creator-skill-dispatch.md` に同内容のルールがあるが、
  ルールは「常時読み込みトークン消費」かつ「Claude が無視しても検知できない」という問題がある。
- UserPromptSubmit フックはプロンプト文字列を直接検査し、一致した場合だけ追加コンテキストを差し込める。
- フックが存在する場合はルール側のコンテンツを削除してトークン節約も検討できる。

## 検知パターン（想定）

以下のキーワードをプロンプトに含む場合にフックを発火させる:

- `SKILL.md` / `SKILL.jp.md`
- `CLAUDE.md`
- `.claude/rules/`
- `plugin.json` / `marketplace.json`
- `hooks/`（claude-kit スコープ内）

## インジェクションするメッセージ（骨子）

```
Before editing this file, invoke the matching creator skill:
- SKILL.md / SKILL.jp.md → /claude-kit:skill-creator
- CLAUDE.md              → /claude-kit:claude-creator
- .claude/rules/**       → /claude-kit:rule-creator
- hooks/                 → /claude-kit:hook-creator
- plugin.json / marketplace.json → /claude-kit:plugin-creator
```

## 実装結果

- **フック形式**: インライン `-c` 形式（Pythonスクリプトファイル不要）
- **トリガー精度**: ファイルパス・ファイル名キーワードマッチング
- **既存ルール**: `.claude/rules/feature/creator-skill-dispatch.md` を削除（フックで完全代替）
- **バージョン**: claude-kit 3.19.1 → 3.20.0（MINOR バンプ）

## キーワードマッチング仕様

| フック | 検知キーワード |
|---|---|
| skill-creator-dispatch | `skill.md`, `skill.jp.md`, `/skills/` |
| rule-creator-dispatch | `.claude/rules/`, `rules/` |
| hook-creator-dispatch | `/hooks/`, `hooks.json` |
| claude-creator-dispatch | `claude.md` |
| plugin-creator-dispatch | `plugin.json`, `marketplace.json` |

## 現行設計の限界と今後の改善計画

### UserPromptSubmit の限界（PR121 で判明）

- UserPromptSubmit はユーザーのプロンプト文字列のみを検査するため、Claude が内部的に
  ツールを呼び出してファイルを編集する場面（スキル実行中など）では発火しない。
- PreToolUse ブロック型（skill-creator-dispatch）は Claude のツール呼び出し前に発火するため、
  この問題を回避できる。

### PR121 の問題（PR124 で修正）

- skill-creator-dispatch の PreToolUse フックを claude-kit/dev-kit/ui-kit/work-kit の
  4プラグインに重複追加した。
- claude-kit がインストール済みなら他プラグインにフックを持つ必要はない。
- PR124 で dev-kit/ui-kit/work-kit から重複エントリ + prompts ファイルを削除し、claude-kit に集約。

### 残課題（後続PR）

- claude-kit の PreToolUse パターンが `/skills/[^/]+/SKILL\.md$` のみ → `SKILL.jp.md`、
  `.claude/rules/*.md`、`CLAUDE.md` をカバーしていない。
- PreToolUse でファイル編集を検知する仕組みの設計調査も必要。
