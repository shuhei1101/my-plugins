#!/usr/bin/env bash
# plugins/gh-kit/scripts/migrate-labels.sh
# 旧ラベル名を最新名にリネームする冪等スクリプト。
# リネーム済みの場合はスキップするため何度実行しても安全。
#
# 使い方:
#   ./migrate-labels.sh <owner/repo>
#   GH_KIT_REPO=owner/repo ./migrate-labels.sh
#
# 引数:
#   $1  対象リポジトリ (例: myorg/myrepo)。省略時は環境変数 GH_KIT_REPO を使用。

set -euo pipefail

REPO="${1:-${GH_KIT_REPO:-}}"
[[ -z "$REPO" ]] && { echo "Usage: $0 <owner/repo> or set GH_KIT_REPO"; exit 1; }

migrate_label() {
  local old=$1 new=$2
  # --search は部分一致のリスクあり。--limit 1000 + jq で完全一致確認する
  if gh label list --repo "$REPO" --limit 1000 --json name \
      --jq --arg n "$old" '.[] | select(.name == $n) | .name' | grep -qx "$old"; then
    gh label edit "$old" --repo "$REPO" --name "$new" && echo "renamed: $old -> $new"
  else
    echo "skip: $old not found (already renamed or does not exist)"
  fi
}

echo "=== gh-kit ラベル移行スクリプト ==="
echo "対象リポジトリ: $REPO"
echo ""

# 確認:pr-plan（skill名）→ 確認:pr-planner（agent名規約）
migrate_label "確認:pr-plan" "確認:pr-planner"
# 処理中:pr-planner は既に正しい命名のためリネーム不要

echo ""
echo "=== 完了 ==="
