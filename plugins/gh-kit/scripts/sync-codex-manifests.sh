#!/usr/bin/env bash
# sync-codex-manifests.sh
# .claude-plugin/*.json から .codex-plugin/*.json へのシンボリックリンクを初期化するスクリプト
#
# 使い方:
#   bash plugins/gh-kit/scripts/sync-codex-manifests.sh [REPO_ROOT]
#
# 引数:
#   REPO_ROOT  リポジトリルートパス（省略時: スクリプトから 3 階層上を自動検出）
#
# 動作:
#   1. 各プラグインの .codex-plugin/plugin.json を正ファイルとして .claude-plugin/plugin.json を symlink 化
#   2. ルートの .codex-plugin/marketplace.json を正ファイルとして .claude-plugin/marketplace.json を symlink 化
#   冪等: 既に symlink なら内容を確認してスキップ
#
# 前提条件:
#   WSL2 環境（core.symlinks=true が必要）
#   Windows ネイティブ環境（WSL 外）では動作しない
#
# このスクリプトの役割:
#   初回 symlink 化または symlink が壊れた場合の再作成に使用する。
#   通常の更新作業では .codex-plugin/*.json を直接編集すれば .claude-plugin/ 側に自動反映される。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${1:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"

echo "sync-codex-manifests: リポジトリルート = $REPO_ROOT"
echo "(symlink 初期化モード: .codex-plugin/ を正として .claude-plugin/ を symlink 化)"

# ステップ 1: 各プラグインの plugin.json を symlink 化
symlink_plugin_json() {
  local plugin_dir="$1"
  local plugin_name
  plugin_name="$(basename "$plugin_dir")"
  local src="$plugin_dir/.codex-plugin/plugin.json"
  local dst="$plugin_dir/.claude-plugin/plugin.json"

  if [ ! -f "$src" ]; then
    echo "  skip: $plugin_name (.codex-plugin/plugin.json が存在しない)"
    return
  fi

  mkdir -p "$(dirname "$dst")"

  if [ -L "$dst" ]; then
    echo "  skip: $plugin_name/.claude-plugin/plugin.json (既に symlink)"
  else
    rm -f "$dst"
    ln -s "../.codex-plugin/plugin.json" "$dst"
    echo "  symlinked: $plugin_name/.claude-plugin/plugin.json -> ../.codex-plugin/plugin.json"
  fi
}

echo ""
echo "--- plugin.json symlink 化 ---"
for plugin_dir in "$REPO_ROOT"/plugins/*/; do
  symlink_plugin_json "$plugin_dir"
done

# ステップ 2: ルートの marketplace.json を symlink 化
echo ""
echo "--- marketplace.json symlink 化 ---"
ROOT_SRC="$REPO_ROOT/.codex-plugin/marketplace.json"
ROOT_DST="$REPO_ROOT/.claude-plugin/marketplace.json"

if [ ! -f "$ROOT_SRC" ]; then
  echo "  skip: .codex-plugin/marketplace.json が存在しない"
else
  mkdir -p "$(dirname "$ROOT_DST")"
  if [ -L "$ROOT_DST" ]; then
    echo "  skip: .claude-plugin/marketplace.json (既に symlink)"
  else
    rm -f "$ROOT_DST"
    ln -s "../.codex-plugin/marketplace.json" "$ROOT_DST"
    echo "  symlinked: .claude-plugin/marketplace.json -> ../.codex-plugin/marketplace.json"
  fi
fi

echo ""
echo "sync-codex-manifests: 完了"
