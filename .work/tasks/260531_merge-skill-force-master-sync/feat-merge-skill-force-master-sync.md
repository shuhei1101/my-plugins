# feat/merge-skill-force-master-sync

> 内部 ID: 219（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`work:merge` スキルの Step 3 で、master に新しいコミットがある場合に自律判断ではなく**必ず** `git merge master` を実行してコンフリクトの有無を確認するよう変更する。コンフリクトが発生した場合はユーザーに解消を求めて停止し、クリーンな場合のみ Step 4 以降に進む。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | 済 | QAを `## QA` に記録 | - |
| 2 | 済 | ノートドキュメントを更新 | `.work/notes/work-kitスキル群.md` |
| 3 | 済 | Step 3 を「master有新コミット → 必ず merge master → コンフリクトなら停止」に書き換え | `plugins/work/skills/merge/SKILL.md` |
| 4 | 済 | ルール / CLAUDE.md 更新（変更なし） | - |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/merge/SKILL.md` | 編集 | Step 3 を必須 master 取り込みフローに変更 | - |
| 2 | `plugins/work/skills/merge/SKILL.jp.md` | 編集 | 同上の日本語ミラー | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | — | — | テストファイルなし | — |

## QA

なし

## 参考ドキュメント

- `plugins/work/skills/merge/SKILL.md`: 変更対象のマージスキル
- `.work/notes/work-kitスキル群.md`: merge スキルの設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | — | — |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | — | — | — |
