---
name: plugin-creator
description: |
  Create or update a Claude Code plugin with versioning (changelogs/ folder).
  Trigger when the user says "新しいプラグインを作りたい", "プラグインを作って", "プラグインを更新したい", "create a plugin", "update a plugin", "make a new plugin", or "plugin-creator して".
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# plugin-creator — プラグイン雛形・更新（薄ラッパー）

プラグインのオーサリング手順は本プラグインの references に移り、`plugin.json` / `marketplace.json`
を編集すると `claude-kit-references-injection` フックが**自動注入**する。このスキルは明示起動の
ために残している薄いラッパー。

## やること

1. `references/plugin-structure.md` + `references/common.md`（本プラグイン内）に従う。`plugin.json` /
   `marketplace.json` を書く際に自動注入される。注入されない場合は直接読む。両者は「標準ディレクトリ
   構成」「新規 / 更新モード」「plugin.json フィールド」「marketplace.json エントリ」「バージョンバンプ
   規則」「plugin.json / marketplace.json / changelog のバージョン一致不変条件」「changelog フォーマット」
   をカバーする。
2. `plugin.json`・`marketplace.json` エントリ・`changelogs/v{X.Y.Z}.md` のバージョンを一致させ、
   changelog の「構造の変更」セクションを書く。
3. プラグインへのリファレンス自動注入機構の付与は `/ref-inject:apply <plugin>` を使う（注入ファイルは
   ref-inject の領分。plugin-creator は `plugin.json` / ルート `CLAUDE.md` / `marketplace.json` の領分）。
4. 各生成ファイルを `references/provenance.md` に従ってスタンプする — ファイルを書く際に自動注入される
   ので、直接スタンプを書く（スキル呼び出し不要）。
