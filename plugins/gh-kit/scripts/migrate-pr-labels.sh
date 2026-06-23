#!/usr/bin/env bash
# migrate-pr-labels.sh — PR 限定ラベル移行ワンショットスクリプト
#
# 目的:
#   既存の Open PR に付いている「確認:issue-reviewer」を「確認:pr-reviewer」に付け替える。
#   labels.sh の migrate_label は Issue / PR を両方対象にするため、Issue 側の
#   「確認:issue-reviewer」まで変更してしまう。このスクリプトは PR 限定で移行する。
#
# 使い方（初回適用時に一度だけ実行）:
#   bash plugins/gh-kit/scripts/migrate-pr-labels.sh
#
# 前提:
#   - gh CLI が認証済みであること（gh auth status）
#   - 対象リポジトリで gh コマンドが動作すること
#
# 注意:
#   このスクリプトは冪等（二度実行しても問題ない）。
#   「確認:issue-reviewer」が付いていない PR はスキップされる。

set -euo pipefail

OLD_LABEL="確認:issue-reviewer"
NEW_LABEL="確認:pr-reviewer"

echo "=== PR ラベル移行: ${OLD_LABEL} → ${NEW_LABEL} ==="
echo "対象: Open PR のみ（Issue には手をつけない）"
echo ""

# Open PR で OLD_LABEL が付いているものを列挙
prs=$(gh pr list --state open --label "$OLD_LABEL" --json number --jq '.[].number' 2>/dev/null || true)

if [ -z "$prs" ]; then
  echo "[skip] 対象 PR なし（「${OLD_LABEL}」が付いた Open PR は存在しない）"
  echo ""
  echo "=== 移行完了（対象なし） ==="
  exit 0
fi

for n in $prs; do
  echo "PR #${n}: remove=${OLD_LABEL} → add=${NEW_LABEL}"
  gh pr edit "$n" --remove-label "$OLD_LABEL" --add-label "$NEW_LABEL"
done

echo ""
echo "=== PR ラベル移行完了 ==="
