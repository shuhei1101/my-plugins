"""work プラグインのコマンド群を MCP サーバーとして公開する。

# 実行方法（プラグインの .mcp.json から自動起動）
uv run --with mcp python ${CLAUDE_PLUGIN_ROOT}/mcp/server.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

mcp = FastMCP("work-tools")


class CommandResult(BaseModel):
    success: bool = Field(description="終了コードが 0 なら True")
    output: str = Field(description="標準出力と標準エラーを結合したログ")


def _project_dir() -> str:
    return os.environ["CLAUDE_PROJECT_DIR"]


def _run_script(script: str, args: list[str]) -> CommandResult:
    """scripts/ 配下のスクリプトをプロジェクトルートで実行する。script はサブフォルダ込みのパス（例: worktree/worktree-tool.py）。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=_project_dir(),
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout + result.stderr,
    )


@mcp.tool(
    title="ワークツリー作成",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def worktree_create(
    branch_type: Annotated[Literal["feat", "fix", "docs", "chore", "refactor", "test"], Field(description="ブランチ種別")],
    title: Annotated[str, Field(description="ブランチタイトル（英数字ケバブケース。例: my-feature）")],
) -> CommandResult:
    """ブランチ {type}/{title} とワークツリー（.claude/worktrees/ 配下）を作成し、Stop リマインダー用のセッショントークンを書く。"""
    return _run_script("worktree/worktree-tool.py", ["create", "--type", branch_type, "--title", title])


@mcp.tool(
    title="ワークツリー削除",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def worktree_remove(
    branch: Annotated[str, Field(description="削除対象のブランチ名（例: feat/my-feature）。ワークツリーとブランチを両方削除する")],
) -> CommandResult:
    """マージ済みブランチのワークツリーとブランチを削除し、セッショントークンを消す。"""
    return _run_script("worktree/worktree-tool.py", ["remove", "--branch", branch])


if __name__ == "__main__":
    mcp.run()
