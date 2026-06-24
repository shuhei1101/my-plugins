#!/usr/bin/env bash
# gh-kit ラベル整備スクリプト
# GitHub 上のラベルを冪等に create / edit する。
# 旧ラベルを新日本語ラベルへ付け替えたうえで削除する。
#
# 使い方:
#   bash plugins/gh-kit/scripts/labels.sh
#
# 前提: gh CLI が認証済みであること（gh auth status）

set -euo pipefail

# ──────────────────────────────────────────
# ヘルパー: ラベルが存在すれば edit、なければ create
# upsert_label <name> <color> <description>
# ──────────────────────────────────────────
upsert_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label list --limit 200 --json name --jq '.[].name' | grep -qxF "$name"; then
    echo "[update] $name"
    gh label edit "$name" --color "$color" --description "$description"
  else
    echo "[create] $name"
    gh label create "$name" --color "$color" --description "$description"
  fi
}

# ──────────────────────────────────────────
# ヘルパー: 旧ラベルを新ラベルへ Issue/PR 付け替え後に削除
# migrate_label <old_name> <new_name>
# ──────────────────────────────────────────
migrate_label() {
  local old_name="$1"
  local new_name="$2"

  # 旧ラベルが存在しない場合はスキップ
  if ! gh label list --limit 200 --json name --jq '.[].name' | grep -qxF "$old_name"; then
    echo "[skip]   $old_name (存在しない)"
    return
  fi

  echo "[migrate] $old_name → $new_name"

  # open Issue の付け替え
  local issues
  issues=$(gh issue list --state open --label "$old_name" --json number --jq '.[].number' 2>/dev/null || true)
  for n in $issues; do
    echo "  Issue #$n: remove=$old_name add=$new_name"
    gh issue edit "$n" --remove-label "$old_name" --add-label "$new_name"
  done

  # open PR の付け替え
  local prs
  prs=$(gh pr list --state open --label "$old_name" --json number --jq '.[].number' 2>/dev/null || true)
  for n in $prs; do
    echo "  PR #$n: remove=$old_name add=$new_name"
    gh pr edit "$n" --remove-label "$old_name" --add-label "$new_name"
  done

  # 旧ラベル削除
  echo "[delete] $old_name"
  gh label delete "$old_name" --yes
}

echo "=== gh-kit ラベル整備 開始 ==="

# ──────────────────────────────────────────
# フロー制御: 処理中 系（エージェント名 -er 統一）
# ──────────────────────────────────────────
upsert_label "処理中"                   "FBCA04" "AI 処理中（排他制御）"
upsert_label "処理中:issue-reviewer"   "FBCA04" "issue-reviewer エージェントがレビュー中"
upsert_label "処理中:pr-planner"       "FBCA04" "Draft PR が存在し PR 対応中（pr-draft-create-auto が付与）"
upsert_label "処理中:pr-implementer"   "FBCA04" "実装エージェントが実装中（pr-implement-auto が付与）"
upsert_label "処理中:pr-reviewer"      "FBCA04" "レビューエージェントがレビュー中（pr-review-auto が付与）"

# ──────────────────────────────────────────
# フロー制御: 確認 系（エージェント名 -er 統一）
# ──────────────────────────────────────────
upsert_label "確認:issue-reviewer"     "0E8A16" "issue-reviewer エージェントによるレビュー必要（GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW）"
upsert_label "確認:pr-reviewer"        "0E8A16" "pr-reviewer エージェントによるレビュー必要（GH_KIT_LABEL_CONFIRM_PR_REVIEW）"
upsert_label "確認:pr-implementer"     "D93F0B" "レビュー結果、pr-implementer エージェントが修正必要（GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT）"
upsert_label "確認:pr-planner"         "0052CC" "AI レビュー完了・PR 作成 OK（pr-draft-create-auto の起動契機）"

# ──────────────────────────────────────────
# フロー制御: 確認 系（追加）
# ──────────────────────────────────────────
upsert_label "確認:pr-merger"          "0E8A16" "pr-reviewer がレビュー OK と判定し、pr-merger によるマージ待ち"

# ──────────────────────────────────────────
# 優先度
# ──────────────────────────────────────────
upsert_label "優先度:急ぎ"             "B60205" "セキュリティ脆弱性・クラッシュバグ・データ損失リスクなど早急に対応が必要なもの"
upsert_label "優先度:いつでも"         "0075CA" "コード品質・ドキュメント不足など時期を問わず対応可能なもの"

# ──────────────────────────────────────────
# タイプ
# ──────────────────────────────────────────
upsert_label "type:bug"               "D73A4A" "バグ"
upsert_label "type:feat"              "84b6eb" "新機能・整備"
upsert_label "type:refactor"          "0075CA" "リファクタリング"
upsert_label "type:docs"              "0075CA" "ドキュメント"
upsert_label "type:chore"             "0075CA" "ビルド設定・依存更新・CI/CD など"
upsert_label "type:test"              "0075CA" "テストコードの追加・修正のみ"

# ──────────────────────────────────────────
# フロー制御: 確認 系（pr-plan-reviewer）
# ──────────────────────────────────────────
upsert_label "確認:pr-plan-reviewer"   "0E8A16" "Draft PR プランの AI レビュー待ち（pr-plan-review-auto の起動契機）"
upsert_label "処理中:pr-plan-reviewer" "FBCA04" "pr-plan-reviewer エージェントがレビュー中"

# ──────────────────────────────────────────
# 出自タグ
# ──────────────────────────────────────────
upsert_label "AIコードスキャン"        "1D76DB" "claude code がスキャンして起票"

echo ""
echo "=== 旧ラベル移行 開始 ==="

# 処理中 系 旧→新
migrate_label "処理中:pr-draft"        "処理中:pr-planner"
migrate_label "処理中:pr-implement"    "処理中:pr-implementer"
migrate_label "処理中:pr-review"       "処理中:pr-reviewer"

# 確認 系 旧→新
migrate_label "確認:pr-plan"           "確認:pr-planner"

# ステータス 旧→新
migrate_label "approved-merge-ok"      "確認:pr-merger"
migrate_label "マージ可能"             "確認:pr-merger"
# 旧英語優先度ラベル
migrate_label "priority:high"          "優先度:急ぎ"
migrate_label "priority:medium"        "優先度:いつでも"
migrate_label "priority:low"           "優先度:いつでも"

# 旧英語フロー制御ラベル
migrate_label "needs-ai-review"        "確認:issue-reviewer"
migrate_label "needs-user-review"      "確認:pr-implementer"

# 旧 pr-review-auto が使っていた 確認:issue-reviewer（PR 上）→ 確認:pr-reviewer への移行
# 注: 確認:issue-reviewer は Issue でも使われるため Issue/PR を区別して手動実行すること
# migrate_label は Issue と PR を両方対象にするため、以下はコメントアウト
# migrate_label "確認:issue-reviewer"   "確認:pr-reviewer"  # PR のみ移行したい場合は手動で実施
migrate_label "processing:pr-draft"    "処理中:pr-planner"
migrate_label "processing:pr-implement" "処理中:pr-implementer"
migrate_label "processing:pr-review"   "処理中:pr-reviewer"

# 旧英語出自タグ
migrate_label "ai-code-scan"           "AIコードスキャン"

echo ""
echo "=== gh-kit ラベル整備 完了 ==="
