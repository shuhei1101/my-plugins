---
name: gh-kit:pr-review
description: 1 件の PR をレビューし、合格かつ assignees がなければ approved-merge-ok ラベルを付与して pr-merger に委譲する
---

# pr-review

PR を 1 件レビューし、合格時は `approved-merge-ok` ラベルを付与して `pr-merger` に委譲する。
マージ責務は持たない（`pr-merge` スキルが実行する）。

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

## ステップ 2.5: PR 本文チェックリスト未消化チェック（最優先）

**このチェックは他のすべての verdict より優先される。**

ステップ 2 で取得した PR 本文を対象に、未消化チェックリスト（`- [ ]`）が 1 件以上残っていないか確認する。

```bash
# PR 本文の未消化チェックリスト数を確認（行頭の実チェックボックスのみ。インラインコード内の `- [ ]` は除外）
UNCHECKED=$(gh pr view {N} --json body --jq '.body' | python3 -c "
import sys, re
body = sys.stdin.read()
print(len(re.findall(r'^[ \t]*[-*] \[ \]', body, re.MULTILINE)))
")
echo "未消化チェックリスト数: $UNCHECKED"
```

| 条件 | 動作 |
|---|---|
| `- [ ]` の件数 >= 1 | **即座に `$GH_KIT_LABEL_NEEDS_FIX` ラベルを付与して差し戻し（ステップ 7-A へスキップ）** |
| `- [ ]` の件数 == 0 | ステップ 3 以降に進む |

`- [ ]` が残っている場合は以下を実行して処理を終了する:

```bash
# 確認:pr-implementer ラベルを付与（$GH_KIT_LABEL_NEEDS_FIX）
gh pr edit {N} --add-label "$GH_KIT_LABEL_NEEDS_FIX"

# 差し戻しコメントを投稿
gh pr comment {N} --body "$(cat <<'EOF'
## レビュー差し戻し: PR 本文にチェックリスト未消化が残っています

PR 本文に `- [ ]` が残っているため、レビューを開始できません。

**対応手順:**
1. `pr-implement` スキルのステップ 7.5 に従い、実装済みタスクを `- [x]` に更新してください
2. 未実装タスクが残る場合は、その理由を PR コメントに記載してください
3. 全チェックが完了したら再度 Ready にしてください
EOF
)"
```

verdict = `needs-fix`（`確認:pr-implementer` ラベル付与 + changes-requested 相当の差し戻し扱い）でスキルを終了する。

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

event 判定（優先度順）:

| 優先度 | 条件 | event | verdict | 次の動作 |
|---|---|---|---|---|
| 1（最優先） | PR 本文に `- [ ]` が 1 件以上残っている | ステップ 2.5 で処理済み | `needs-fix`（`確認:pr-implementer` ラベル付与） | ステップ 7-A へスキップ（ここには到達しない） |
| 2 | blocker / critical / major を含む | `--request-changes` | `changes-requested` | ステップ 7-A（ラベルなし） |
| 3 | minor / nit のみ + assignees なし | `--approve` | `approved-merge-ok` | ステップ 6（`approved-merge-ok` ラベル付与） |
| 4 | minor / nit のみ + assignees あり | `--approve` | `approved-user-review-pending` | ステップ 7-B（ラベルなし） |

## ステップ 6: approved-merge-ok ラベル付与（approve + assignees なしのみ）

マージは `pr-merger` スキルに委譲する。このスキルは `approved-merge-ok` ラベルを付与するだけで終了する。

```bash
gh pr edit {PR_NUMBER} --add-label "$GH_KIT_LABEL_APPROVED_MERGE_OK"
```

| 状況 | verdict |
|---|---|
| ラベル付与成功 | `approved-merge-ok` |
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
. "${CLAUDE_PLUGIN_ROOT}/scripts/constants.sh"
ISSUE_N=$(gh pr view {PR_NUMBER} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" \
    --remove-label "$LABEL_PROCESSING_PR_PLANNER" \
    --remove-label "$LABEL_PROCESSING_PR_IMPLEMENTER" \
    --remove-label "$LABEL_PROCESSING_PR_REVIEWER"
fi
```

## 制約

| No | 禁止 |
|---|---|
| 1 | 自身の中でサブエージェントを起動しない |
| 2 | `git push --force` を使わない |
| 3 | assignees が設定されている PR を AI 単独でマージしない |
| 4 | 変更行から離れた箇所に inline コメントを付けない |
