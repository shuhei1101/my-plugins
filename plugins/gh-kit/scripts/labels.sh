#!/usr/bin/env bash
# gh-kit ラベル整備スクリプト
# GitHub 上のラベルを冪等に create / edit する。
# 旧ラベル（priority:high / priority:medium / priority:low / needs-ai-review / needs-fix /
# needs-user-review / ai-code-scan / processing:pr-draft / processing:pr-implement /
# processing:pr-review）は既存 Issue/PR を尊重するため削除・リネームしない。
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

echo "=== gh-kit ラベル整備 開始 ==="

# ──────────────────────────────────────────
# フロー制御: 処理中 系
# ──────────────────────────────────────────
upsert_label "処理中"              "FBCA04" "AI 処理中（排他制御）"
upsert_label "処理中:pr-draft"    "FBCA04" "Draft PR が存在し PR 対応中（pr-draft-create-auto が付与）"
upsert_label "処理中:pr-implement" "FBCA04" "実装エージェントが実装中（pr-implement-auto が付与）"
upsert_label "処理中:pr-review"   "FBCA04" "レビューエージェントがレビュー中（pr-review-auto が付与）"

# ──────────────────────────────────────────
# フロー制御: 確認 系
# ──────────────────────────────────────────
upsert_label "確認:issue-reviewer"  "0E8A16" "issue-reviewer スキルによるレビュー必要"
upsert_label "確認:pr-implementer" "D93F0B" "レビュー結果、pr-implementer スキルが修正必要"
upsert_label "確認:pr-plan"        "0052CC" "AI レビュー完了・PR 作成 OK（pr-draft-create-auto の起動契機）"

# ──────────────────────────────────────────
# 優先度
# ──────────────────────────────────────────
upsert_label "優先度:急ぎ"     "B60205" "セキュリティ脆弱性・クラッシュバグ・データ損失リスクなど早急に対応が必要なもの"
upsert_label "優先度:いつでも" "0075CA" "コード品質・ドキュメント不足など時期を問わず対応可能なもの"

# ──────────────────────────────────────────
# タイプ
# ──────────────────────────────────────────
upsert_label "type:bug"      "D73A4A" "バグ"
upsert_label "type:feat"     "84b6eb" "新機能・整備"
upsert_label "type:refactor" "0075CA" "リファクタリング"
upsert_label "type:docs"     "0075CA" "ドキュメント"
upsert_label "type:chore"    "0075CA" "ビルド設定・依存更新・CI/CD など"
upsert_label "type:test"     "0075CA" "テストコードの追加・修正のみ"

# ──────────────────────────────────────────
# PR 専用
# ──────────────────────────────────────────
upsert_label "wip"              "C2E0C6" "Draft 雛形 PR"
upsert_label "approved-merge-ok" "0E8A16" "AI レビュー OK でマージ可（pr-review が付与、pr-merger がマージ後に除去）"

# ──────────────────────────────────────────
# 出自タグ
# ──────────────────────────────────────────
upsert_label "AIコードスキャン" "1D76DB" "claude code がスキャンして起票"

echo ""
echo "=== gh-kit ラベル整備 完了 ==="
echo "注意: 旧ラベル (priority:high / priority:medium / priority:low / needs-ai-review /"
echo "      needs-fix / needs-user-review / ai-code-scan / processing:pr-draft /"
echo "      processing:pr-implement / processing:pr-review) は既存 Issue/PR 尊重のため保持"
