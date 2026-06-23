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
  if gh label list --repo "$REPO" --search "$old" --json name --jq '.[].name' | grep -qx "$old"; then
    gh label edit "$old" --repo "$REPO" --name "$new" && echo "renamed: $old -> $new"
  else
    echo "skip: $old not found (already renamed or does not exist)"
  fi
}

echo "=== gh-kit ラベル移行スクリプト ==="
echo "対象リポジトリ: $REPO"
echo ""

migrate_label "確認:pr-planner" "確認:pr-plan"
migrate_label "処理中:pr-planner" "処理中:pr-draft"

echo ""
echo "=== 完了 ==="
