---
description: >
  Auto-loaded when editing plugin component files — enforces invoking the matching
  creator skill before making any changes.
globs:
  - "plugins/**/skills/**/SKILL.md"
  - "plugins/**/skills/**/SKILL.jp.md"
  - "plugins/**/hooks/**"
  - "plugins/**/CLAUDE.md"
  - "plugins/**/templates/CLAUDE.md"
  - ".claude/rules/**/*.md"
  - "plugins/**/.claude-plugin/plugin.json"
  - ".claude-plugin/marketplace.json"
---

# Creator Skill Dispatch Rules

プラグインのコンポーネントファイルを新規作成・編集する前に、**必ず対応するクリエイタースキルを先に呼び出すこと**。
スキルを経由せずに直接ファイルを編集することを禁止する。

## 編集対象 → 使用するスキル

| 編集・作成するファイル | 先に呼び出すスキル |
|---|---|
| `plugins/**/skills/**/SKILL.md` | `/claude-kit:skill-creator` |
| `plugins/**/skills/**/SKILL.jp.md` | `/claude-kit:skill-creator` |
| `plugins/**/hooks/**` | `/claude-kit:hook-creator` |
| `plugins/**/CLAUDE.md`、`templates/CLAUDE.md` | `/claude-kit:claude-creator` |
| `.claude/rules/**/*.md` | `/claude-kit:rule-creator` |
| `plugins/**/.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json` | `/claude-kit:plugin-creator` |

## 禁止事項

- クリエイタースキルを呼び出さずに上記ファイルを直接作成・編集しない
- 「小さな修正だから」「テキスト変更だけだから」という理由でスキルをスキップしない
- スキルが提示するフローを途中で打ち切らない

## 例外

以下は直接編集してよい:

- `SKILL.jp.md` を英語版 `SKILL.md` の変更に追従させる場合（翻訳更新のみ）
- `changelogs/` ファイル（plugin-creator が自動生成するため）
- バグ修正として既存スキルの文言を修正する場合（ただしバージョン bump は必要）

## なぜこのルールが必要か

クリエイタースキルはファイル生成だけでなく、以下を強制するガイドを提供する:
- 正しいディレクトリ構造
- `plugin.json` / `marketplace.json` のバージョン同期
- `changelogs/` への記録
- JP ミラーの同時更新

スキルを経由しないと、これらの整合性チェックが抜け落ちる。
