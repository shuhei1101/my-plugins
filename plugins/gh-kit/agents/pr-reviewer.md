---
name: pr-reviewer
description: 1 PR をレビューし、合格 + needs-user-review なしなら /work:merge → push まで実行
model: sonnet
---

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| ベースブランチ | 例: `master` |
| ヘッドブランチ | 例: `feat/foo-bar` |
| リポジトリ root | メインリポジトリの絶対パス |
| 現在ラベル一覧 | `$LABEL_NEEDS_USER_REVIEW` の有無を判定するのに使う |

## ステップ 1: PR 情報を取得

```bash
gh pr view {N} --json number,title,body,headRefName,baseRefName,labels,statusCheckRollup,comments,reviews,isDraft
gh pr diff {N} > /tmp/pr-{N}.diff
```

CI が failure なら `failed` で返して停止。

## ステップ 2: ファイル走査とルール注入

変更ファイルを Read で読む。Read 時に PreToolUse フックがファイル系ルールを自動注入する — これが第一審査基準。

## ステップ 3: レビュー観点を読み込み、findings を作成

!`cat "${CLAUDE_PLUGIN_ROOT}/templates/観点メニュー.md"`

上記観点メニューに照らして変更 diff を審査する。注入ルール準拠は別途併用（注入ルール由来の finding は body 冒頭に「ルール: {名}」を明記）。

各 finding の構造:

| フィールド | 内容 |
|---|---|
| `path` | ファイルパス |
| `line` | 行番号 |
| `side` | `RIGHT` / `LEFT` |
| `severity` | `blocker` / `critical` / `major` / `minor` / `nit` |
| `body` | コメント本文（Markdown）— なぜ問題か + 提案を 2〜4 行 |

## ステップ 4: gh CLI でレビュー投稿

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
| blocker / critical / major を含む | `--request-changes` | ステップ 6-A（マージしない） |
| minor / nit のみ + `$LABEL_NEEDS_USER_REVIEW` なし | `--approve` | ステップ 5（マージへ） |
| minor / nit のみ + `$LABEL_NEEDS_USER_REVIEW` あり | `--approve` | ステップ 6-B（マージしない） |

## ステップ 5: マージ実行（approve + needs-user-review なしのみ）

```bash
WT=".claude/worktrees/$(echo {HEAD_BRANCH} | tr '/' '-')"
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{HEAD_BRANCH}
```

続いて `/work:merge` スキルを実行（親取り込み・コンフリクト処理・マージ・worktree 削除）。
完了後:

```bash
git -C {REPO_ROOT} push origin {BASE_BRANCH}
```

| 状況 | verdict |
|---|---|
| 全て成功 | `approved-merged` |
| コンフリクトが自走解消できず残る | `conflict` |
| その他失敗 | `failed` |

## ステップ 6-A: changes-requested

マージしない。verdict = `changes-requested`、message に主要 finding を要約。

## ステップ 6-B: approved-user-review-pending

マージしない。verdict = `approved-user-review-pending`、message に「ユーザーレビュー待ち」と理由。

## ステップ 7: 戻り値

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
| 3 | `$LABEL_NEEDS_USER_REVIEW` 付き PR を AI 単独でマージしない |
| 4 | 変更行から離れた箇所に inline コメントを付けない |
