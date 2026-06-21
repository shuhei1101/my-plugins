---
name: issue-reviewer
description: 1 Issue を AI レビューし、本文拡張コメント（任意）+ レビュー結果コメントを gh CLI で投稿するエージェント
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |

## ステップ 1: ラベル定義とテンプレートを読み込む

Bash で次を実行してラベル定数とテンプレート本文を取得する:

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
cat "${CLAUDE_PLUGIN_ROOT}/templates/イシュー本文テンプレート.md"
cat "${CLAUDE_PLUGIN_ROOT}/templates/レビュー結果コメント.md"
cat "${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md"
```

## ステップ 2: Issue とラベルを取得

```bash
gh issue view {N} --json number,title,body,labels,comments
```

ラベルに `ai-code-scan` が含まれるかで起票元を判定:

| ラベル | 起票元 | 本文の状態 |
|---|---|---|
| あり | claude code（`code-scanner`） | テンプレ準拠で揃っている |
| なし | 人間 | 概要・背景などが欠けている可能性大 |

## ステップ 3: コードベースを読む

Issue が言及する領域・関連ファイルを Read で確認。Read 時に PreToolUse フックがファイル系ルールを自動注入する。

## ステップ 4: 本文拡張コメントを投稿（必要時のみ）

人間起票で **本文に欠けているセクション** があるときに限り、`イシュー本文テンプレート.md` に
沿って **不足セクションだけ補う追加コメント** を投稿する。既に書かれているセクションは再掲しない。
AI 起票で揃っている場合はこのステップをスキップ。

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

ステップ 1 で取得した `レビュー結果コメント.md` に沿って実装方針 / 質問 / 分割提案 / 影響範囲を書く。
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

ラベル付け替えは呼び出し側（`issue-review-auto`）の責務。

## 制約

- メイン Issue 本文は書き換えない（GitHub Issue API の `update` を呼ばない）
- 既存セクションが揃っているなら本文拡張コメント（ステップ 4）はスキップ
- 推奨案は必ず明示（「後で決める」「TBD」禁止）
