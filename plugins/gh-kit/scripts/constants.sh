#!/usr/bin/env bash
# gh-kit 定数定義。Session Start フックで自動実行され、$CLAUDE_ENV_FILE に書き込まれて
# Claude Code セッション全体に環境変数として展開される。
# 定数名にはプラグイン名プレフィックス GH_KIT_ を付与する。
#
# 注意: サブシェルで export しても親プロセス（Claude Code）には伝わらない。
#       $CLAUDE_ENV_FILE への追記により Claude Code が環境変数として読み込む。

echo "export GH_KIT_LABEL_PROCESSING=処理中" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_NEEDS_AI_REVIEW=確認:issue-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_NEEDS_FIX=確認:pr-implementer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_AI_CODE_SCAN=AIコードスキャン" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_WIP=wip" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_COLOR_PROCESSING=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_NEEDS_AI_REVIEW=0E8A16" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_NEEDS_FIX=D93F0B" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_AI_CODE_SCAN=1D76DB" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_WIP=C2E0C6" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_PROCESSING_PR_DRAFT=処理中:pr-draft" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_IMPLEMENT=処理中:pr-implement" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_REVIEW=処理中:pr-review" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_DRAFT=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_IMPLEMENT=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_REVIEW=FBCA04" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_PRIORITY_URGENT=優先度:急ぎ" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PRIORITY_LOW=優先度:いつでも" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PRIORITY_URGENT=B60205" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PRIORITY_LOW=0075CA" >> "$CLAUDE_ENV_FILE"
