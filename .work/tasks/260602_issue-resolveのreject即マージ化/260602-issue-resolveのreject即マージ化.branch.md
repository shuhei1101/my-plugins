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
| 1 | 済 | Step 2 を「メインリポで close → 一時ブランチへ追跡変更を載せ即 master マージ → ブランチ削除」に書き換え |
| 2 | 済 | frontmatter description / Overview / Step 4 報告文から共有ブランチ蓄積の記述を更新 |
| 3 | 済 | SKILL.jp.md を同期 |
| 4 | 済 | plugins/work/CLAUDE.md（+ JP ミラー）のライフサイクル記述・Skills 表・Changelog を更新 |
| 5 | 済 | plugin.json / marketplace.json のバージョンを 2.68.0 へ bump |
| 6 | 済 | QA をこのドキュメントに記録（ブロッカーなし） |
| 7 | 済 | ノート（イシュー対応ワークフロー）を更新 |

## QA

（ブロッカーなし。設計判断はユーザーの「reject は即マージ／ステータス変更の master 直コミットは取り下げ」
の指示で確定済み。close をメインリポで実行する点は `_index.yaml` の gitignore 特性から必然的に決まる。）

## テスト

| No | 完了 | 項目 |
|---|---|---|
| 1 | | SKILL.md / SKILL.jp.md の Step 2 が新フロー（メインリポ close → 即マージ）で一貫しているか目視確認 |

## 変更内容

- `plugins/work/skills/issue-resolve/SKILL.md` / `SKILL.jp.md`: Step 2 を「使い捨てブランチでクローズ
  → 即 master マージ」に全面書き換え。frontmatter description・Overview・Step 4 報告文も更新。
- `plugins/work/CLAUDE.md` / `CLAUDE.jp.md`: イシューライフサイクル記述・Skills 表・Changelog を更新。
- `plugins/work/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json`: 2.67.0 → 2.68.0。
- ガード調査結果: master 直 `git commit` は `master-commit-guard` でブロック（マージ中は素通り）。
  master への `git merge <feature>` は `git-guard` で 1 回確認（トークンでリトライは素通り）。
  → 「直コミット」は不可、「ブランチ→即マージ」は確認 1 回で可能。

## 参考ドキュメント

- `.work/notes/ワークフロー・マージ/イシュー対応ワークフロー.md`
- `.work/notes/スキル設計/issue-resolveスキル.md`
