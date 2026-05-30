# chore/sync-work-plugin-templates

> 内部 ID: 232（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`/work:plugin-update` スキルを実行し、work プラグインの `.work/` 内テンプレートファイル（CLAUDE.md、CLAUDE.jp.md、.gitignore）を最新版に上書き同期する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録する |
| 2 | 済 | ノートを `.work/notes/` に更新する |
| 3 | 済 | `.work/CLAUDE.md` を最新テンプレートで上書き（テンプレートに CLAUDE.md 未存在のためスキップ） |
| 4 | 済 | `.work/CLAUDE.jp.md` を最新テンプレートで上書き（テンプレートに CLAUDE.jp.md 未存在のためスキップ） |
| 5 | 済 | `.work/tasks/.gitignore` を最新テンプレートで上書き（既に同一内容） |
| 6 | 済 | `.work/issues/.gitignore` を最新テンプレートで追加 |
| 7 | 済 | `index.yaml` に `last_id` がなければ追加（last_id: 232 で既存） |
| 8 | 済 | 変更をコミット |
| 9 | 済 | `.work/CLAUDE.md` と `.work/CLAUDE.jp.md` を削除（テンプレートから削除済み＝ref-inject に移行済み） |
| 10 | 済 | `work:plugin-update` スキルに削除ステップを追加 |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `.work/issues/.gitignore` | 新規 | テンプレートより追加（`_index.yaml` を gitignore） | - |
| 2 | `.work/CLAUDE.md` | 削除 | ref-inject 移行済みのため削除 | - |
| 3 | `.work/CLAUDE.jp.md` | 削除 | 〃 | - |
| 4 | `plugins/work/skills/plugin-update/SKILL.md` | 編集 | Step 2 を CLAUDE.md 削除 + .gitignore 同期に改訂 | - |
| 5 | `plugins/work/skills/plugin-update/SKILL.jp.md` | 編集 | 〃 日本語版 | - |

## テスト

上記実装に伴って追加・変更したテストファイル。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

オープンな未決定事項なし。

## 参考ドキュメント

- `.work/notes/work-kitスキル群.md`: work プラグイン全般のノート

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | chore/work-template-update | 先行：テンプレートファイル構造の整備 |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
