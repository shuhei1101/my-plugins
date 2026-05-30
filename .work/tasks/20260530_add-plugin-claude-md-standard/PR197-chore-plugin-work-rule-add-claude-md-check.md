# PR197 — plugin-work-rule-add-claude-md-check

## 概要

`plugin-work.md` の "When Editing" チェックリストに、プラグイン配下の `CLAUDE.md` 更新チェックを追加する。
各プラグインディレクトリには `CLAUDE.md` が存在し、プラグインのスキル・フック・環境変数などが記載されている。
プラグインを編集した際にこのファイルも更新するよう、整合性ルールとして明文化する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `## QA` に未決定事項を記録する | - |
| 済 | `.work/notes/` のノートを更新 | - |
| 済 | `plugin-work.md` の When Editing チェックリストに `plugins/{name}/CLAUDE.md` 更新チェックを追加 | - `.claude/rules/core/plugin-work.md` |
| 済 | JP ミラーを更新 | - `.claude/rules-jp/core/plugin-work.md` |
| 済 | ルールを更新 | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `.claude/rules/core/plugin-work.md` | 編集 | When Editing に CLAUDE.md チェックを追加 | - |
| `.claude/rules-jp/core/plugin-work.md` | 編集 | 同上の日本語ミラー | - |

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
| - | - | - |
