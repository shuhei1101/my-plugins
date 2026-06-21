---
name: gh-kit:issue-create
description: GitHub Issue を 1 件起票する。gh-kit:needs-ai-review ラベルを強制付与し、AI レビューフローに確実に乗せる。code-scanner や手動呼び出しの両方から使える。
---

# issue-create

このスキルは Issue 起票の責務を一か所に集約するために作られた。

**なぜ `needs-ai-review` を強制付与するのか？**
Issue 起票後に AI レビューフロー（`/gh-kit:issue-review-auto`）が確実に対象を拾うには、`needs-ai-review` ラベルが必須。呼び出し側（code-scanner 等）がラベルを付け忘れると AI レビューが走らなくなるため、このスキル内部で構造的に保証する。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| `title` | 必須 | Issue タイトル |
| `body` | 必須 | Issue 本文（`イシュードキュメント.j2` テンプレを呼び出し側が展開済み） |
| `type` | 必須 | Issue タイプラベル（例: `bug`, `enhancement`, `refactor`） |
| `priority` | 必須 | 優先度ラベル（例: `priority-high`, `priority-medium`, `priority-low`） |
| `needs_user_review` | 任意 | `true` の場合 `gh-kit:needs-user-review` ラベルを追加（既定: `false`） |
| `extra_labels` | 任意 | 追加ラベルのカンマ区切り文字列（既定: なし） |

## 動作フロー

1. `labels.sh` を読み込んでラベル定数を確保する
2. 必要ラベルを `gh label create` で冪等に用意する（既存ならスキップ）
3. `needs-ai-review` を含むラベル文字列を組み立てる
4. `gh issue create` で起票する
5. `issue_number` / `issue_url` を戻り値として返す

## 呼び出し元

- `code-scanner` エージェント（ステップ 7 から移管）
- ユーザーが `/gh-kit:issue-create` を直接呼び出す場合

## ステップ 1: ラベルを冪等に用意する

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

gh label list | grep -q "^${LABEL_NEEDS_AI_REVIEW}" || \
  gh label create "$LABEL_NEEDS_AI_REVIEW" --color "$LABEL_COLOR_NEEDS_AI_REVIEW" --description "AI レビュー必要"

gh label list | grep -q "^${LABEL_NEEDS_USER_REVIEW}" || \
  gh label create "$LABEL_NEEDS_USER_REVIEW" --color "$LABEL_COLOR_NEEDS_USER_REVIEW" --description "ユーザーレビュー必要"
```

## ステップ 2: ラベル文字列を組み立てる

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

# gh-kit:needs-ai-review は呼び出し側が指定しなくても必ず付与する（構造的保証）
LABELS="${LABEL_AI_CODE_SCAN},${LABEL_NEEDS_AI_REVIEW},{type},{priority}"

if [ "{needs_user_review}" = "true" ]; then
  LABELS="${LABELS},${LABEL_NEEDS_USER_REVIEW}"
fi

if [ -n "{extra_labels}" ]; then
  LABELS="${LABELS},{extra_labels}"
fi
```

## ステップ 3: gh issue create で起票する

```bash
gh issue create \
  --title "{title}" \
  --body-file <(cat <<'EOF'
{body}
EOF
) \
  --label "$LABELS"
```

起票に成功したら `gh issue view` で `number` と `url` を取得する。

## 戻り値

```json
{
  "issue_number": 42,
  "issue_url": "https://github.com/owner/repo/issues/42",
  "title": "Issue タイトル",
  "needs_user_review": false
}
```
