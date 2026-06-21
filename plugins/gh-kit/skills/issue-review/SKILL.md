---
name: gh-kit:issue-review
description: 1 Issue をレビューし、本文補完コメント（必要時のみ）+ レビュー結果コメントを gh CLI で投稿し、needs_user_review 判定を返す
---

# issue-review

GitHub Issue を 1 件レビューし、結果を gh CLI でコメント投稿する。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |

## ステップ 1: ラベル定義とテンプレートを読み込む

ラベル定数は bash 経由で取得（上記 `!` 構文で注入済み）。
テンプレート本文は `gh-kit-tools` MCP の `template_get` で取得:

| 用途 | template_name |
|---|---|
| Issue 本文テンプレート | `イシュードキュメント.j2` |
| レビュー結果コメント | `レビュー結果コメント.j2` |
| `needs-user-review` 判定基準 | `ユーザーレビュー要否判定.md` |

## ステップ 2: Issue とラベルを取得

```bash
gh issue view {N} --json number,title,body,labels,comments
```

ラベルに `ai-code-scan` が含まれるかで起票元を判定:

| ラベル | 起票元 | 本文の状態 |
|---|---|---|
| あり | claude code（`code-scanner`） | テンプレ準拠で揃っている |
| なし | 人間 | 概要・背景などが欠けている可能性大 |

## ステップ 2.5: 類似 Issue を検索

Issue のタイトル・本文からキーワードを 2〜4 個抽出し、`gh issue list` でオープン Issue を検索する:

```bash
# キーワードの組み合わせで 2〜3 回検索（クローズ済みは除外）
gh issue list --state open --search "{キーワード1} {キーワード2}" --json number,title,body --limit 20
```

レビュー対象の Issue 自身は結果から除外する。
全検索で最大 20 件の候補を収集する。

## ステップ 2.6: 類似度判定と処理分岐

ステップ 2.5 の候補リストに対し、LLM で各候補との類似度を判定する。

各ペアを以下の 3 分類に振り分ける:

| 分類 | 定義 | 処理 |
|---|---|---|
| `partial_overlap` | 現 Issue に既存 Issue にない情報が含まれるが、テーマが重複 | 差分を既存 Issue にコメント転記 → 現 Issue を転記先リンク付きでクローズ |
| `full_duplicate` | 現 Issue の内容が既存 Issue に完全に含まれる | 現 Issue を既存 Issue リンク付きでクローズ（転記なし） |
| `unrelated` | 有意な重複なし | スキップ（ステップ 3 へ進む） |

**partial_overlap 時の処理:**

```bash
# 1. 差分情報を抽出・要約（現 Issue にあって既存 Issue にない情報のみ）
# 2. 抽出内容を既存 Issue にコメント投稿
gh issue comment {EXISTING_N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による関連 Issue からの情報追記

## 追記情報（Issue #{N} より）

{差分要約: 既存 Issue に含まれていない追加情報のみを記載}

元 Issue: #{N}
EOF
)

# 3. 現 Issue をクローズコメント付きでクローズ
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による重複検出

類似する Issue #{EXISTING_N} が既に存在するため、この Issue をクローズします。
追加情報は #{EXISTING_N} にコメントとして転記しました。

移行先 Issue: {EXISTING_ISSUE_URL}
EOF
)
gh issue close {N}
```

**full_duplicate 時の処理:**

```bash
# 現 Issue をクローズコメント付きでクローズ
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による重複検出

Issue #{EXISTING_N} と完全に重複しているため、この Issue をクローズします。

既存 Issue: {EXISTING_ISSUE_URL}
EOF
)
gh issue close {N}
```

`partial_overlap` または `full_duplicate` が検出された場合、**ステップ 3〜6 をスキップ**してステップ 7 に直接ジャンプし、`status: "duplicate_merged"` または `status: "duplicate_closed"` を返す。

複数の候補がある場合は、類似度が高い順 → Issue 番号が小さい順（古い順）で優先する。

## ステップ 3: コードベースを読む

Issue が言及する領域・関連ファイルを Read で確認。Read 時に PreToolUse フックがファイル系ルールを自動注入する。

### Step 3a: Fetch official documentation (only when external tool/library names are present)

If the Issue title or body contains the name of an external tool, library, framework, or service:
1. Use `WebFetch` to retrieve the official documentation page(s) most relevant to the Issue.
2. If fetching fails, note "参照不可（理由）" and continue without blocking.
3. Record each successfully retrieved URL in `{doc_urls}` for use in the review-result comment.

Skip entirely when the Issue contains no external tool/library names.

## Step 3.5: Behavior verification (optional — when feasible)

Attempt to confirm whether the reported problem actually occurs in the current codebase.

| Issue type | Verification method |
|---|---|
| Skill / Claude Code behavior | Launch a sub-agent and reproduce the scenario described in the Issue |
| Code bug (test exists) | Run the relevant test suite and check for failures |
| Code bug (no test) | Perform manual behavior confirmation |
| Verification not feasible | Note "確認不可（理由）" and continue |

Store the result in `{verification_result}` for inclusion in the review-result comment.
This step is **optional** — if infrastructure or context makes it impossible, skip gracefully.

## ステップ 4: 本文補完コメントを投稿（必要時のみ）

人間起票で **本文に欠けているセクション** があるときに限り、`イシュードキュメント.j2` に沿って
**不足セクションだけ補う追加コメント** を投稿する。既に書かれているセクションは再掲しない。
本文が揃っている場合（AI 起票 or 人間起票でも完備）はこのステップをスキップ。

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による本文補完

## 概要
（欠けていた概要を記入）

## 背景
（欠けていた背景を記入）
EOF
)
```

## ステップ 5: レビュー結果コメントを投稿

ステップ 1 で取得した `レビュー結果コメント.j2` に沿って実装方針 / 質問 / 分割提案 / 影響範囲を書く。
質問・分割提案がなければ該当セクションごと省略。

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{レビュー結果本文}
EOF
)
```

## ステップ 6: `needs-user-review` 要否判定

ステップ 1 で取得した `ユーザーレビュー要否判定.md` に照らして判定する。
ステップ 5 で質問が含まれる場合・分割提案がある場合は無条件で true。

## ステップ 7: 戻り値

```json
{
  "issue_number": 42,
  "needs_user_review": true,
  "status": "ok"
}
```

`status` 取りうる値:

| 値 | 意味 |
|---|---|
| `ok` | 通常レビュー完了 |
| `duplicate_merged` | 部分重複 — 差分情報を既存 Issue に転記し、現 Issue をクローズ |
| `duplicate_closed` | 完全重複 — 現 Issue をリンク付きでクローズ |

ラベル付け替えは呼び出し側（`issue-review-auto`）の責務。

## 制約

- メイン Issue 本文は書き換えない（GitHub Issue API の `update` を呼ばない）
- 既存セクションが揃っているなら本文補完コメント（ステップ 4）はスキップ
- 推奨案は必ず明示（「後で決める」「TBD」禁止）
