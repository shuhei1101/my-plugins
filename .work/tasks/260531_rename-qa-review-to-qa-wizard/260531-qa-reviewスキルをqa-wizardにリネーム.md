# qa-reviewスキルをqa-wizardにリネーム

> ブランチ: `refactor/rename-qa-review-to-qa-wizard`

## 概要

work プラグインの `qa-review` スキルは「QA をレビューする」ではなく「未決定の QA 項目をユーザーに提示して判断を収集する」動作であるため、実態に合わない。`qa-wizard` に改名して意図を明確にする。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `## QA` に未決定事項を記録する |
| 2 | 済 | スキルディレクトリを `qa-review` → `qa-wizard` にリネーム |
| 3 | 済 | `SKILL.md` / `SKILL.jp.md` の `name` フィールドと本文内参照を更新 |
| 4 | 済 | `plugins/work/CLAUDE.md` / `CLAUDE.jp.md` の `work:qa-review` 参照を更新 |
| 5 | 済 | `.work/notes/` のノートを更新 |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/qa-wizard/SKILL.md` | 新規 | qa-review → qa-wizard へリネーム後の SKILL.md | 旧 qa-review/SKILL.md を移動 |
| 2 | `plugins/work/skills/qa-wizard/SKILL.jp.md` | 新規 | 〃 JP ミラー | 〃 |
| 3 | `plugins/work/CLAUDE.md` | 編集 | `work:qa-review` → `work:qa-wizard` に更新 | - |
| 4 | `plugins/work/CLAUDE.jp.md` | 編集 | 〃 JP ミラー | - |

## テスト

手動テスト・動作確認の実施記録。

| # | シナリオ | 期待値 | 実値 | 判定 | 補足 |
|---|---|---|---|---|---|
| 1 | `/work:qa-wizard` を呼び出す | QA 項目が提示される | - | - | リネーム後に確認 |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

（なし）

## 参考ドキュメント

- `.work/notes/スキル設計/インタラクティブレビュースキル.md`: qa-wizard（旧 qa-review）と impl-review の設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
