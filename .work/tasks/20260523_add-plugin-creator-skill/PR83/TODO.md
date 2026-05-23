# PR83 — add-plugin-creator-skill

## 概要

plugin-kit プラグインに `plugin-creator` スキルを新規追加する。
プラグイン作成・更新時にバージョン管理フォルダ（`changelogs/`）と変更履歴ファイルを必ず生成するスキル。
これにより、プラグイン構造が変わった際に「どのバージョンで何が変わったか」を追跡できるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/.../PR83/QA.md` |
| - | `.work/specs/` の仕様書を更新する | `.work/specs/plugin-kit.md` |
| - | plugin-kit プラグインディレクトリを作成する | `plugins/plugin-kit/` |
| - | plugin.json を作成する | `plugins/plugin-kit/.claude-plugin/plugin.json` |
| - | plugin-creator スキル（SKILL.md）を作成する | `plugins/plugin-kit/skills/plugin-creator/SKILL.md` |
| - | marketplace.json にエントリを追加する | `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する | 必要に応じて |

## 参考ドキュメント

- `README.md`: プラグイン作成方法の公式手順
- `.work/specs/plugin-kit.md`: plugin-kit スキル仕様書

## 次PR候補

| タイトル | 概要 |
|---|---|
| plugin-kit:plugin-updater | 既存プラグインの更新・バージョンバンプを支援するスキル |
