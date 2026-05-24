---
created_at: 2026-05-24
updates:
  - 2026-05-24 — 初版作成
related_specs: []
related_prs:
  - PR103
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

## 未決事項

- フックのトリガー精度: 誤検知を避けるにはどこまでパターンを絞るか
- 既存ルール `creator-skill-dispatch.md` の扱い: フック追加後に削除or残存させるか
