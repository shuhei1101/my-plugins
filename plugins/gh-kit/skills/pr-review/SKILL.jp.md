---
name: gh-kit:pr-review
description: 1 件の PR をレビューし、承認かつ needs-user-review がなければ base 取り込み→コンフリクト解消→--no-ff マージ→worktree 削除→push まで自走する
---

# pr-review

PR を 1 件レビューし、合格時はそのまま base ブランチへマージする。

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| ベースブランチ | 例: `master` |
| ヘッドブランチ | 例: `feat/foo-bar` |
| リポジトリ root | メインリポジトリの絶対パス |
| 現在ラベル一覧 | `needs-user-review` の有無を判定するのに使う |

## ステップ 1: 観点メニューを取得

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/観点メニュー.md"
```

ステップ 3 で参照する。

## ステップ 2: PR 情報を取得

```bash
gh pr view {N} --json number,title,body,headRefName,baseRefName,labels,statusCheckRollup,comments,reviews,isDraft
gh pr diff {N} > /tmp/pr-{N}.diff
```

CI が failure なら `failed` で返して停止。

## ステップ 3: ファイル走査とルール注入

変更ファイルを Read で読む。Read 時に PreToolUse フックがファイル系ルールを自動注入する — これが第一審査基準。
ステップ 1 で取得した観点メニューと組み合わせて変更 diff を審査する。

注入ルール由来の finding は body 冒頭に「ルール: {名}」を明記する。

## ステップ 4: findings を作成

各 finding の構造:

| フィールド | 内容 |
|---|---|
| `path` | ファイルパス |
| `line` | 行番号 |
| `side` | `RIGHT` / `LEFT` |
| `severity` | `blocker` / `critical` / `major` / `minor` / `nit` |
| `body` | コメント本文（Markdown）— なぜ問題か + 提案を 2〜4 行 |

## ステップ 5: gh CLI でレビュー投稿

```bash
gh pr review {N} \
  --approve|--comment|--request-changes \
  --body-file <(cat <<'EOF'
{観点別サマリ}
EOF
)
# inline コメントが必要なら gh api repos/:owner/:repo/pulls/{N}/comments を使う
```

event 判定:

| 条件 | event | 次の動作 |
|---|---|---|
| blocker / critical / major を含む | `--request-changes` | ステップ 7-A（マージしない） |
| minor / nit のみ + `needs-user-review` なし | `--approve` | ステップ 6（マージへ） |
| minor / nit のみ + `needs-user-review` あり | `--approve` | ステップ 7-B（マージしない） |

## ステップ 6: マージ実行（approve + needs-user-review なしのみ）

ワークツリーを最新化したうえで親ブランチを取り込み、コンフリクトがあれば AI が解消し、`--no-ff` で base にマージ、worktree を削除して push する。

```bash
WT=".claude/worktrees/$(echo {HEAD_BRANCH} | tr '/' '-')"
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{HEAD_BRANCH}
git -C "$WT" merge origin/{BASE_BRANCH}
```

コンフリクトが残ったら `git -C "$WT" status -s` で UU / AA / DD などのコードを確認し、両側の意図を読んで「意味が強い」方を採用または両立させる（`-X ours` / `-X theirs` 一括解消は禁止）。解消後 `git -C "$WT" add` / `git -C "$WT" commit`。

```bash
git -C {REPO_ROOT} merge --no-ff -m "{type}: {title}" {HEAD_BRANCH}
```

`gh-kit-tools` MCP の `worktree_remove`（`branch={HEAD_BRANCH}`）を呼んでワークツリーとブランチを削除。最後に push。

```bash
git -C {REPO_ROOT} push origin {BASE_BRANCH}
```

| 状況 | verdict |
|---|---|
| 全て成功 | `approved-merged` |
| コンフリクトが自走解消できず残る | `conflict` |
| その他失敗 | `failed` |

## ステップ 7-A: changes-requested

マージしない。verdict = `changes-requested`、message に主要 finding を要約。

## ステップ 7-B: approved-user-review-pending

マージしない。verdict = `approved-user-review-pending`、message に「ユーザーレビュー待ち」と理由。

## ステップ 8: 戻り値

```json
{
  "verdict": "approved-merged" | "approved-user-review-pending" | "changes-requested" | "conflict" | "failed",
  "pr_number": 42,
  "branch": "feat/foo-bar",
  "message": "詳細メッセージ",
  "findings_count": {"blocker": 0, "critical": 0, "major": 1, "minor": 2, "nit": 3}
}
```

## 制約

| No | 禁止 |
|---|---|
| 1 | 自身の中でサブエージェントを起動しない |
| 2 | `git push --force` を使わない |
| 3 | `needs-user-review` 付き PR を AI 単独でマージしない |
| 4 | 変更行から離れた箇所に inline コメントを付けない |
