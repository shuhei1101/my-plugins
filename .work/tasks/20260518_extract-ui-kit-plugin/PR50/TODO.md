# PR50 — extract-ui-kit-plugin

## 概要

`dev-kit` から UI 関連を分離し、新プラグイン **`ui-kit`** を新設する。
さらに新スキル `logging`(ログ整備)と `flocss-apply`(FLOCSS 適用)を追加する。

役割分担:
- **dev-kit**: 開発規約全般(Python・YAML・将来の他言語規約)
- **ui-kit**: 開発用 UI コンポーネント提供 + UI 規約

合わせて dev-kit の空 references は削除し、現状有効な内容のみ残す。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/20260518_extract-ui-kit-plugin/PR50/QA.md` |
| - | 仕様書 `ui-kit-design.md` を新規作成 | - `.work/specs/ui-kit-design.md` |
| - | 仕様書 `dev-kit-design.md` を更新(UI 関連を削除) | - `.work/specs/dev-kit-design.md` |
| - | `ui-kit` プラグインスケルトン作成 | - `plugins/ui-kit/.claude-plugin/plugin.json` |
| - | `ui-kit/references/principles.md` 作成(DRY/FLOCSS/JS 規約/frontend-design 必須) | - `plugins/ui-kit/references/principles.md`, `principles.jp.md` |
| - | dev-kit `skills/ui-dev/` を ui-kit に移動・改名 `debug-fab/` | - `plugins/ui-kit/skills/debug-fab/` |
| - | `ui-kit/skills/logging/` 新規作成(ログ規約・出力レベル別ガイド) | - `plugins/ui-kit/skills/logging/SKILL.md`, `SKILL.jp.md` |
| - | `ui-kit/skills/flocss-apply/` 新規作成(新規/既存両対応) | - `plugins/ui-kit/skills/flocss-apply/SKILL.md`, `SKILL.jp.md` |
| - | dev-kit から空 references を削除 | - `plugins/dev-kit/references/{backend,vscode-extension,html,css,js,frontend,common}.{md,jp.md}` |
| - | dev-kit `skills/ui-dev/` を削除(ui-kit 側に移動済) | - `plugins/dev-kit/skills/ui-dev/` |
| - | dev-kit バージョン更新(1.1.0 → 2.0.0、破壊的変更) | - `plugins/dev-kit/.claude-plugin/plugin.json` |
| - | marketplace.json に ui-kit 追加、dev-kit バージョン更新 | - `.claude-plugin/marketplace.json` |
| - | CSS-JS 紐付けルールを `/rule-creator` で作成 | - `.claude/rules/{name}.md`(rule-creator が決定) |
| - | ルール・CLAUDE.md を整備する | - `CLAUDE.md`, `CLAUDE.jp.md`(必要に応じて) |

## 参考ドキュメント

- `.work/specs/ui-kit-design.md`: ui-kit 設計仕様(本 PR で作成)
- `.work/specs/dev-kit-design.md`: dev-kit 設計仕様(本 PR で更新)
