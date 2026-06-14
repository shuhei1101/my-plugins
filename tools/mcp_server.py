"""my-plugins ツール群を MCP サーバーとして公開する。

# 実行方法（Claude Code の mcpServers から自動起動）
uv run --with mcp python tools/mcp_server.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"

mcp = FastMCP("my-plugins-tools")


class CommandResult(BaseModel):
    """ツールスクリプトの実行結果。"""

    success: bool = Field(description="終了コードが 0 なら True")
    output: str = Field(description="標準出力と標準エラーを結合したログ")


def _run_tool(args: list[str]) -> CommandResult:
    """tools/ 配下のスクリプトを実行して結果を返す。"""
    result = subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout + result.stderr,
    )


@mcp.tool(
    title="master を push して全体を更新",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def push() -> CommandResult:
    """master を origin に push し、marketplace upgrade と全 tmux セッションへの /reload-plugins 送信まで一括実行する。"""
    return _run_tool([str(TOOLS / "post_merge_upgrade.py")])


@mcp.tool(
    title="プラグインバージョンのバンプ",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def bump_version(
    bump_kind: Annotated[Literal["minor", "major"], Field(description="バンプ種別。major は minor を 0 にリセットする")],
    plugin_name: Annotated[str, Field(description="対象プラグイン名。省略時は master との差分から変更プラグインを自動検出")] = "",
) -> CommandResult:
    """プラグインの plugin.json と marketplace.json のバージョンを同時にバンプする。"""
    args = [str(TOOLS / "bump-version.py")]
    if plugin_name:
        args += [plugin_name, bump_kind]
    else:
        args += [bump_kind]
    return _run_tool(args)


@mcp.tool(
    title="マーケットプレイス管理",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def marketplace(
    command: Annotated[
        Literal["list", "status", "add", "install", "sync", "install-diff", "update", "remove", "upgrade"],
        Field(description="サブコマンド。list/status は読み取りのみ、remove はプラグイン uninstall を伴う"),
    ],
    branch: Annotated[str, Field(description="対象の Git ブランチ名。add/install/sync/install-diff/update/remove で指定")] = "",
    plugin: Annotated[str, Field(description="対象プラグイン名。install でのみ指定")] = "",
    local: Annotated[bool, Field(description="True でローカル（プロジェクト）スコープにインストール")] = False,
) -> CommandResult:
    """レビュー用マーケットプレイスの追加・削除・同期・アップグレードを行う。"""
    args = [str(TOOLS / "marketplace.py"), command]
    if branch:
        args.append(branch)
    if plugin:
        args.append(plugin)
    if local:
        args.append("-l")
    return _run_tool(args)


@mcp.tool(
    title="全セッションにプラグイン再読み込みを送信",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def reload_plugins() -> CommandResult:
    """marketplace.py upgrade でキャッシュを最新化してから、起動中の tmux セッション（ait-0〜10 / plg-1〜10）に /reload-plugins コマンドを送信する。"""
    return _run_tool([str(TOOLS / "reload_plugins.py")])


@mcp.tool(
    title="プラグインキャッシュ同期",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def sync_plugin_cache(
    plugin_name: Annotated[str, Field(description="対象プラグイン名。省略時はインストール済み全プラグインを同期")] = "",
    update: Annotated[bool, Field(description="True でマーケットプレイスの正規版に復元（ローカル編集を破棄）")] = False,
) -> CommandResult:
    """ローカル編集したプラグインを ~/.claude/plugins/cache/ に上書き同期する。キャッシュ側は一度削除してからコピーされる。"""
    args = [str(TOOLS / "sync_plugin_cache.py")]
    if update:
        args.append("--update")
    if plugin_name:
        args.append(plugin_name)
    return _run_tool(args)


@mcp.tool(
    title="マージ前バージョンチェック",
    annotations=ToolAnnotations(readOnlyHint=True),
)
def pre_merge_check(
    merge_branch: Annotated[str, Field(description="master にマージしようとしているブランチ名")],
) -> CommandResult:
    """マージ前に変更プラグインのバージョン更新漏れを確認する。output が空なら問題なし、警告メッセージがあれば bump_version の実行が必要。"""
    result = _run_tool([str(TOOLS / "pre_merge_check.py"), merge_branch])
    if result.success and not result.output.strip():
        result.output = "バージョンチェック: 問題なし"
    return result


if __name__ == "__main__":
    mcp.run()
