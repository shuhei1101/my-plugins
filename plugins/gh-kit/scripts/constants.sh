#!/usr/bin/env bash
#
# 使い方
# source constants.shで定数をロードする

# 定数
export REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
export WIKI_BASE="https://raw.githubusercontent.com/${REPO_SLUG}/master/docs/wiki"

# GitHub Issue / PR のラベル名（CLAUDE.md のモニター一覧と 1:1 対応）

# 共通
export GH_KIT_LABEL_PHASE_END="フェーズ終了"
export GH_KIT_LABEL_PROCESSING_PREFIX="処理中:"

# 1. issue-triage
export GH_KIT_LABEL_CONFIRM_ISSUE_TRIAGE="確認:issue-triage"
export GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE="処理中:issue-triage"

# 2. issue-spec
export GH_KIT_LABEL_CONFIRM_ISSUE_SPEC="確認:issue-spec"
export GH_KIT_LABEL_PROCESSING_ISSUE_SPEC="処理中:issue-spec"

# 3. pr-ui
export GH_KIT_LABEL_CONFIRM_PR_UI="確認:pr-ui"
export GH_KIT_LABEL_PROCESSING_PR_UI="処理中:pr-ui"

# 4. pr-arch
export GH_KIT_LABEL_CONFIRM_PR_ARCH="確認:pr-arch"
export GH_KIT_LABEL_PROCESSING_PR_ARCH="処理中:pr-arch"

# 5. pr-test
export GH_KIT_LABEL_CONFIRM_PR_TEST="確認:pr-test"
export GH_KIT_LABEL_PROCESSING_PR_TEST="処理中:pr-test"

# 6. pr-impl
export GH_KIT_LABEL_CONFIRM_PR_IMPL="確認:pr-impl"
export GH_KIT_LABEL_PROCESSING_PR_IMPL="処理中:pr-impl"

# 7. pr-impl-review
export GH_KIT_LABEL_CONFIRM_PR_IMPL_REVIEW="確認:pr-impl-review"
export GH_KIT_LABEL_PROCESSING_PR_IMPL_REVIEW="処理中:pr-impl-review"

# 8. pr-doc-plan
export GH_KIT_LABEL_CONFIRM_PR_DOC_PLAN="確認:pr-doc-plan"
export GH_KIT_LABEL_PROCESSING_PR_DOC_PLAN="処理中:pr-doc-plan"

# 9. pr-doc
export GH_KIT_LABEL_CONFIRM_PR_DOC="確認:pr-doc"
export GH_KIT_LABEL_PROCESSING_PR_DOC="処理中:pr-doc"

# 10. pr-doc-review
export GH_KIT_LABEL_CONFIRM_PR_DOC_REVIEW="確認:pr-doc-review"
export GH_KIT_LABEL_PROCESSING_PR_DOC_REVIEW="処理中:pr-doc-review"

# 11. pr-merge
export GH_KIT_LABEL_CONFIRM_PR_MERGE="確認:pr-merge"
export GH_KIT_LABEL_PROCESSING_PR_MERGE="処理中:pr-merge"

# 12. reset
export GH_KIT_LABEL_CONFIRM_RESET="確認:reset"
export GH_KIT_LABEL_PROCESSING_RESET="処理中:reset"

# 優先度（ユーザーが付与）
export GH_KIT_LABEL_PRIORITY_URGENT="優先度:急ぎ"
export GH_KIT_LABEL_PRIORITY_LOW="優先度:いつでも"

# タイプ（issue-triage が付与）
export GH_KIT_LABEL_TYPE_BUG="type:bug"
export GH_KIT_LABEL_TYPE_FEAT="type:feat"
export GH_KIT_LABEL_TYPE_REFACTOR="type:refactor"
export GH_KIT_LABEL_TYPE_DOCS="type:docs"
export GH_KIT_LABEL_TYPE_CHORE="type:chore"
export GH_KIT_LABEL_TYPE_TEST="type:test"

# GitHub Issue / PR のテンプレートファイル名

# イシューレビュー
export GH_KIT_TEMPLATE_ISSUE_DOCUMENT="イシュードキュメント.md"
export GH_KIT_TEMPLATE_REVIEW_RESULT="レビュー結果コメント.md"
export GH_KIT_TEMPLATE_USER_REVIEW_CRITERIA="ユーザー確認要否判定.md"
export GH_KIT_TEMPLATE_SCRIPT_TEST_REPORT="スクリプトテスト結果報告テンプレート.md"
export GH_KIT_TEMPLATE_OTHER_TEST_REPORT="その他動作確認報告テンプレート.md"
export GH_KIT_TEMPLATE_LIBRARY_SELECTION="テンプレート_ライブラリ選定論点.md"
export GH_KIT_TEMPLATE_DESIGN_REVIEW="テンプレート_設計レビュー論点.md"
