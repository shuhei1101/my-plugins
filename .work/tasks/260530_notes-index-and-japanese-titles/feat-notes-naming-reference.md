# feat/notes-naming-reference

> 内部 ID: 225（index.yaml 採番用 — クロスリファレンス目的）

## 概要

前ブランチ `feat/notes-sync-rule`（#218）で `.work/notes/` 編集時の `_index.md` 同期ルールを
`work-dot-work-dir.md` に追記した（短期 B 案）。

このブランチでは長期 A 案として、専用のリファレンスファイルを `plugins/work/references/` に追加し、
`.work/notes/` 配下のファイルを編集した際に **ref-inject フック** で自動注入する仕組みを実装する。

注入するリファレンスの内容:
- ファイル名・H1 タイトルは日本語（技術識別子はそのまま）
- `_index.md` を常に更新する（新規作成・リネーム時は同じコミットで追加、削除時は同じコミットで削除）

### 実施条件

即時実施可（PR206 `feat/ref-inject-references-edit-guard` マージ済みで実施条件が満たされた）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を `## QA` に記録する | - |
| - | ノートドキュメントを更新する | `.work/notes/` |
| - | ノート命名規則リファレンスを新規作成する | `plugins/work/references/notes-naming-rules.md` |
| - | JP ミラーを作成する | `plugins/work/references/notes-naming-rules.jp.md` |
| - | `_injection_rules.yaml` に `.work/notes/` パターンを追加する | `plugins/work/references/_injection_rules.yaml` |
| - | `_index.yaml` / `_index.jp.yaml` にリファレンスエントリを追加する | `plugins/work/references/` |
| - | `work-dot-work-dir.md` の既存ルールとの重複を確認・整理する | `plugins/work/references/work-dot-work-dir.md` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `{file/path}` | 新規 | {このファイルで何を実装したか} | {補足あれば} |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (なし) | - | - | - |

## QA

QA なし

## 参考ドキュメント

- `.work/notes/ノートインデックス同期ルール.md`: 前ブランチの設計メモ（A 案の背景が記載）
- `.work/notes/_index.md`: 同期対象のインデックスファイル
- `plugins/work/references/work-dot-work-dir.md`: 既存の `.work/` ディレクトリガイド（B 案の短期ルールを含む）
- `plugins/work/references/_injection_rules.yaml`: 注入パターン定義ファイル

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| `feat/notes-sync-rule` (#218) | 短期 B 案として `work-dot-work-dir.md` に `_index.md` 同期ルールを追記（前ブランチ） |
| `feat/ref-inject-references-edit-guard` (#206) | ref-inject フックの実装（このブランチの実施条件） |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
