---
paths:
  - "plugins/claude-kit/skills/conversation-to-claude/**"
  - "plugins/claude-kit/skills/skill-creator/**"
  - "plugins/claude-kit/skills/rule-creator/**"
  - "plugins/claude-kit/skills/hook-creator/**"
  - "plugins/claude-kit/skills/claude-creator/**"
  - "plugins/claude-kit/skills/claude-refactor/**"
  - "plugins/claude-kit/references/**"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/feature/claude-kit-skill-dependencies.md` も同時に更新してください。

# claude-kit スキル依存関係

## 概要

`conversation-to-claude` は Step 3 で4つの creator スキルに委譲する。
すべての creator スキルと `claude-refactor` は `plugins/claude-kit/references/` の共有参照ファイルを利用する。
これらのファイルを編集する際は、委譲インターフェースと参照ファイルのリンクが一貫していることを確認すること。

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` | オーケストレーター — Step 3 で creator スキルを呼び出す |
| `plugins/claude-kit/skills/skill-creator/SKILL.md` | スキル作成の委譲先 |
| `plugins/claude-kit/skills/rule-creator/SKILL.md` | ルール作成の委譲先 |
| `plugins/claude-kit/skills/hook-creator/SKILL.md` | フック作成の委譲先 |
| `plugins/claude-kit/skills/claude-creator/SKILL.md` | CLAUDE.md 作成の委譲先 |
| `plugins/claude-kit/skills/claude-refactor/SKILL.md` | すべての Claude 設定タイプを監査・整理する |
| `plugins/claude-kit/references/common.md` | 共有: ファイルタイプ判定基準と JP/EN ミラールール |
| `plugins/claude-kit/references/rules.md` | ルール設計ガイド（2種類・ユースケース指向・フォルダ構成） |
| `plugins/claude-kit/references/skills.md` | スキル設計ガイド |
| `plugins/claude-kit/references/hooks.md` | フック設計ガイド |
| `plugins/claude-kit/references/claude-md.md` | CLAUDE.md 設計ガイド |

## 編集時の確認事項

- `conversation-to-claude` の Step 3 委譲テーブルを変更した場合 → 委譲先 creator スキルが同じコンテキストを受け入れるか確認
- creator スキルの入力仕様を変更した場合 → `conversation-to-claude` の「渡すコンテキスト」列を更新
- `conversation-to-claude` に新しい成果物タイプを追加した場合 → 対応する creator スキルの行を追加
- `references/*.md` の内容を変更した場合 → そのファイルを参照しているすべてのスキルが正しく動作するか確認
- 新しい creator スキルを追加した場合 → `paths:`・関連ファイル表・スキルの Step 0 参照リストに追加

## ルールのメンテナンス

- 新しい creator スキルを追加した場合 → `paths:` と関連ファイル表に追加
- creator スキルを削除・リネームした場合 → `paths:` と関連ファイル表を更新
- `references/` ファイルを追加・リネームした場合 → `paths:` と関連ファイル表を更新し、参照しているすべてのスキルも更新
