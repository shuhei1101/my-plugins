# claude-kit 成果物同期 — plugin-update スキルによるリポジトリ規約同期

## 概要

`claude-kit:plugin-update` スキルを使ってリポジトリ内の claude-kit 管轄成果物を最新の規約に同期する作業のメモ。

このスキルは静的テンプレートのコピーではなく、各ファイルを対応する reference（`references/*.md`）と照合し、差分だけを適用する「セマンティックマイグレーション」を行う。

## 同期対象

| # | 対象パターン | 参照 reference |
|---|---|---|
| 1 | `**/skills/*/SKILL.md` | `skills.md` + `common.md` |
| 2 | `.claude/rules/**/*.md` | `rules.md` + `common.md` |
| 3 | `**/CLAUDE{.local,.jp,}.md` | `claude-md.md` + `common.md` |
| 4 | `**/hooks/hooks.json`, `.claude/settings*.json` | `hooks.md` + `common.md` + `environment.md` |
| 5 | `**/hooks/prompts/*.md` | `hooks.md` |
| 6 | `**/.claude-plugin/{plugin,marketplace}.json` | `plugin-structure.md` + `common.md` |

## 実行手順

1. `master` / `main` 以外の作業ブランチで実行する
2. `/claude-kit:plugin-update` を実行
3. 各カテゴリのファイルを Read → injection hook が reference を注入 → 差分を Edit で適用
4. ステータスライン再適用（claude-kit 署名があれば）
5. 変更差分を確認してコミット
