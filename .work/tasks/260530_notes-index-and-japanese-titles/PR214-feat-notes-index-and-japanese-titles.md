# PR214 — notes-index-and-japanese-titles

## 概要

`.work/notes/` 配下のノートの H1 タイトルを日本語に統一し、カテゴリ別にリンクを束ねた `_index.md` インデックスファイルを追加する。
あわせて work プラグインのノートテンプレートも日本語タイトル例示に更新し、work:start スキルに `_index.md` の自動生成・更新ステップを追加する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | ノートドキュメントを更新する | `.work/notes/` |
| 済 | 既存ノート 11 件の H1 タイトルを日本語に統一する | `.work/notes/*.md` (my-plugins-wt-PR214) |
| 済 | `_index.md` をカテゴリ別分類で作成する | `.work/notes/_index.md` |
| 済 | workプラグインのノートテンプレートを日本語タイトル例示に更新する | `plugins/work/templates/note.md` |
| 済 | work:start スキルに `_index.md` 自動生成・更新ステップを追加する | `plugins/work/skills/start/SKILL.md` |
| 済 | 既存ノート 25 件のファイル名を日本語化する | `.work/notes/*.md` |
| 済 | `_index.md` のリンクを新ファイル名に更新する | `.work/notes/_index.md` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `.work/notes/_index.md` | 新規 | カテゴリ別ノートインデックス | |
| `.work/notes/*.md` (25件) | 編集 | H1 タイトルを日本語に統一 | |
| `plugins/work/skills/start/SKILL.md` | 編集 | `_index.md` 生成ステップを追加 | my-plugins リポジトリ側 |
| `plugins/work/skills/start/SKILL.jp.md` | 編集 | JP ミラー更新 | |
| `plugins/work/templates/note.md` | 編集 | 日本語タイトル例示に更新 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (なし) | - | - | - |

## QA

QA なし

## 参考ドキュメント

- `.work/notes/_index.md`: 作成するインデックスファイル本体

## 関連PR

| PR番号 | 概要 |
|---|---|
| #187 | rename-specs-to-notes (notes ディレクトリの命名整備) |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| notes-sync-rule | ノートを新規作成・更新したとき `_index.md` の同期を促すルールを追加 | 即時実施可 |
| notes-naming-reference | `plugins/work/references/` にノート命名規則リファレンスを追加し `_injection_rules.yaml` で `.work/notes/` 編集時に注入する。内容: ファイル名・H1 タイトルは日本語、技術識別子はそのまま、`_index.md` を常に更新する | `PR206/feat/ref-inject-references-edit-guard` がマージされてから |
