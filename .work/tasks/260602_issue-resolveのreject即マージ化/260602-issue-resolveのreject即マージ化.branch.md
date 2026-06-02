# issue-resolveのreject即マージ化

> ブランチ: refactor/issue-resolve-reject-immediate-merge

## 概要

issue-resolve の REJECT フローを、共有 `chore/rejected-issues` ブランチへの蓄積方式から、
reject ごとに一時ブランチを切って即 master へマージする方式に変更する。

### 実施条件

即時実施可

### 背景・問題

旧フローは reject されたイシューを共有 `chore/rejected-issues` ブランチに溜め、ユーザーが
後でまとめてマージする設計だった。しかし `.work/issues/_index.yaml` は gitignore（作業コピー
ごとに別物）で、Step 1 が読むのはメインリポの `_index.yaml`。reject の close を worktree 側で
行うとメインリポの `_index.yaml` が更新されず、ファイル移動（master へ未マージ）と status が
乖離し続ける。reject が溜まるほど整合性が崩れていく。

## 作業内容

| No | 完了 | 作業 |
|---|---|---|
| 1 | | Step 2 を「メインリポで close → 一時ブランチへ追跡変更を載せ即 master マージ → ブランチ削除」に書き換え |
| 2 | | frontmatter description / Overview / Step 4 報告文から共有ブランチ蓄積の記述を更新 |
| 3 | | SKILL.jp.md を同期 |
| 4 | | plugins/work/CLAUDE.md のライフサイクル記述・Skills 表・Changelog を更新 |
| 5 | | plugin.json / marketplace.json のバージョンを bump |
| 6 | | QA をこのドキュメントに記録 |
| 7 | | ノートを更新（該当あれば） |

## QA

（このセクションは Step 7 で追記）

## テスト

| No | 完了 | 項目 |
|---|---|---|
| 1 | | SKILL.md / SKILL.jp.md の Step 2 が新フロー（メインリポ close → 即マージ）で一貫しているか目視確認 |

## 変更内容

（実装中に記録）

## 参考ドキュメント

（最終コミットで追記）
