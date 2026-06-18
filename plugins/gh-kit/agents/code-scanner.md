---
name: code-scanner
description: 1 観点でコードベースをスキャンし、見つけた問題を gh issue create で直接起票するエージェント
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| 観点 | このスキャナーで扱う 1 観点（メインが選定済み） |

追加で観点を独自に広げない。

## ラベル定義の読み込み

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

## ステップ 1: 対象ファイルを解決

ファイル解決ルールを直展開する。

!`cat "${GH_KIT_FILE_RESOLUTION_PATH:-${CLAUDE_PLUGIN_ROOT}/templates/ファイル解決.md}"`

## ステップ 2: ファイルを読む

主対象ファイル + 関連ファイル（兄弟・import 元/先・関連レイヤー・対応テスト）を Read で読む。
Read 時に PreToolUse フックがプロジェクト規約を自動注入する。

## ステップ 3: 問題を発見

注入されたルールおよび一般的なコード品質観点に照らして、独立対応単位ごとに 1 件ずつ findings を作る（1 事項 = 1 Issue）。

## ステップ 4: 各 finding について `needs-user-review` を付けるか判定

以下の基準に従う:

!`cat "${GH_KIT_USER_REVIEW_CRITERIA_PATH:-${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md}"`

## ステップ 5: Issue 本文を作成

本文テンプレートを直展開する。

!`cat "${GH_KIT_ISSUE_BODY_TEMPLATE_PATH:-${CLAUDE_PLUGIN_ROOT}/templates/イシュー本文テンプレート.md}"`

## ステップ 6: gh CLI で起票

各 finding について以下を実行する:

```bash
# 必要ラベルが無ければ事前に作成
gh label list | grep -q "^${LABEL_AI_CODE_SCAN}" || \
  gh label create "$LABEL_AI_CODE_SCAN" --color "$LABEL_COLOR_AI_CODE_SCAN" --description "claude code がスキャンして起票"
gh label list | grep -q "^${LABEL_NEEDS_AI_REVIEW}" || \
  gh label create "$LABEL_NEEDS_AI_REVIEW" --color "$LABEL_COLOR_NEEDS_AI_REVIEW" --description "AI レビュー必要"

# Issue 起票（needs-ai-review は必須付与、needs-user-review は判定結果で付与）
LABELS="${LABEL_AI_CODE_SCAN},${LABEL_NEEDS_AI_REVIEW},type:{type},priority:{priority}"
if [ "{needs_user_review_required}" = "true" ]; then
  LABELS="${LABELS},${LABEL_NEEDS_USER_REVIEW}"
fi

gh issue create \
  --title "{タイトル}" \
  --body-file <(cat <<'EOF'
{ステップ 5 で作った本文}
EOF
) \
  --label "$LABELS"
```

## 戻り値

起票した Issue の `[{issue_number, issue_url, title, needs_user_review}]` 配列を返す。findings 0 件なら `[]`。

## 制約

- `needs-ai-review` は **必ず** 付ける
- `needs-user-review` は判定基準に厳格に従う（疑わしきは付ける）
- ラベル名はハードコードせず `labels.sh` の変数を使う
