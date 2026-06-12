"""my-plugins ツール群を MCP サーバーとして公開する。

# 実行方法（Claude Code の mcpServers から自動起動）
uv run --with mcp python tools/mcp_server.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"

mcp = FastMCP("my-plugins-tools")


@mcp.tool()
def push() -> str:
    """master を push して marketplace upgrade と reload-plugins を実行する。"""
    result = subprocess.run(
        [sys.executable, str(TOOLS / "post_merge_upgrade.py")],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return result.stdout + result.stderr


@mcp.tool()
def bump_version(bump_kind: str, plugin_name: str = "") -> str:
    """プラグインのバージョンをバンプする。

    bump_kind: "minor" または "major"
    plugin_name: 省略時は master との差分から自動検出
    """
    args = [sys.executable, str(TOOLS / "bump-version.py")]
    if plugin_name:
        args += [plugin_name, bump_kind]
    else:
        args += [bump_kind]
    result = subprocess.run(args, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.stdout + result.stderr


@mcp.tool()
def marketplace(command: str, branch: str = "", plugin: str = "", local: bool = False) -> str:
    """マーケットプレイスを管理する。

    command: list / status / add / install / sync / install-diff / update / remove / upgrade
    branch: add / install / sync / install-diff / update / remove で対象ブランチを指定
    plugin: install で対象プラグイン名を指定
    local: True でローカルスコープでインストール
    """
    args = [sys.executable, str(TOOLS / "marketplace.py"), command]
    if branch:
        args.append(branch)
    if plugin:
        args.append(plugin)
    if local:
        args.append("-l")
    result = subprocess.run(args, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.stdout + result.stderr


@mcp.tool()
def reload_plugins() -> str:
    """起動中の tmux セッション（ait-* / plg-*）に /reload-plugins を送信する。"""
    result = subprocess.run(
        [sys.executable, str(TOOLS / "reload_plugins.py")],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return result.stdout + result.stderr or "送信完了"


@mcp.tool()
def sync_plugin_cache(plugin_name: str = "", update: bool = False) -> str:
    """ローカル編集したプラグインをキャッシュに同期する。

    plugin_name: 省略時はインストール済み全プラグインを同期
    update: True でマーケットプレイスの最新版に更新
    """
    args = [sys.executable, str(TOOLS / "sync_plugin_cache.py")]
    if update:
        args.append("--update")
    if plugin_name:
        args.append(plugin_name)
    result = subprocess.run(args, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.stdout + result.stderr


@mcp.tool()
def pre_merge_check(merge_branch: str) -> str:
    """マージ前にプラグインのバージョン更新漏れを確認する。

    問題がなければ空文字列、問題があれば警告メッセージを返す。
    """
    result = subprocess.run(
        [sys.executable, str(TOOLS / "pre_merge_check.py"), merge_branch],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return result.stdout or "バージョンチェック: 問題なし"


if __name__ == "__main__":
    mcp.run()
