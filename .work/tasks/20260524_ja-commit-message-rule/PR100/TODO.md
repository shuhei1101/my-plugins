# PR100 — ja-commit-message-rule

## 概要

work-kit:work-start スキルの Step 10（コミット実行）に「コミットメッセージは日本語で記述する」ルールを追記する。
ユーザーは音声入力で日本語ベースで作業しており、コミット履歴の可読性のためにも日本語コミットメッセージで統一したい。
適用範囲は work-start のみで、既存コミット履歴の修正は不要（今後生成するコミットだけ日本語化）。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| ✅ | `/claude-kit:skill-creator` 経由で SKILL.md の Step 10 に日本語化ルールを追記 | - `plugins/work-kit/skills/work-start/SKILL.md` |
| ✅ | SKILL.jp.md にも同じ追記を反映 | - `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| ✅ | `plugin.json` と `marketplace.json` のバージョン bump（PATCH 2.27.0 → 2.27.1） | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| ✅ | `changelogs/` にエントリ追加 | - `plugins/work-kit/changelogs/v2.27.1.md` |
| ✅ | ルール・CLAUDE.md の更新は不要と確認（既存ルールに該当なし） | - `.claude/rules/**` |

## 参考ドキュメント

- なし（小規模なルール追加）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
