#!/usr/bin/env bash
# sync-codex-manifests.sh
# .claude-plugin/*.json から .codex-plugin/*.json を自動同期する冪等スクリプト
#
# 使い方:
#   bash plugins/gh-kit/scripts/sync-codex-manifests.sh [REPO_ROOT]
#
# 引数:
#   REPO_ROOT  リポジトリルートパス（省略時: スクリプトから 3 階層上を自動検出）
#
# 動作:
#   1. 各プラグインの .claude-plugin/plugin.json → .codex-plugin/plugin.json に同期
#   2. ルートの .claude-plugin/marketplace.json → .codex-plugin/marketplace.json に同期
#   冪等: 既に同一内容ならスキップ（差分がある場合のみ上書き）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${1:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"

echo "sync-codex-manifests: リポジトリルート = $REPO_ROOT"

# ステップ 1: 各プラグインの plugin.json を同期
sync_plugin_json() {
  local plugin_dir="$1"
  local plugin_name
  plugin_name="$(basename "$plugin_dir")"
  local src="$plugin_dir/.claude-plugin/plugin.json"
  local dst="$plugin_dir/.codex-plugin/plugin.json"

  if [ ! -f "$src" ]; then
    echo "  skip: $plugin_name (.claude-plugin/plugin.json が存在しない)"
    return
  fi

  mkdir -p "$(dirname "$dst")"

  if [ -f "$dst" ] && diff -q "$src" "$dst" > /dev/null 2>&1; then
    echo "  skip: $plugin_name/plugin.json (差分なし)"
  else
    cp "$src" "$dst"
    echo "  sync: $plugin_name/.codex-plugin/plugin.json を更新"
  fi
}

echo ""
echo "--- plugin.json 同期 ---"
for plugin_dir in "$REPO_ROOT"/plugins/*/; do
  sync_plugin_json "$plugin_dir"
done

# ステップ 2: ルートの marketplace.json を同期
echo ""
echo "--- marketplace.json 同期 ---"
ROOT_SRC="$REPO_ROOT/.claude-plugin/marketplace.json"
ROOT_DST="$REPO_ROOT/.codex-plugin/marketplace.json"

if [ ! -f "$ROOT_SRC" ]; then
  echo "  skip: .claude-plugin/marketplace.json が存在しない"
else
  mkdir -p "$(dirname "$ROOT_DST")"
  if [ -f "$ROOT_DST" ] && diff -q "$ROOT_SRC" "$ROOT_DST" > /dev/null 2>&1; then
    echo "  skip: .codex-plugin/marketplace.json (差分なし)"
  else
    cp "$ROOT_SRC" "$ROOT_DST"
    echo "  sync: .codex-plugin/marketplace.json を更新"
  fi
fi

echo ""
echo "sync-codex-manifests: 完了"
