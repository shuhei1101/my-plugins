# feat/branch-author-env

> 内部 ID: 235（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`work:start` で作成するブランチ名に、任意の作者名を差し込む環境変数 `WORK_BRANCH_AUTHOR` を追加する。
設定されていれば `feat/nishikawa/test-update` 形式、空白・未設定なら従来の `feat/test-update` 形式になる。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA セクションに未決事項を記録する（このドキュメント） |
| 2 | 済 | `.work/notes/` のノートドキュメントを更新する |
| 3 | 済 | `plugins/work/skills/start/SKILL.md` — Step 1 に `WORK_BRANCH_AUTHOR` チェックを追加、Naming 注釈を更新 |
| 4 | 済 | `plugins/work/skills/start/SKILL.jp.md` — JP ミラーを同期 |
| 5 | 済 | `plugins/work/CLAUDE.md` — Environment Variables 表に追加、Changelog を更新 |
| 6 | 済 | `plugins/work/CLAUDE.jp.md` — JP ミラーを同期 |
| 7 | 済 | ルール / CLAUDE.md を更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/start/SKILL.md` | 編集 | Step 1 に WORK_BRANCH_AUTHOR チェックを追加 | - |
| 2 | `plugins/work/skills/start/SKILL.jp.md` | 編集 | JP ミラーを同期 | - |
| 3 | `plugins/work/CLAUDE.md` | 編集 | 環境変数テーブルとChangelog に追加 | - |
| 4 | `plugins/work/CLAUDE.jp.md` | 編集 | JP ミラーを同期 | - |

## テスト

上記実装に伴って追加・変更したテストファイル。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テストファイルなし | スキル定義のみ変更 |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

（未決事項なし）

## 参考ドキュメント

- `.work/notes/envトグル実装メモ.md`: work プラグイン env var の設計ノート（WORK_BRANCH_AUTHOR セクション参照）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
