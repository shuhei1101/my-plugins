#!/usr/bin/env bash
# gh-kit 定数定義。Session Start フックで自動実行され、$CLAUDE_ENV_FILE に書き込まれて
# Claude Code セッション全体に環境変数として展開される。
# 定数名にはプラグイン名プレフィックス GH_KIT_ を付与する。
#
# 注意: サブシェルで export しても親プロセス（Claude Code）には伝わらない。
#       $CLAUDE_ENV_FILE への追記により Claude Code が環境変数として読み込む。

echo "export GH_KIT_LABEL_NEEDS_AI_REVIEW=確認:issue-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_NEEDS_FIX=確認:pr-implementer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_AI_CODE_SCAN=AIコードスキャン" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_WIP=wip" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_CONFIRM_PR_MERGER=確認:pr-merger" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_USER_REVIEWED=user-reviewed" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_COLOR_NEEDS_AI_REVIEW=0E8A16" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_NEEDS_FIX=D93F0B" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_AI_CODE_SCAN=1D76DB" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_WIP=C2E0C6" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_CONFIRM_PR_MERGER=0E8A16" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_USER_REVIEWED=5319E7" >> "$CLAUDE_ENV_FILE"

# 各エージェント固有の処理中ラベル（排他マーカー）
echo "export GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER=処理中:issue-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_PLANNER=処理中:pr-planner" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_IMPLEMENTER=処理中:pr-implementer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_REVIEWER=処理中:pr-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_MERGER=処理中:pr-merger" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_ISSUE_REVIEWER=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_PLANNER=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_IMPLEMENTER=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_REVIEWER=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_MERGER=FBCA04" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_PRIORITY_URGENT=優先度:急ぎ" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PRIORITY_LOW=優先度:いつでも" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PRIORITY_URGENT=B60205" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PRIORITY_LOW=0075CA" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_TYPE_BUG=type:bug" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_TYPE_FEAT=type:feat" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_TYPE_REFACTOR=type:refactor" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_TYPE_DOCS=type:docs" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_TYPE_CHORE=type:chore" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_TYPE_TEST=type:test" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_TYPE=0075CA" >> "$CLAUDE_ENV_FILE"

echo "export GH_KIT_LABEL_CONFIRM_PR_PLANNER=確認:pr-planner" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_CONFIRM_PR_PLANNER=0052CC" >> "$CLAUDE_ENV_FILE"

# pr-plan-reviewer エージェント用ラベル
echo "export GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER=確認:pr-plan-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER=処理中:pr-plan-reviewer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER=確認:pr-implementer" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_CONFIRM_PR_PLAN_REVIEWER=0E8A16" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_PROCESSING_PR_PLAN_REVIEWER=FBCA04" >> "$CLAUDE_ENV_FILE"
echo "export GH_KIT_LABEL_COLOR_CONFIRM_PR_IMPLEMENTER=D93F0B" >> "$CLAUDE_ENV_FILE"
