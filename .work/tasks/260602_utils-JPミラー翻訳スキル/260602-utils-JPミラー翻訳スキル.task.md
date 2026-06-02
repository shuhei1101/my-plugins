# utils JP ミラー翻訳スキル

> ブランチ: feat/utils-jp-mirror-translator

## 概要

utils プラグインを新規作成し、JP ミラー（`.jp.md`）ファイルを英語版に翻訳・同期するスキルとサブエージェントを追加する。

### 実施条件

即時実施可

## 作業内容

| No | 状態 | タスク |
|----|------|--------|
| 1 | 済 | `plugins/utils/` プラグインを新規作成（`plugin.json` 含む） |
| 2 | 済 | `jp-mirror-translator` サブエージェントを作成（`SKILL.md` + `SKILL.jp.md`） |
| 3 | 済 | `jp-mirror-sync` スキルを作成（`SKILL.md` + `SKILL.jp.md`） |
| 4 | 済 | `marketplace.json` にエントリを追加 |
| 5 | 済 | QA の記録 |
| 6 | 済 | ノートを更新 |

## 変更内容

| No | ファイル | 変更内容 |
|----|----------|----------|
| 1 | `plugins/utils/.claude-plugin/plugin.json` | プラグインマニフェストを新規作成 |
| 2 | `plugins/utils/CLAUDE.md` / `CLAUDE.jp.md` | プラグイン開発ガイドを新規作成 |
| 3 | `plugins/utils/agents/jp-mirror-translator.md` / `.jp.md` | JP→EN 翻訳サブエージェントを新規作成（Sonnet）|
| 4 | `plugins/utils/skills/jp-mirror-sync/SKILL.md` / `.jp.md` | ユーザー向けスキルを新規作成（並列サブエージェント）|
| 5 | `plugins/utils/skills/plugin-migrate/SKILL.md` / `.jp.md` | plugin-migrate スキルを新規作成 |
| 6 | `.claude-plugin/marketplace.json` | utils プラグインのエントリを追加 |

## テスト

| No | 項目 | 結果 |
|----|------|------|
| 1 | - | - |

## QA

| No | ID | 質問 | 回答 |
|----|----|------|------|
| 1 | QA-001 | サブエージェントのモデルは Haiku と Sonnet どちらにするか？技術的な開発者向けドキュメントの翻訳なので Sonnet を推奨するが確認したい | **Sonnet** で確定 |

## 参考ドキュメント

- `.work/notes/utils/utils-JP-ミラー翻訳スキル.md`

## 関連ブランチ

| No | ブランチ | 関係 |
|----|----------|------|
| 1 | - | - |

## 次ブランチ候補

| No | ブランチ名 | 概要 | 優先度 |
|----|------------|------|--------|
| 1 | - | - | - |
