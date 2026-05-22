# PR76 — rules-folder-restructure

## 概要

`my-plugins/.claude/rules/` 直下の7ファイルを `core/` と `feature/` サブフォルダに整理し、欠損している JP ミラー5本を `rules-jp/` に追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/20260523_rules-folder-restructure/PR76/QA.md` |
| - | `rules/core/` フォルダを作成し3ファイルを git mv で移動 | `glossary.md` `incidents.md` `plugin-work.md` |
| - | `rules/feature/` フォルダを作成し4ファイルを git mv で移動 | `claude-kit-skill-dependencies.md` `debug-fab-template-sync.md` `work-kit-todo-template-sync.md` `worktree-kit-dependency.md` |
| - | `rules/core/_overview.md` を生成 | `.claude/rules/core/_overview.md` |
| - | `rules/feature/_overview.md` を生成 | `.claude/rules/feature/_overview.md` |
| - | 欠損 JP ミラー5本を `rules-jp/` に作成 | `rules-jp/claude-kit-skill-dependencies.md` etc. |
| - | `incidents.md` 内の detail リンクパスを更新確認 | `.claude/rules/core/incidents.md` |
| - | rules を参照している他ファイルのパス更新確認 | CLAUDE.md, その他 rules |
| - | ルール・CLAUDE.md を整備する | 必要に応じて |

## 参考ドキュメント

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | - |
