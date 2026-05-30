# feat/notes-sync-rule

> 内部 ID: 218（index.yaml 採番用 — クロスリファレンス目的）

## 概要

PR214 (`feat/notes-index-and-japanese-titles`) で `.work/notes/` 配下のノートを以下のルールで整備した:
- ファイル名・H1 タイトルはすべて日本語（技術識別子はそのまま）
- `_index.md` にカテゴリ別インデックスを作成

しかし **新規ノート作成・既存ノート更新時に `_index.md` を更新し忘れる** という課題が残っている。
このブランチでは `.work/notes/` 配下のファイルを編集したときに `_index.md` の同期を促すルール
（または ref-inject リファレンス）を追加する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | ノートドキュメントを更新する | `.work/notes/` |
| 済 | `.work/notes/` 編集時に `_index.md` 同期を促すルールまたはリファレンスを追加する | `plugins/work/` |
| 済 | ルール / CLAUDE.md を更新する | - |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/references/work-dot-work-dir.md` | 編集 | `notes/` セクションに `_index.md` カタログの説明と同期規約を追加 | |
| 2 | `plugins/work/references/work-dot-work-dir.jp.md` | 編集 | 英語版の日本語ミラーを同期 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (なし) | - | - | - |

## QA

QA なし

## 参考ドキュメント

- `.work/notes/ノートインデックス同期ルール.md`: このブランチの設計メモ
- `.work/notes/_index.md`: 同期対象のインデックスファイル
- `.work/tasks/260530_notes-index-and-japanese-titles/PR214-feat-notes-index-and-japanese-titles.md`: 前ブランチのドキュメント

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| `feat/notes-index-and-japanese-titles` (#214) | ノートタイトル日本語化・`_index.md` 作成（前ブランチ） |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| notes-naming-reference | `plugins/work/references/` にノート命名規則リファレンスを追加し `_injection_rules.yaml` で `.work/notes/` 編集時に注入。内容: ファイル名・H1 タイトルは日本語、技術識別子はそのまま、`_index.md` を常に更新する | `PR206/feat/ref-inject-references-edit-guard` がマージされてから |
