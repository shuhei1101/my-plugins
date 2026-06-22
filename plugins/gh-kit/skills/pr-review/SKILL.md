---
name: gh-kit:pr-review
description: 1 件の PR をレビューし、承認かつ assignees がなければ base 取り込み→コンフリクト解消→--no-ff マージ→worktree 削除→push まで自走する
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
| 現在 assignees 一覧 | assignees の有無を判定するのに使う |

## ステップ 0: Wiki チェックリストを読み込む

`GH_KIT_CHECKLIST_PAGES` が設定されている場合に限り、指定されたチェックリストページをリモート Wiki から取得してコンテキストに注入する。
ページが存在しない場合は警告を出力して続行する。

```bash
REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
IFS=',' read -ra PAGES <<< "${GH_KIT_CHECKLIST_PAGES:-共通チェックリスト}"
for PAGE in "${PAGES[@]}"; do
  PAGE=$(echo "$PAGE" | xargs)  # trim whitespace
  CONTENT=$(curl -fsSL "https://raw.githubusercontent.com/wiki/${REPO_SLUG}/${PAGE}.md" 2>/dev/null)
  if [ -n "$CONTENT" ]; then
    echo "# Wiki チェックリスト: $PAGE"
    echo "$CONTENT"
  else
    echo "[INFO] Wiki チェックリストページが見つかりません: ${PAGE}.md" >&2
  fi
done
```

取得できたチェックリスト内容は、ステップ 3 のレビューで確認項目として観点メニューと合わせて参照する。

## ステップ 1: 観点メニューを取得

```bash
curl -fsSL "https://raw.githubusercontent.com/wiki/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/観点メニュー.md"
```

ステップ 3 で参照する。

## ステップ 2: PR 情報を取得

```bash
gh pr view {N} --json number,title,body,headRefName,baseRefName,labels,assignees,statusCheckRollup,comments,reviews,isDraft
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
| minor / nit のみ + assignees なし | `--approve` | ステップ 6（マージへ） |
| minor / nit のみ + assignees あり | `--approve` | ステップ 7-B（マージしない） |

## ステップ 6: マージ実行（approve + assignees なしのみ）

ワークツリーを最新化したうえで親ブランチを取り込み、コンフリクトがあれば AI が解消し、`--no-ff` で base にマージ、worktree を削除して push する。

```bash
WT=".claude/worktrees/$(echo {HEAD_BRANCH} | tr '/' '-')"
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{HEAD_BRANCH}
git -C "$WT" merge origin/{BASE_BRANCH}
```

コンフリクトが残ったら `git -C "$WT" status -s` で UU / AA / DD などのコードを確認し、両側の意図を読んで「意味が強い」方を採用または両立させる（`-X ours` / `-X theirs` 一括解消は禁止）。解消後 `git -C "$WT" add` / `git -C "$WT" commit`。

自走解消できなかった場合（コンフリクトが残る場合）は、以下を実行してユーザーに通知する:

```bash
# コンフリクトファイル一覧を取得
CONFLICT_FILES=$(git -C "$WT" status -s | grep '^UU\|^AA\|^DD' | awk '{print "- `" $2 "`"}')
```

リモート Wiki から `コンフリクト通知コメント` ページを取得し、以下の変数を埋めて `gh pr comment` で投稿する:

```bash
# Wiki からテンプレートを取得
curl -fsSL "https://raw.githubusercontent.com/wiki/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/コンフリクト通知コメント.md"
```

| 変数 | 内容 |
|---|---|
| `{head_branch}` | HEAD ブランチ名 |
| `{base_branch}` | BASE ブランチ名 |
| `{conflict_files}` | `$CONFLICT_FILES` の値 |
| `{conflict_reason}` | AI が判断した解消不能の理由（例: 両側で同箇所に別ロジックが追加されており自動判定不可） |

```bash
# テンプレートに変数を埋めたコメントを投稿
gh pr comment {PR_NUMBER} --body "{テンプレートに変数を埋めた本文}"

# assignee にユーザーを追加して通知
gh pr edit {PR_NUMBER} --add-assignee @me
```

```bash
git -C {REPO_ROOT} merge --no-ff -m "{type}: {title}" {HEAD_BRANCH}
```

`gh-kit-tools` MCP の `worktree_remove`（`branch={HEAD_BRANCH}`）を呼んでワークツリーとブランチを削除。リモートブランチを削除してから base ブランチを push する。

```bash
git push origin --delete {HEAD_BRANCH}
git -C {REPO_ROOT} push origin {BASE_BRANCH}
```

マージ完了後、紐づく Issue を Close し、`processing:*` ラベルを除去する。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# PR 本文から "Refs #N" または "Closes #N" で Issue 番号を抽出
ISSUE_N=$(gh pr view {PR_NUMBER} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue close "$ISSUE_N"
  gh issue edit "$ISSUE_N" \
    --remove-label "$LABEL_PROCESSING_PR_DRAFT" \
    --remove-label "$LABEL_PROCESSING_PR_IMPLEMENT" \
    --remove-label "$LABEL_PROCESSING_PR_REVIEW"
fi
```

| 状況 | verdict |
|---|---|
| 全て成功 | `approved-merged` |
| コンフリクトが自走解消できず残る（コメント通知 + assignee 追加済み） | `conflict` |
| その他失敗 | `failed` |

## ステップ 7-A: changes-requested

マージしない。verdict = `changes-requested`、message に主要 finding を要約。

## ステップ 7-B: approved-user-review-pending

マージしない。verdict = `approved-user-review-pending`、message に「ユーザー確認待ち（assignees 設定済み）」と理由。

ユーザーが内容を確認したら、以下の操作をすることで次回 `pr-review-auto` の Monitor が自動検知してマージフローへ進む:
1. PR に `user-reviewed` ラベルを付与する
2. assignees を外す（自身を remove する）

`pr-review-auto` は `user-reviewed` ラベル付きの Ready PR（assignees なし）を検知したとき、AI レビュー済みとみなしてマージを実行する。

## ステップ 7-C: Drop（PR Close without merge）

PR を `--close` した場合（failed / conflict）も `processing:*` ラベルを除去する（Issue は Close しない）。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
ISSUE_N=$(gh pr view {PR_NUMBER} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" \
    --remove-label "$LABEL_PROCESSING_PR_DRAFT" \
    --remove-label "$LABEL_PROCESSING_PR_IMPLEMENT" \
    --remove-label "$LABEL_PROCESSING_PR_REVIEW"
fi
```

## 制約

| No | 禁止 |
|---|---|
| 1 | 自身の中でサブエージェントを起動しない |
| 2 | `git push --force` を使わない |
| 3 | assignees が設定されている PR を AI 単独でマージしない |
| 4 | 変更行から離れた箇所に inline コメントを付けない |
