# PR63 — fix-rule-proposal-path

## 概要

ルール提案時に適用パス（どのファイル/ディレクトリにルールを適用するか）を提案フォーマットに追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.jp.md のルール提案フォーマットに「適用パス」を追加 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | SKILL.md のルール提案フォーマットに「適用パス」を追加 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | plugin.json / marketplace.json のバージョンを bump する | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

| 済 | SKILL に「再発防止」抽出カテゴリ (E) を追加し固定ルール名提案を実装 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md`, `SKILL.md` |
| 済 | incidents リファレンスファイル（en/jp）を新規作成 | `plugins/claude-kit/references/incidents.md`, `incidents.jp.md` |
| 済 | incidents フォルダ構造（rules/インデックス＋references/詳細）をドキュメントに明記 | 上記ファイル内 |
| 済 | plugin.json / marketplace.json バージョン bump (3.10.0) | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## QA

なし
