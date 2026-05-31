# chore/remove-plugin-update-step1

> 内部 ID: 242（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`dev-kit` / `claude-kit` の `plugin-migrate` スキル（旧称 `plugin-update`、インストール済みキャッシュでは `plugin-update` 名）の Step 1 に「カレントブランチが master/main でないかチェックする」処理が含まれている。

work プラグインの UserPromptSubmit フック（work:start チェック）が、すべてのプロンプトで「セッション内にブランチがなければ work:start を実行せよ」と注入する。そのため plugin-migrate スキル側の Step 1（ブランチチェック）は責務の重複であり、かつ「master でないなら続行」と判定してフックの work:start 強制より先に通ってしまう競合を起こす（実際に aituber 側で、ブランチ未作成のまま静的テンプレが更新される事故が発生した）。

ブランチ管理はフック側の責務なので、`dev-kit` / `claude-kit` の `plugin-migrate` スキルから Step 1 を削除してステップを再番号付けする。

> 補足: aituber プロジェクトのプラグインキャッシュ
> (`~/.claude/plugins/cache/mentaiko-claude-plugins/{dev-kit,claude-kit}/.../skills/plugin-update/SKILL{,.jp}.md`)
> には暫定で同じ修正を適用済み。本ブランチでソース（my-plugins）を直し、プラグインを再配布すれば恒久化される。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA に未決定事項を記録する（現状なし） |
| 2 | 済 | `.work/notes/` のノートを更新する（必要なら新規作成） |
| 3 | 済 | `plugins/dev-kit/skills/plugin-migrate/SKILL.md` の Step 1（ブランチチェック）を削除し Step を再番号付け |
| 4 | 済 | `plugins/dev-kit/skills/plugin-migrate/SKILL.jp.md` を同期 |
| 5 | 済 | `plugins/claude-kit/skills/plugin-migrate/SKILL.md` の Step 1 を削除し Step を再番号付け |
| 6 | 済 | `plugins/claude-kit/skills/plugin-migrate/SKILL.jp.md` を同期 |
| 7 | 済 | `work` / `ref-inject` の plugin-migrate Step 1 は機能の一部なので **触らない** ことを確認 |
| 8 | 済 | 各 plugin.json の version を bump（プラグイン配布規約に従う） |
| 9 | 済 | ルール / CLAUDE.md の更新（必要があれば） |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/dev-kit/skills/plugin-migrate/SKILL.md` | 編集 | Step 1「ブランチチェック」削除・再番号付け | 旧 Step 2-6 → 1-5 |
| 2 | 〃 `SKILL.jp.md` | 〃 | JP ミラー同期 | - |
| 3 | `plugins/claude-kit/skills/plugin-migrate/SKILL.md` | 編集 | Step 1「ブランチチェック」削除・再番号付け | 旧 Step 2-4 → 1-3 |
| 4 | 〃 `SKILL.jp.md` | 〃 | JP ミラー同期 | - |
| 5 | `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | v4.11.0 → v4.11.1 | - |
| 6 | `plugins/dev-kit/CLAUDE.md` | 〃 | Changelog に 4.11.1 追加 | - |
| 7 | 〃 `CLAUDE.jp.md` | 〃 | 〃 | - |
| 8 | `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | v3.49.0 → v3.49.1 | - |
| 9 | `plugins/claude-kit/CLAUDE.md` | 〃 | Changelog に 3.49.1 追加 | - |
| 10 | 〃 `CLAUDE.jp.md` | 〃 | 〃 | - |
| 11 | `.claude-plugin/marketplace.json` | 編集 | dev-kit / claude-kit バージョン更新 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

未決定事項なし。

## 参考ドキュメント

- なし

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
