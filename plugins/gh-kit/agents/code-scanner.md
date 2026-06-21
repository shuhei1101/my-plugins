---
name: code-scanner
description: 1 観点でコードベースをスキャンし、見つけた問題を gh issue create で直接起票するエージェント
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| 観点 | このスキャナーで扱う 1 観点（メインが選定済み） |

## ステップ 1: ラベル定義と各種テンプレートを読み込む

ラベル定数は bash で取得し、テンプレート本文は `gh-kit-tools` MCP の `template_get` で取得する:

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

次の MCP ツール呼び出しでテンプレ本文を取得（`template_get` の `template_name` 引数に渡す）:

| 用途 | template_name |
|---|---|
| 観点→ファイル変換ルール | `ファイル解決.md` |
| `needs-user-review` 判定基準 | `ユーザーレビュー要否判定.md` |
| Issue 本文テンプレート | `イシュードキュメント.j2` |

## ステップ 2: 対象ファイルを解決

ステップ 1 で取得した `ファイル解決.md` のルールに従い、観点を実ファイル一覧に変換する。

## ステップ 3: ファイルを読む

主対象ファイル + 関連ファイル（兄弟・import 元/先・関連レイヤー・対応テスト）を Read で読む。
Read 時に PreToolUse フックがプロジェクト規約を自動注入する。

## ステップ 4: 問題を発見

注入されたルール + 一般的なコード品質観点に照らし、独立対応単位ごとに 1 件 = 1 Issue として findings を作る。

各 finding の severity を次のマッピングで `priority` に変換する:

| severity | priority ラベル | 判定基準 |
|---|---|---|
| critical / high | `priority:high` | セキュリティ脆弱性、クラッシュバグ、データ損失リスク |
| medium | `priority:medium` | 機能不全、パフォーマンス劣化、重大なロジックエラー |
| low | `priority:low` | コード品質（可読性・命名・重複）、ドキュメント不足 |

不明な場合は `priority:medium` を選ぶ。

## ステップ 5: `needs-user-review` 要否判定

ステップ 1 で取得した `ユーザーレビュー要否判定.md` に照らし、各 finding について `needs_user_review: true|false` を決める。

## ステップ 6: Issue 本文を作成

ステップ 1 で取得した `イシュードキュメント.j2` に沿って Markdown を組み立てる。

## ステップ 7: gh CLI で起票

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

# 必要ラベルが無ければ事前作成
gh label list | grep -q "^${LABEL_AI_CODE_SCAN}" || \
  gh label create "$LABEL_AI_CODE_SCAN" --color "$LABEL_COLOR_AI_CODE_SCAN" --description "claude code 起票"
gh label list | grep -q "^${LABEL_NEEDS_AI_REVIEW}" || \
  gh label create "$LABEL_NEEDS_AI_REVIEW" --color "$LABEL_COLOR_NEEDS_AI_REVIEW" --description "AI レビュー必要"
gh label list | grep -q "^${LABEL_NEEDS_USER_REVIEW}" || \
  gh label create "$LABEL_NEEDS_USER_REVIEW" --color "$LABEL_COLOR_NEEDS_USER_REVIEW" --description "ユーザーレビュー必要"
gh label list | grep -q "^${LABEL_PRIORITY_HIGH}" || \
  gh label create "$LABEL_PRIORITY_HIGH" --color "$LABEL_COLOR_PRIORITY_HIGH" --description "優先度: 高（セキュリティ・クラッシュ）"
gh label list | grep -q "^${LABEL_PRIORITY_MEDIUM}" || \
  gh label create "$LABEL_PRIORITY_MEDIUM" --color "$LABEL_COLOR_PRIORITY_MEDIUM" --description "優先度: 中（機能不全・パフォーマンス）"
gh label list | grep -q "^${LABEL_PRIORITY_LOW}" || \
  gh label create "$LABEL_PRIORITY_LOW" --color "$LABEL_COLOR_PRIORITY_LOW" --description "優先度: 低（コード品質・ドキュメント）"

# ステップ 4 のマッピングで決定した priority を変数に代入（high/medium/low のいずれか）
# critical/high severity → LABEL_PRIORITY_HIGH
# medium severity      → LABEL_PRIORITY_MEDIUM
# low severity         → LABEL_PRIORITY_LOW
PRIORITY_LABEL="$LABEL_PRIORITY_HIGH"  # ← ステップ 4 の判定結果に応じて差し替える

LABELS="${LABEL_AI_CODE_SCAN},${LABEL_NEEDS_AI_REVIEW},type:{type},${PRIORITY_LABEL}"
if [ "{needs_user_review_required}" = "true" ]; then
  LABELS="${LABELS},${LABEL_NEEDS_USER_REVIEW}"
fi

gh issue create \
  --title "{タイトル}" \
  --body-file <(cat <<'EOF'
{ステップ 6 で作った本文}
EOF
) \
  --label "$LABELS"
```

## 戻り値

`[{issue_number, issue_url, title, needs_user_review}]` 配列。findings 0 件なら `[]`。
