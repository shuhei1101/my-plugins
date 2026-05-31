# refactor/fix-terminology-in-work-plugin

> 内部 ID: 248（index.yaml 採番用 — クロスリファレンス目的）

## 概要

workプラグイン内に残っている「PR」「プルリクエスト」などのGitHub由来の用語をすべて「ブランチ」に統一する。
また `user-prompt-submit.py` 内の古い形式の参照（QA・ToDo確認手順など）を現在のブランチ文書構造に合わせて修正する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | workプラグイン全体を「PR」「プルリクエスト」で grep し、修正箇所を洗い出す |
| 2 | 済 | `user-prompt-submit.py` の古い表記（QA/ToDo確認手順など）を現在の構造に合わせて修正 |
| 3 | 済 | 洗い出した「PR」→「ブランチ」置換を実施 |
| 4 | 済 | ルール・CLAUDE.md の更新（不要と判断 — 変更はenv var名とコメントのみ） |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/hooks/scripts/user-prompt-submit.py` | 編集 | docstring コメント・`WORK_PR_ENFORCEMENT`→`WORK_BRANCH_ENFORCEMENT` | - |
| 2 | `plugins/work/scripts/trim-index.py` | 編集 | "PR entries/PR(s)" → "branch entries/branch(es)" | - |
| 3 | `plugins/work/scripts/issue-tool.py` | 編集 | `--linked-pr`→`--linked-branch`、`linked_pr`→`linked_branch` | - |
| 4 | `plugins/work/skills/plugin-config/SKILL.md` | 編集 | `WORK_PR_ENFORCEMENT`→`WORK_BRANCH_ENFORCEMENT` | - |
| 5 | `plugins/work/skills/plugin-config/SKILL.jp.md` | 編集 | 〃 | JPミラー |
| 6 | `plugins/work/skills/setup/SKILL.md` | 編集 | "PR folders"→"branch folders" | - |
| 7 | `plugins/work/skills/setup/SKILL.jp.md` | 編集 | "PR フォルダ"→"ブランチフォルダ" | JPミラー |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | （テスト変更なし） | - | - | - |

## QA

（なし）

## 参考ドキュメント

- `.work/notes/PR用語廃止・ブランチ用語統一.md`: 同テーマの先行変更履歴と方針

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/rename-pr-to-branch | 同系統のPR→ブランチ用語リネーム（先行ブランチ） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | （なし） | - | - |
