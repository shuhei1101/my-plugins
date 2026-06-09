<!-- This file is a Japanese mirror of merge-theirs-loses-branch-only-additions.md. When updating the English original, update this file too. -->

# 大幅に編集された共有ファイルに対して `git merge master -X theirs` を使うと、ブランチ側のみの追記が静かに消える

## 状況

- PR: PR168（`refactor-task-doc-structure`）
- 日付: 2026-05-30

## 起きたこと

PR168 は long-running PR で、待っている間に master が 5 PR（PR165 / PR166 / PR169 / PR170 / PR172）で大幅にリファクタされていた。ユーザーに「master が正解、その上に PR168 を重ねる」と判断してもらい、以下を実行した:

```bash
git merge master -X theirs
```

`plugins/work-kit/` → `plugins/workspace/` リネーム、`mark-generated` 廃止、`version-sync` 廃止など多数の構造衝突を、全部 master 側を優先して一括解消する狙い。

**master も触ったファイル**については期待通り master 版が勝ち問題なし。しかし PR168 は `.claude/rules/core/glossary.md`（PR172 で master 側も大量編集していた）に**新規エントリ 4 件を追記**していた。これらは master の編集とは別箇所への追加だったにも関わらず、merge 後のファイルからきれいに消えていた — 追加分はゼロ。

気づいたのは merge 直後に新用語名を grep したから:

```bash
grep -n "PR168\|plugin-update\|変更内容セクション\|テストセクション\|単一ファイル化" .claude/rules/core/glossary.md
# (出力なし)
```

4 件を手で再追記すれば済んだが、確認せずにコミットしていたら静かに失われていた。

## 教訓

`-X theirs` は両側で append が起きているファイルに対しては精度を欠く。git の auto-merge は「両方 modified」と見たファイル全体について theirs を選び、ブランチ側のファイル別箇所への追記を巻き込んで消すことがある。long-lived ブランチへの `-X theirs` merge 後は以下を必須にする:

- 自分の PR が **追記**したファイルを全て洗い出す（編集や移動ではなく追記）: glossary、incidents、marketplace のプラグイン一覧、index 系ファイルなど。
- 各ファイルに対し、PR を識別できる文字列（新用語名・新ファイルパス・PR 番号）で merge 直後に `grep` する。
- 欠落があれば、merge コミット前に手で再追記する。

ブランチ側の追記が孤立しているのが事前に分かっている場合は、`-X theirs` を使わず、append 型のファイルだけは手で「both modified」を解消するほうが安全（他のファイルは theirs で OK でも）。

## 関連

- `large-master-adapt-user-decisions.md` — long-running PR で master が大変動した時の判断パターン。本件はそれを実行するときの「どの戦略を取るか」の後続教訓。
- `parallel-pr-version-bump-collision.md` — long-running PR が master から離れたときの別パターン。
