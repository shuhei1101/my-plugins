# PR197 — plugin-work-rule-add-claude-md-check

## 概要

`plugins/claude-kit/references/plugin-structure.md` の Authoring workflow に、プラグイン配下の
`CLAUDE.md` 更新チェックを追加する。各プラグインディレクトリには `CLAUDE.md` が存在し、
スキル・フック・環境変数などが記載されている。プラグインを編集した際にこのファイルも更新するよう、
チェックリストとして明文化する。

なお `.claude/rules/` は将来的に全廃止しプラグインリファレンスへ移行する予定のため、
今回は既存のルールファイルは変更せず、リファレンス側にのみ追記する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `## QA` に未決定事項を記録する | - |
| 済 | `.work/notes/` のノートを更新 | - |
| 済 | `plugin-structure.md` の Step 3/4 に CLAUDE.md 更新チェックを追加 | - `plugins/claude-kit/references/plugin-structure.md` |
| 済 | JP ミラーを更新 | - `plugins/claude-kit/references/plugin-structure.jp.md` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/plugin-structure.md` | 編集 | Step 3/4 に CLAUDE.md 更新チェックリストを追加 | ルールファイルではなくリファレンス側に記載 |
| `plugins/claude-kit/references/plugin-structure.jp.md` | 編集 | 同上の日本語ミラー | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストなし | - |

## QA

なし

## 参考ドキュメント

- `.work/notes/plugin-claude-md-standard.md`: プラグイン CLAUDE.md 標準セクション構成

## 関連PR

| PR番号 | 概要 |
|---|---|
| #171 | プラグイン CLAUDE.md 標準セクション構成の定義 |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| deprecate-claude-rules-migrate-to-references | `.claude/rules/` 配下のルールファイルを全廃止し、内容を各プラグインの `references/` へ移行する | 即時実施可 |
