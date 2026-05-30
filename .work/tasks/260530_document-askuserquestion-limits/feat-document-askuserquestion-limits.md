# feat/document-askuserquestion-limits

> 内部 ID: 211（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`AskUserQuestion` の制約と正しい使い方を claude-kit リファレンスに汎用ドキュメントとして追加する。

具体的には以下の制約を文書化する：
- options は 2〜4 個（min 2 / max 4）
- "Other" オプションは UI が自動付与するため手動追加禁止
- `multiSelect: true` で複数選択可（排他でない選択肢に使用）
- `preview` フィールドは視覚的比較用（single-select のみ対応）
- スキル外での使用制限（Stop フックが発火しないため）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録 | - |
| 済 | ノートドキュメントを更新 | `.work/notes/AskUserQuestion制約リファレンス.md` |
| 済 | `askuserquestion.jp.md` を新規作成（JP ミラー先行） | `plugins/claude-kit/references/askuserquestion.jp.md` |
| 済 | `askuserquestion.md` を新規作成（英語版） | `plugins/claude-kit/references/askuserquestion.md` |
| 済 | `_index.yaml` にエントリを追加 | `plugins/claude-kit/references/_index.yaml` |
| 済 | `_index.jp.yaml` にエントリを追加 | `plugins/claude-kit/references/_index.jp.yaml` |
| 済 | `_injection_rules.yaml` を更新（skills パターンに optional 追加） | `plugins/claude-kit/references/_injection_rules.yaml` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/askuserquestion.md` | 新規 | AskUserQuestion の制約・使用ガイド（英語） | - |
| `plugins/claude-kit/references/askuserquestion.jp.md` | 新規 | 同上の JP ミラー | - |
| `plugins/claude-kit/references/_index.yaml` | 編集 | askuserquestion.md のエントリを追加 | - |
| `plugins/claude-kit/references/_index.jp.yaml` | 編集 | 〃 | - |
| `plugins/claude-kit/references/_injection_rules.yaml` | 編集 | skills パターンに optional: askuserquestion.md を追加 | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| テスト変更なし | - | - | - |

## QA

QA なし（制約はツールスキーマと CLAUDE.md から明確に取得可能）

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-config.md`: AskUserQuestion の使用例（config スキルパターン）
- `plugins/claude-kit/references/_injection_rules.yaml`: 注入ルール構造
- `.work/notes/AskUserQuestion制約リファレンス.md`: 本ブランチのノート

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| - | - |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
