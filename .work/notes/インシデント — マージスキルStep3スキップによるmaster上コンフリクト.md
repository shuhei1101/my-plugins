---
created_at: 2026-05-31
updates:
  - 2026-05-31 — fix/merge-skill-sync-before-merge: スキップ分岐を削除して再発防止
related_notes: []
related_branches:
  - fix/merge-skill-sync-before-merge
  - refactor/python-script-style-unify
---

# インシデント — マージスキル Step 3 スキップによる master 上コンフリクト

## 何が起きたか

`work:merge` スキルを使って `refactor/python-script-style-unify` を master にマージしようとした際、
Step 3（master を worktree に取り込む）がスキップされ、Step 7 で master 上に直接
`git merge --no-ff refactor/python-script-style-unify` が実行された。

master と feature branch の両方で変更されていたファイルがあったため、master の作業ツリー上で
コンフリクトが発生した。コンフリクト解消の試みも失敗し、master が `MERGE_HEAD` を持つ
マージ進行中状態のまま放置された。

## なぜ起きたか

SKILL.md の Step 3 に以下の分岐があった：

```
git -C {WORKTREE_PATH} log HEAD..<PARENT_BRANCH> --oneline
If no output → the target branch has not moved; skip to Step 4.
```

このチェックが何らかの理由で「新コミットなし」と誤判定し、`git merge master` を実行せずに
Step 4 → Step 7 と進んだ。

## 影響

- master が `MERGE_HEAD` を持つ不正状態になった
- `git merge --abort` で復旧するまで他の操作が不可能だった
- コンフリクトファイル: `index.archive.yaml`, `Pythonスクリプト.md`, `Pythonスクリプト.jp.md`, `trim-index.py`

## 再発防止

`fix/merge-skill-sync-before-merge` ブランチで Step 3 を修正：

1. `git log` チェックとスキップ分岐を削除
2. `git merge <PARENT_BRANCH>` を **常に無条件で実行** するよう変更
   （既に最新の場合は `Already up to date.` で終わるため害がない）
3. Step 7 の禁止事項に「Step 3 がクリーンに完了していない場合は実行禁止」を追加

## 教訓

- `git merge` のような冪等に近い操作は「不要かもしれないから skip」より「必ず実行」にする
- master 上でコンフリクトが出た場合は `git merge --abort` で即座に中断し、worktree 側で解消してからやり直す
