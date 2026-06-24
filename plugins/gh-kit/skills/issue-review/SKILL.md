---
name: gh-kit:issue-review
description: 1 Issue をレビューし、本文補完コメント（必要時のみ）+ レビュー結果コメントを gh CLI で投稿し、needs_user_review 判定を返す
---

# issue-review

GitHub Issue を 1 件レビューし、結果を gh CLI でコメント投稿する。

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |

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

取得できたチェックリスト内容は、ステップ 5 のレビューで確認項目として参照する。

## ステップ 1: テンプレートを読み込む

ラベル定数は Session Start フックで自動展開済み（`GH_KIT_LABEL_*` 変数が利用可能）。
テンプレート本文はリモート Wiki から取得する:

```bash
REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
WIKI_BASE="https://raw.githubusercontent.com/wiki/${REPO_SLUG}"
```

| 用途 | Wiki ページ名 | curl コマンド例 |
|---|---|---|
| Issue 本文テンプレート | `イシュードキュメント` | `curl -fsSL "${WIKI_BASE}/イシュードキュメント.md"` |
| レビュー結果コメント | `レビュー結果コメント` | `curl -fsSL "${WIKI_BASE}/レビュー結果コメント.md"` |
| ユーザー確認要否判定基準 | `ユーザー確認要否判定` | `curl -fsSL "${WIKI_BASE}/ユーザー確認要否判定.md"` |

## ステップ 2: Issue とラベルを取得

```bash
gh issue view {N} --json number,title,body,labels,comments
```

ラベルに `AIコードスキャン` が含まれるかで起票元を判定:

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

### ステップ 3a: 公式ドキュメント取得（外部ツール・ライブラリ名がある場合のみ）

Issue タイトルや本文に外部ツール・ライブラリ・フレームワーク・サービス名が含まれる場合:
1. `WebFetch` で Issue に最も関連する公式ドキュメントページを取得する。
2. 取得に失敗した場合は「参照不可（理由）」と記録し、処理を継続する。
3. 取得に成功した各 URL を `{doc_urls}` に記録し、レビュー結果コメントで使用する。

Issue に外部ツール・ライブラリ名が含まれない場合はスキップ。

## ステップ 3.5: 動作確認（任意 — 実施可能な場合のみ）

報告された問題が現在のコードベースで実際に発生するかを確認する。

| Issue の種類 | 確認方法 |
|---|---|
| スキル / Claude Code の動作 | サブエージェントを起動し、Issue に記載されたシナリオを再現する |
| コードバグ（テストあり） | 関連テストスイートを実行し、失敗を確認する |
| コードバグ（テストなし） | 手動で動作確認を行う |
| 確認不可 | 「確認不可（理由）」と記録し、処理を継続する |

結果を `{verification_result}` に格納し、レビュー結果コメントに含める。
このステップは**任意**。インフラやコンテキストの都合で実施不可能な場合はスキップしてよい。

## ステップ 3.75: タイトル更新（人間起票のみ）

`ai-code-scan` ラベルが **ない**（人間起票）場合のみ実行する。

Issue の本文・コメントを読んだうえで、内容を正確に表す適切なタイトルを生成し、`gh issue edit --title` で更新する。

```bash
gh issue edit {N} --title "{生成したタイトル}"
```

### タイトル生成ガイドライン

| 項目 | 内容 |
|---|---|
| 形式 | `{スコープ}: {動詞} — {対象}` を推奨（例: `gh-kit:issue-review — 人間起票 Issue のタイトルを自動更新する責務を追加`） |
| 長さ | 60〜80 文字以内 |
| 言語 | Issue 本文に合わせる（日本語 Issue は日本語タイトル） |
| 元タイトル保持 | 不要。GitHub の変更履歴（Activity）にタイトル変更が記録されるため、元タイトルを別途残す必要はない |

`ai-code-scan` ラベルあり（AI 起票）の場合はスキップ（タイトルは既に整っているため）。

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

**「対応案」セクションの省略ルール**: Issue 本文（またはステップ 4 で投稿した本文補完コメント）に既に「対応案」セクションが含まれる場合、レビュー結果コメントの「対応案」セクションは**省略**する。重複掲載しない。

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{レビュー結果本文}
EOF
)
```

## ステップ 5.5: タイプラベル判定・付与

Issue 本文・タイトル・補完コメント（ステップ 4）の内容から、適切な `type:*` ラベルを判定して付与する。

### 判定基準

| type ラベル | 変数 | 付与条件 |
|---|---|---|
| `type:bug` | `$GH_KIT_LABEL_TYPE_BUG` | 既存の動作が仕様または期待と異なる問題の修正 |
| `type:feat` | `$GH_KIT_LABEL_TYPE_FEAT` | 新機能追加・既存機能の有意な拡張 |
| `type:refactor` | `$GH_KIT_LABEL_TYPE_REFACTOR` | 外部動作を変えずにコードを整理・改善 |
| `type:docs` | `$GH_KIT_LABEL_TYPE_DOCS` | ドキュメント・コメントのみの変更 |
| `type:chore` | `$GH_KIT_LABEL_TYPE_CHORE` | ビルド設定・依存更新・CI/CD など |
| `type:test` | `$GH_KIT_LABEL_TYPE_TEST` | テストコードの追加・修正のみ |

いずれにも当てはまらない場合は `$GH_KIT_LABEL_TYPE_FEAT` を選ぶ（デフォルト）。

### 既付与時スキップ + 冪等付与

```bash
# 既に type:* ラベルが付与されている場合はスキップ
EXISTING_TYPE=$(gh issue view {N} --json labels --jq '.labels[].name' | grep '^type:' | head -1)
if [ -n "$EXISTING_TYPE" ]; then
  echo "type ラベル ${EXISTING_TYPE} 付与済みのためスキップ"
else
  # 選んだタイプラベルを変数に設定（例: TYPE_LABEL="$GH_KIT_LABEL_TYPE_BUG"）
  TYPE_LABEL="$GH_KIT_LABEL_TYPE_{判定したタイプ}"

  # ラベルが存在しなければ作成（冪等）
  gh label list --json name --jq '.[].name' | grep -q "^${TYPE_LABEL}$" || \
    gh label create "${TYPE_LABEL}" --color "$GH_KIT_LABEL_COLOR_TYPE" --description "Issue タイプ: ${TYPE_LABEL}"

  # Issue に付与
  gh issue edit {N} --add-label "${TYPE_LABEL}"
fi
```

`AIコードスキャン` ラベルがある（AI 起票）場合もこのステップを実行する（`code-scanner` が付与済みの場合は `--add-label` が冪等で安全）。

## ステップ 6: 優先度ラベルを付与（人間起票 Issue のみ）

ラベルに `AIコードスキャン` が含まれない（= 人間起票）かつ、Issue に優先度ラベルがまだ付いていない場合に限り、以下の基準で優先度を判定して付与する。

| 状況 | 優先度ラベル |
|---|---|
| セキュリティ脆弱性・クラッシュバグ・データ損失リスク・緊急対応が必要 | `優先度:急ぎ` |
| コード品質・ドキュメント・機能改善など時期を問わず対応できる | `優先度:いつでも` |

```bash
# Issue の既存ラベルを取得
CURRENT_LABELS=$(gh issue view {N} --json labels --jq '.labels | map(.name) | .[]')

# 優先度ラベルが未付与かつ AIコードスキャン 起票でない場合のみ付与
if ! echo "$CURRENT_LABELS" | grep -q "$GH_KIT_LABEL_AI_CODE_SCAN"; then
  if ! echo "$CURRENT_LABELS" | grep -qE "$GH_KIT_LABEL_PRIORITY_URGENT|$GH_KIT_LABEL_PRIORITY_LOW"; then
    # LLM で重大度を判定し、急ぎなら URGENT、それ以外は LOW を使う
    # 急ぎの場合:
    gh issue edit {N} --add-label "$GH_KIT_LABEL_PRIORITY_URGENT"
    # いつでもの場合:
    # gh issue edit {N} --add-label "$GH_KIT_LABEL_PRIORITY_LOW"
  fi
fi
```

## ステップ 7: レビュー完了後の assignee 追加（スキップ禁止）

レビュー完了後は、**必ず** GH ユーザーを Issue の assignee に追加する。
`needs_user_review` による条件分岐は行わない。常に実行する。

```bash
GH_LOGIN="$(gh api user --jq '.login')"
gh issue edit {N} --add-assignee "$GH_LOGIN"
```

**`確認:pr-planner` ラベルの自動付与は禁止。ユーザーが手動で付与する。**

ユーザーが Issue の内容を確認し、PR 作成を進める場合に、ユーザー自身が手動で `確認:pr-planner` ラベルを付与する。
AI が自動判定して `確認:pr-planner` を付与することは絶対に禁止（誤起動・意図しない PR 作成の防止のため）。

レビュー完了後は、以下のコメントでユーザーへの案内を投稿する:

```bash
gh issue comment {N} --body "$(cat <<'EOF'
## レビュー完了 — 次工程への進め方

Issue のレビューが完了しました。内容をご確認ください。

PR 作成を進める場合は、以下の手順で操作してください:

1. この Issue の内容を確認する
2. 問題なければ `確認:pr-planner` ラベルを手動で付与する
3. `pr-plan-auto` が自動的に Draft PR を作成します

**AI は `確認:pr-planner` ラベルを自動付与しません（誤起動防止のため）。**
EOF
)"
```

## ステップ 8: 戻り値

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

- メイン Issue 本文は書き換えない（タイトル更新は許可 — `gh issue edit --title` のみ使用可）
- 既存セクションが揃っているなら本文補完コメント（ステップ 4）はスキップ
- 推奨案は必ず明示（「後で決める」「TBD」禁止）
