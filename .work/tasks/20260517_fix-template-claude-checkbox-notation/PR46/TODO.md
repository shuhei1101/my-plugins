# PR46 — fix-template-claude-checkbox-notation

## 概要

work-kit テンプレート（`plugins/work-kit/templates/.work/CLAUDE.md` および `CLAUDE.jp.md`）に、
古いチェックボックス表記（`- [x]`）と新しいテーブル表記（`完了` 列の `済`）が混在している。
TODO.md のフォーマットがテーブル形式に変わって以降、`[x]` の記述は不整合となっているため、
すべて `済` ベースの説明に統一する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する（本 PR では未決定事項なし） | - `.work/tasks/20260517_fix-template-claude-checkbox-notation/PR46/QA.md` |
| - | `.work/specs/` の関連仕様書を更新する（該当 spec なし — スキップ） | - なし |
| - | `templates/.work/CLAUDE.jp.md` L31 / L47 の `[x]` 表記を `済` 基準の文言に修正 | - `plugins/work-kit/templates/.work/CLAUDE.jp.md` |
| - | `templates/.work/CLAUDE.md` L27 / L43 の `[x]` 表記を `済` 基準の文言に修正（JP ミラーと同期） | - `plugins/work-kit/templates/.work/CLAUDE.md` |
| - | plugin.json / marketplace.json の version を PATCH 上げ | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する（該当変更なし） | - なし |

## 参考ドキュメント

- なし（仕様書を伴わないドキュメント整合性修正）
