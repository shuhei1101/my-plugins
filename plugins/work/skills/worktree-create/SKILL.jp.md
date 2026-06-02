---
name: worktree-create
description: |
  ブランチ用のgitワークツリーを作成します。work:start（Step 4）から呼び出されてワークツリーを作成するか、
  直接実行されます。「ワークツリーを作って」「worktree を作成して」「work-add して」
  またはwork:startから `/work:worktree-create` として実行されたときにトリガー。
---

<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:worktree-create — ワークツリーを作成

git ワークツリーとブランチを作成します。

> **命名規則**: ブランチは `{type}/{title}` を使用します（`PR{N}/` プレフィックスなし）。
> ワークツリーパスはブランチ名を反映して `../{repo}-wt-{type}-{title}` となります
> （スラッシュはハイフンに置き換え）。
> レガシー `wt-PR{N}` 命名法のワークツリーはそのまま残されます — 新しく作成されたワークツリーのみ
> 新しい形式に従います。

---

## タスク

### ステップ 1: 引数を解析

#### 条件

- 常に実行 — 最初に実行

#### 処理

1. 引数が指定されている場合（例：`refactor/rename-pr-to-branch`）、それを解析します：
   - 単一の引数：ブランチ名（`{type}/{title}`）
   - レガシー実行 `/work:worktree-create PR58 refactor/foo` も後方互換性のため受け付けます：
     `PR{N}` トークンは削除され、ブランチサフィックスのみが使用されます
2. 引数なしで呼び出された場合、ユーザーに質問します：
   - ブランチタイプ（`feat` / `fix` / `refactor` / `docs` / `chore` / `test`）
   - タイトル（kebab-case）

→ ステップ 2 へ

#### 出力

- `BRANCH` — 完全なブランチ名（`{type}/{title}`）

---

### ステップ 2: ワークツリーを作成

#### 条件

- Step 1 完了

#### 処理

1. スラッシュをハイフンで置き換えてワークツリーサフィックスを派生させます：

```bash
BRANCH=refactor/rename-pr-to-branch
WT_SUFFIX="${BRANCH//\//-}"  # → refactor-rename-pr-to-branch
```

2. `${WORK_BASE_BRANCH}` を読み込みます：

```bash
base="${WORK_BASE_BRANCH:-}"
```

3. ワークツリーとブランチを作成します：

```bash
if [ -n "$base" ]; then
  git worktree add -b "$BRANCH" "../$(basename $(pwd))-wt-${WT_SUFFIX}" "$base"
else
  git worktree add -b "$BRANCH" "../$(basename $(pwd))-wt-${WT_SUFFIX}"
fi
```

→ ステップ 3 へ

#### 出力

- ワークツリーが `../{repo}-wt-{type}-{title}` に作成されました
- ブランチ `{type}/{title}` が存在します

#### 注記

##### 禁止事項

- master/main に直接コミットしないでください

---

### ステップ 3: 呼び出し元に報告

#### 条件

- Step 2 完了

#### 処理

1. 作成されたワークツリーパスとブランチ名を報告
2. `work:start` から呼び出された場合、呼び出し元に制御を返す

#### 出力

- ワークツリーパス：`../{repo}-wt-{type}-{title}`
- ブランチ名：`{type}/{title}`
