# PR4 — update-todo-template

## 概要

TODO.md テンプレートを刷新する。チェックボックス1行形式から、概要・作業内容テーブル・参考ドキュメントの3セクション構成に変更。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| [x] | プラグイン内 TODO.md テンプレートを新構成に更新 | `plugins/work-kit/skills/setup/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` |
| [x] | `.work/` デプロイ済みテンプレートを同期 | `.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` |
| [x] | stop.jp.md — index.yaml 読み込みステップを削除、セッション内 PR の TODO 更新に変更 | `plugins/work-kit/hooks/prompts/stop.jp.md` |
| [x] | stop.md（英語本体）を同期 | `plugins/work-kit/hooks/prompts/stop.md` |
| [x] | user-prompt-submit.jp.md — ステップ1（index.yaml 読み込み）を削除 | `plugins/work-kit/hooks/prompts/user-prompt-submit.jp.md` |
| [x] | user-prompt-submit.md（英語本体）を同期 | `plugins/work-kit/hooks/prompts/user-prompt-submit.md` |
| [x] | テンプレート CLAUDE.jp.md の規約セクションを新 TODO 形式に合わせて更新 | `plugins/work-kit/skills/setup/templates/.work/CLAUDE.jp.md` |
| [x] | テンプレート CLAUDE.md（英語本体）を同期 | `plugins/work-kit/skills/setup/templates/.work/CLAUDE.md` |
| [x] | work-kit バージョンバンプ（plugin.json + marketplace.json） | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

<!-- 関連仕様書・参考リンクなし -->
