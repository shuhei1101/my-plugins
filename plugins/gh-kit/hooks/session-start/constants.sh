#!/usr/bin/env bash
#
# 使い方
# source constants.shで定数をロードする

# 定数
export REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
export WIKI_BASE="https://raw.githubusercontent.com/wiki/${REPO_SLUG}"

# GitHub Issue / PR のラベル名
export GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW="確認:issue-reviewer"
export GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER="処理中:issue-reviewer"
export GH_KIT_LABEL_CONFIRM_PR_REVIEW="確認:pr-reviewer"
export GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT="確認:pr-implementer"
export GH_KIT_LABEL_AI_CODE_SCAN="AIコードスキャン"
export GH_KIT_LABEL_CONFIRM_PR_MERGER="確認:pr-merger"
export GH_KIT_LABEL_PROCESSING_PR_PLANNER="処理中:pr-planner"
export GH_KIT_LABEL_PROCESSING_PR_IMPLEMENTER="処理中:pr-implementer"
export GH_KIT_LABEL_PROCESSING_PR_REVIEWER="処理中:pr-reviewer"
export GH_KIT_LABEL_PROCESSING_PR_MERGER="処理中:pr-merger"
export GH_KIT_LABEL_PRIORITY_URGENT="優先度:急ぎ"
export GH_KIT_LABEL_PRIORITY_LOW="優先度:いつでも"
export GH_KIT_LABEL_TYPE_BUG="type:bug"
export GH_KIT_LABEL_TYPE_FEAT="type:feat"
export GH_KIT_LABEL_TYPE_REFACTOR="type:refactor"
export GH_KIT_LABEL_TYPE_DOCS="type:docs"
export GH_KIT_LABEL_TYPE_CHORE="type:chore"
export GH_KIT_LABEL_TYPE_TEST="type:test"
export GH_KIT_LABEL_CONFIRM_PR_PLANNER="確認:pr-planner"
export GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER="確認:pr-plan-reviewer"
export GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER="処理中:pr-plan-reviewer"
export GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER="確認:pr-implementer"
export GH_KIT_LABEL_PROCESSING_PREFIX="処理中:"
export GH_KIT_AUTO_TITLE_GENERATE="自動タイトル生成"

# GitHub Issue / PR のテンプレートファイル名

# イシューレビュー
export GH_KIT_TEMPLATE_ISSUE_DOCUMENT="イシュードキュメント.md"
export GH_KIT_TEMPLATE_REVIEW_RESULT="レビュー結果コメント.md"
export GH_KIT_TEMPLATE_USER_REVIEW_CRITERIA="ユーザー確認要否判定.md"
export GH_KIT_TEMPLATE_SCRIPT_TEST_REPORT="スクリプトテスト結果報告テンプレート.md"
export GH_KIT_TEMPLATE_OTHER_TEST_REPORT="その他動作確認報告テンプレート.md"
export GH_KIT_TEMPLATE_LIBRARY_SELECTION="テンプレート_ライブラリ選定論点.md"
export GH_KIT_TEMPLATE_DESIGN_REVIEW="テンプレート_設計レビュー論点.md"
