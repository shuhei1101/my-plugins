# PR83 — add-plugin-creator-skill

## 概要

plugin-kit プラグインに `plugin-creator` スキルを新規追加する。
プラグイン作成・更新時にバージョン管理フォルダ（`changelogs/`）と変更履歴ファイルを必ず生成するスキル。
これにより、プラグイン構造が変わった際に「どのバージョンで何が変わったか」を追跡できるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/.../PR83/QA.md` |
| 済 | `.work/specs/` の仕様書を更新する | `.work/specs/plugin-kit.md` |
| 済 | plugin-kit プラグインディレクトリを作成する | `plugins/plugin-kit/` |
| 済 | plugin.json を作成する | `plugins/plugin-kit/.claude-plugin/plugin.json` |
| 済 | plugin-creator スキル（SKILL.md）を作成する | `plugins/plugin-kit/skills/plugin-creator/SKILL.md` |
| 済 | marketplace.json にエントリを追加する | `.claude-plugin/marketplace.json` |
| - | plugin-kit を削除し claude-kit に移動する | `plugins/plugin-kit/` → `plugins/claude-kit/skills/plugin-creator/` |
| - | marketplace.json から plugin-kit エントリを削除する | `.claude-plugin/marketplace.json` |
| - | claude-kit の plugin.json バージョンをバンプする | `plugins/claude-kit/.claude-plugin/plugin.json` |
| - | ルール・CLAUDE.md を整備する | 必要に応じて |

## 参考ドキュメント

- `README.md`: プラグイン作成方法の公式手順
- `.work/specs/plugin-kit.md`: plugin-kit スキル仕様書

## 次PR候補

| タイトル | 概要 |
|---|---|
| plugin-kit:plugin-updater | 既存プラグインの更新・バージョンバンプを支援するスキル |
