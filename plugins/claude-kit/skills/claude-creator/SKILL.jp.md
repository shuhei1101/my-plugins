---
name: claude-creator
description: |
  Create or overhaul a CLAUDE.md (and its CLAUDE.jp.md mirror) for a project or subfolder.
  Trigger when the user says "CLAUDE.md を作って", "CLAUDE.md を書いて", "create a CLAUDE.md",
  "クロードのガイドを作りたい", "このフォルダの CLAUDE.md を作って", or asks to set up
  Claude Code instructions for a project or specific folder.
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# claude-creator — CLAUDE.md オーサリング（薄ラッパー）

CLAUDE.md のオーサリング手順は本プラグインの references に移り、`CLAUDE.md` を編集すると
`claude-kit-references-injection` フックが**自動注入**する。このスキルは明示起動のために残している薄いラッパー。

## やること

1. `references/claude-md.md` + `references/common.md`（本プラグイン内）に従う。`CLAUDE.md` を書く際に
   自動注入される。注入されない場合は直接読む。両者は「読み込みタイミング（ルート / サブフォルダ）」
   「薄肉原則と抽出先ガイド」「他ファイル種別との照合」「JP ミラー先行ワークフロー」「必須セクション」
   「構造例」「行数ガイドライン」をカバーする。
2. `CLAUDE.jp.md` を先に書き（日本語・約200行以内）、それから英語の `CLAUDE.md` を生成する。
3. 各ファイルを `references/provenance.md` に従ってスタンプする — ファイルを書く際に自動注入される
   ので、直接スタンプを書く（スキル呼び出し不要）。
