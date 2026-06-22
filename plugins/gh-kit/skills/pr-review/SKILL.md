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

`GH_KIT_WIKI_PATH` と `GH_KIT_CHECKLIST_PAGES` が設定されている場合に限り、指定されたチェックリストページをコンテキストに注入する。
ページが存在しない場合は警告を出力して続行する（未設定プロジェクトでも従来通り動作する）。

```bash
IFS=',' read -ra PAGES <<< "${GH_KIT_CHECKLIST_PAGES:-共通チェックリスト}"
for PAGE in "${PAGES[@]}"; do
  PAGE=$(echo "$PAGE" | xargs)  # trim whitespace
  if [ -n "$GH_KIT_WIKI_PATH" ]; then
    FILE="$GH_KIT_WIKI_PATH/${PAGE}.md"
    if [ -f "$FILE" ]; then
      echo "# Wiki チェックリスト: $PAGE"
      cat "$FILE"
    else
      echo "[INFO] Wiki チェックリストページが見つかりません: $FILE" >&2
    fi
  fi
done
```

取得できたチェックリスト内容は、ステップ 3 のレビューで確認項目として観点メニューと合わせて参照する。

## ステップ 1: 観点メニューを取得

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/観点メニュー.md"
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
| blocker / critical / major を含む | `--request-changes` | ステップ 7-A（ラベルなし） |
| minor / nit のみ + assignees なし | `--approve` | ステップ 6（`approved-merge-ok` ラベル付与） |
| minor / nit のみ + assignees あり | `--approve` | ステップ 7-B（ラベルなし） |

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
