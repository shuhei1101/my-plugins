# PR64 — add-glossary-to-conversation-skill

## 概要

conversation-to-claude スキルに用語集（glossary）の自動検出・追記機能を追加する。
提案はせず、Claude が会話を分析して自動判断で `.claude/rules/glossary.md` に追記する。
用語集はカテゴリ（H2）ごとに用語テーブルで管理する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.jp.md にステップ 1 の抽出カテゴリ F（用語）と自動追記ステップを追加 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | SKILL.md に同上（英語版） | `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | glossary リファレンスファイル（en/jp）を新規作成 | `plugins/claude-kit/references/glossary.md`, `glossary.jp.md` |
| 済 | plugin.json / marketplace.json バージョン bump | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

| 済 | glossary をサイレントではなく提案フェーズに統合（用語一覧を提示して確認）に変更 | `SKILL.jp.md`, `SKILL.md` |

## 参考ドキュメント

- なし

## QA

なし
