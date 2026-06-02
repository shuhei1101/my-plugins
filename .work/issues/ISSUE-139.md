# ISSUE-139: branch-show の「merge Step 12」参照が古い（現在は Step 13）

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見

---

## 概要

`plugins/work/skills/branch-show/SKILL.md` の Overview および Step 1 が `work:branch-show` を「merge Step 12 から抽出されたスキル」と記述しているが、現在の `merge` スキルでは branch-show は **Step 13** で呼び出されており、Step 12 は「Report merge completion」になっている。

## 背景

スキルが分割・再編された際にステップ番号が変わったが、branch-show 側の参照が更新されなかった。直接的な動作影響はないが、スキルの説明を読む開発者が混乱する。

## 現状

`plugins/work/skills/branch-show/SKILL.md`:
- 行 14: `A standalone skill extracted from merge Step 12.`
- 行 31: `1. If called with a task document path argument (e.g. from merge Step 12), use that file directly`

`plugins/work/skills/merge/SKILL.md`:
- 行 362: `### Step 12: Report merge completion`（branch-show を呼ばない）
- 行 373: `### Step 13: Present next branch candidates in 3 categories`（ここで branch-show を呼ぶ）
- 行 377: `Invoke `/work:branch-show` passing the merged task document path as the data source.`

## 期待される状態

branch-show SKILL.md の「Step 12」参照を「Step 13」に修正する。

## 対応案

`plugins/work/skills/branch-show/SKILL.md` の行 14 と行 31 の `Step 12` を `Step 13` に修正する。変更は 2 か所のみの 1 行修正。
