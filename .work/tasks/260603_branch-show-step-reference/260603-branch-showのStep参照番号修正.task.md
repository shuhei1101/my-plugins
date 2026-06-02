# branch-show の Step 参照番号修正

**ブランチ**: fix/branch-show-step-reference
**作成日**: 2026-06-03

## 作業内容

| # | 内容 | 完了 |
|---|---|---|
| 1 | merge/SKILL.md を確認し、`/work:branch-show` が呼び出される実ステップ番号を確認する | 済 |
| 2 | branch-show/SKILL.md の `Step 12` 参照（行 14・行 31）を正しい番号に修正する | - |
| 3 | branch-show/SKILL.jp.md の対応する参照を EN に合わせて修正する | - |

## QA

（なし）

## テスト

- merge/SKILL.md を確認: `/work:branch-show` は **Step 13** で呼び出されている（行 377）
- Step 12 は「Report merge completion」でブランチ表示とは無関係
- branch-show/SKILL.md の `Step 12` を `Step 13` に 2 箇所修正
- branch-show/SKILL.jp.md の `Step 12` を `Step 13` に 2 箇所修正

## 変更内容

`plugins/work/skills/branch-show/SKILL.md` の Overview と Step 1 に残っていた旧ステップ番号参照を修正。
JP ミラーも同様に修正。

## 関連イシュー

| イシュー ID | タイトル | 状態 |
|---|---|---|
| ISSUE-139 | branch-show の「merge Step 12」参照が古い（現在は Step 13） | in_progress |

## 参考ドキュメント

（なし）

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
