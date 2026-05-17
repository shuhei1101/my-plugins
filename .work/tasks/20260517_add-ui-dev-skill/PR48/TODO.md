# PR48 — add-ui-dev-skill

## 概要

`dev-kit` プラグインに新スキル `ui-dev` を追加する。
開発系の画面(管理画面・内部ツール・デバッグ画面など)を作成・編集する際に必ず適用する規約で、
中心機能は「フロートデバッグボタンを画面に置き、押すと関連ファイル情報と直近 JS ログを
JSON でクリップボードにコピーできるデバッグモーダルを開く」というデバッグ動線を提供すること。

ボタン本体・ロガーフック・モーダルは**共通モジュール**として 1 回読み込めば動くようにし、
各画面は `data-debug-files` 属性で関連ファイルを宣言するだけにする(各画面に同じコードを書かない)。

合わせて `references/common.md` にログ規約(JSON Lines・ロガー必須・操作ログ重視・1 行ログ短く)を追加し、
`references/{html,css,js}.md` の雛形も作成する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する(QA-001〜010) | - `.work/tasks/20260517_add-ui-dev-skill/PR48/QA.md` |
| 済 | 仕様書 `ui-dev-design.md` を最終仕様に合わせて更新 | - `.work/specs/ui-dev-design.md` |
| 済 | `templates/uidev.css` を新規作成(モックから抽出) | - `plugins/dev-kit/skills/ui-dev/templates/uidev.css` |
| 済 | `templates/uidev.js` を新規作成(モックから抽出) | - `plugins/dev-kit/skills/ui-dev/templates/uidev.js` |
| 済 | `templates/CLAUDE.md` + `CLAUDE.jp.md` を作成(フォルダ用ガイド、Claude 自動読み込み) | - `plugins/dev-kit/skills/ui-dev/templates/CLAUDE.md`, `CLAUDE.jp.md` |
| 済 | `templates/example.html` を新規作成(参考実装例) | - `plugins/dev-kit/skills/ui-dev/templates/example.html` |
| 済 | `skills/ui-dev/SKILL.md` を新規作成 | - `plugins/dev-kit/skills/ui-dev/SKILL.md` |
| 済 | `skills/ui-dev/SKILL.jp.md` を新規作成(日本語ミラー) | - `plugins/dev-kit/skills/ui-dev/SKILL.jp.md` |
| 済 | `references/common.md` にログ規約セクションを追加 | - `plugins/dev-kit/references/common.md`, `common.jp.md` |
| 済 | `references/html.md` 雛形を新規作成 | - `plugins/dev-kit/references/html.md`, `html.jp.md` |
| 済 | `references/css.md` 雛形を新規作成 | - `plugins/dev-kit/references/css.md`, `css.jp.md` |
| 済 | `references/js.md` 雛形を新規作成 | - `plugins/dev-kit/references/js.md`, `js.jp.md` |
| 済 | dev-kit のバージョン更新(1.0.0 → 1.1.0) | - `plugins/dev-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | `references/frontend.md` に「frontend-design スキルを必ず使う」ルールを追加 | - `plugins/dev-kit/references/frontend.md`, `frontend.jp.md` |
| 済 | ルール・CLAUDE.md を整備する(必要があれば) | - `CLAUDE.md`, `CLAUDE.jp.md` |

## 参考ドキュメント

- `.work/specs/ui-dev-design.md`: ui-dev スキル設計仕様(本 PR で更新)
- `tmp/ui-dev-mock.html`(メインリポジトリ・gitignored): UI 確認用モック(完成版)
