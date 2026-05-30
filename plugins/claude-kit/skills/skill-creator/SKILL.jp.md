---
name: skill-creator
description: |
  Create a new Claude Code skill under .claude/skills/ using the step-based structure.
  Trigger when the user says "スキルを作りたい", "新しいスキル作って", "create a skill", "make a skill for X", or claude-kit dispatches here.
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# skill-creator — 新規スキル雛形（薄ラッパー）

スキルのオーサリング手順は本プラグインの references に移り、`SKILL.md` を編集すると
`claude-kit-references-injection` フックが**自動注入**する。このスキルは明示起動と呼び出し元
（例: `notes-to-claude`）のために残している薄いラッパー。

## やること

1. `references/skills.md` + `references/common.md`（本プラグイン内）に従う。`SKILL.md` を書く際に
   自動注入される。注入されない場合は直接読む。両者は「skill が適切な種別か」「既存類似スキルの
   確認」「JP ミラー先行ワークフロー」「ステップ構造テンプレ」「description フロントマター規約」を
   カバーする。
2. `.claude/skills/<name>/SKILL.jp.md` を先に作り、それから英語の `SKILL.md` を生成する。
3. 各ファイルを `references/provenance.md` に従ってスタンプする — ファイルを書く際に自動注入される
   ので、直接スタンプを書く（スキル呼び出し不要）。
