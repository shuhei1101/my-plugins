---
name: work-add
description: |
  Create a git worktree for a branch.
  Called by workspace:work-start (Step 4) to create the worktree, or invoked directly.
  Trigger when the user says "ワークツリーを作って", "worktree を作成して", "work-add して",
  or invoked by work-start as `/workspace:work-add`.
---

<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# workspace:work-add — ワークツリーを作成する

ギットワークツリーとブランチを作成します。

> **命名規則**: ブランチは `{type}/{title}` の形式を使用します（`PR{N}/` プレフィックスなし）。ワークツリーパスはブランチ名をミラーして `../{repo}-wt-{type}-{title}` となります（スラッシュはハイフンに置き換え）。
> レガシー命名 `wt-PR{N}` の既存ワークツリーはそのまま保持されます — 新しく作成されるワークツリーのみが新形式に従います。

---

## タスク

### ステップ 1: 引数の解決

#### 条件

- 常に実行 — 最初に実行

#### プロセス

1. 引数付きで呼び出された場合（例：`refactor/rename-pr-to-branch`）、それを解析します:
   - 単一引数: ブランチ名（`{type}/{title}`）
   - レガシー呼び出し `/workspace:work-add PR58 refactor/foo` も後方互換のため受け入れます: `PR{N}` トークンは破棄され、ブランチサフィックスのみが使用されます。
2. 引数なしで呼び出された場合、ユーザーに尋ねます:
   - ブランチタイプ（`feat` / `fix` / `refactor` / `docs` / `chore` / `test`）
   - タイトル（ケバブケース）

→ ステップ 2 に進む

#### 出力

- `BRANCH` — 完全なブランチ名（`{type}/{title}`）

---

### ステップ 2: ワークツリーを作成する

#### 条件

- ステップ 1 完了

#### プロセス

1. スラッシュをハイフンに置き換えることでワークツリーサフィックスを派生させます:

```bash
BRANCH=refactor/rename-pr-to-branch
WT_SUFFIX="${BRANCH//\//-}"  # → refactor-rename-pr-to-branch
```

2. ワークツリーとブランチを作成します:

```bash
git worktree add -b "$BRANCH" "../$(basename $(pwd))-wt-${WT_SUFFIX}"
```

→ ステップ 3 に進む

#### 出力

- ワークツリーが `../{repo}-wt-{type}-{title}` に作成される
- ブランチ `{type}/{title}` が存在する

#### 注釈

##### 禁止項目

- master/main に直接コミットしない

---

### ステップ 3: 呼び出し元に報告する

#### 条件

- ステップ 2 完了

#### プロセス

1. 作成されたワークツリーパスとブランチ名を報告します
2. `work-start` から呼び出された場合は、呼び出し元に制御を戻します

#### 出力

- ワークツリーパス: `../{repo}-wt-{type}-{title}`
- ブランチ名: `{type}/{title}`
