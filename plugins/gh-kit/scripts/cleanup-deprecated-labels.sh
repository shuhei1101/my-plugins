#!/usr/bin/env bash
# gh-kit 廃止ラベル削除スクリプト（ワンショット・冪等）
#
# Issue #239 で廃止確認されたラベルを GitHub リポジトリから削除し、
# Open PR / Issue に付いている廃止ラベルを除去する。
#
# 使い方:
#   bash plugins/gh-kit/scripts/cleanup-deprecated-labels.sh
#
# 前提: gh CLI が認証済みであること（gh auth status）
# 冪等: 既に削除済みのラベルは警告なくスキップする。

set -euo pipefail

# ──────────────────────────────────────────
# 廃止ラベル一覧
# Issue #239 で廃止が確認されたラベル
# ──────────────────────────────────────────
DEPRECATED_LABELS=(
  "wip"
  "ユーザーレビュード"
  "ユーザーレビューオート"
)

echo "=== gh-kit 廃止ラベル削除 開始 ==="

for LABEL in "${DEPRECATED_LABELS[@]}"; do
  echo ""
  echo "--- ラベル: $LABEL ---"

  # ラベルが存在しない場合はスキップ
  if ! gh label list --limit 200 --json name --jq '.[].name' | grep -qxF "$LABEL"; then
    echo "[skip] $LABEL (リポジトリに存在しない)"
    continue
  fi

  # Open PR に付いている廃止ラベルを除去
  echo "[PR ラベル除去] $LABEL"
  PR_NUMBERS=$(gh pr list --state open --label "$LABEL" --json number --jq '.[].number' 2>/dev/null || true)
  if [ -n "$PR_NUMBERS" ]; then
    while IFS= read -r N; do
      echo "  PR #$N: remove=$LABEL"
      gh pr edit "$N" --remove-label "$LABEL" 2>/dev/null || true
    done <<< "$PR_NUMBERS"
  else
    echo "  (対象 PR なし)"
  fi

  # Open Issue に付いている廃止ラベルを除去
  echo "[Issue ラベル除去] $LABEL"
  ISSUE_NUMBERS=$(gh issue list --state open --label "$LABEL" --json number --jq '.[].number' 2>/dev/null || true)
  if [ -n "$ISSUE_NUMBERS" ]; then
    while IFS= read -r N; do
      echo "  Issue #$N: remove=$LABEL"
      gh issue edit "$N" --remove-label "$LABEL" 2>/dev/null || true
    done <<< "$ISSUE_NUMBERS"
  else
    echo "  (対象 Issue なし)"
  fi

  # ラベル自体を削除
  echo "[delete] $LABEL"
  gh label delete "$LABEL" --yes 2>/dev/null || true
done

echo ""
echo "=== gh-kit 廃止ラベル削除 完了 ==="
