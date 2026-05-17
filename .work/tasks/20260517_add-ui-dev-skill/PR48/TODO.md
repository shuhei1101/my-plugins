# PR48 — add-ui-dev-skill

## 概要

`dev-kit` プラグインに新スキル `ui-dev` を追加する。
開発系の画面(開発用 UI)を作成・編集する際に必ず適用する規約で、
中心機能は「フロートデバッグボタンを画面に置き、押すと関連ファイル情報と直近 JS ログを
JSON でクリップボードにコピーできるデバッグモーダルを開く」というデバッグ動線を提供すること。

リファレンスは今回作らずスキル単体で完結させる(規約量が増えたら将来切り出す)。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/20260517_add-ui-dev-skill/PR48/QA.md` |
| - | 仕様書 `ui-dev-design.md` を新規作成する | - `.work/specs/ui-dev-design.md` |
| - | `skills/ui-dev/SKILL.md` を新規作成(フロートデバッグボタン規約・実装手順) | - `plugins/dev-kit/skills/ui-dev/SKILL.md` |
| - | `skills/ui-dev/SKILL.jp.md` を新規作成(日本語ミラー) | - `plugins/dev-kit/skills/ui-dev/SKILL.jp.md` |
| - | dev-kit のバージョン更新(1.0.0 → 1.1.0) | - `plugins/dev-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する(必要があれば) | - `CLAUDE.md`, `CLAUDE.jp.md` |

## 参考ドキュメント

- `.work/specs/ui-dev-design.md`: ui-dev スキル設計仕様(本 PR で作成)
