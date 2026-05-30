---
name: rule-creator
description: |
  Create a new path-scoped rule under .claude/rules/ using the step-based structure.
  Trigger when the user says "新しいルール作って", "ルールを新規作成", "make a rule for X", or "create a rule for".
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# rule-creator — パススコープルール作成（薄ラッパー）

ルールのオーサリング手順は本プラグインの references に移り、`.claude/rules/` 配下のファイルを
編集すると `claude-kit-references-injection` フックが**自動注入**する。このスキルは明示起動と
呼び出し元（`conversation-to-claude`, `notes-to-claude`）のために残している薄いラッパー。

## やること

1. `references/rules.md` + `references/common.md`（本プラグイン内）に従う。ルールファイルを書く際に
   自動注入される。注入されない場合は直接読む。両者は「ルールの読み込み条件」「2 種類（リンク型 /
   コンテキスト型）」「ユースケース指向の `paths:` 設計」「統合 / 分離基準」「フォルダ構成」「必須
   セクション」「構造例」をカバーする。
2. `.claude/rules-jp/<name>.md` を先に作り、それから英語の `.claude/rules/<name>.md` を生成する。
   JP ミラーを `.claude/rules/` 配下に置かないこと（自動ロードされてしまう）。
3. 各ファイルを `references/provenance.md` に従ってスタンプする — ファイルを書く際に自動注入される
   ので、直接スタンプを書く（スキル呼び出し不要）。
