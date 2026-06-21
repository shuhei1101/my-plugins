"""gh-kit プラグインのテンプレート取得用 MCP サーバー。

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

mcp = FastMCP("gh-kit-tools")


class CommandResult(BaseModel):
    success: bool = Field(description="終了コードが 0 なら True")
    output: str = Field(description="標準出力（success=False のときは標準エラー）")


TemplateName = Literal[
    "PRドキュメント.j2",
    "イシュードキュメント.j2",
    "レビュー結果コメント.j2",
    "コンフリクト通知コメント.j2",
    "Wikiページ.j2",
    "観点メニュー.md",
    "ファイル解決.md",
    "ユーザー確認要否判定.md",
]


@mcp.tool(
    title="テンプレート取得",
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
def template_get(
    template_name: Annotated[TemplateName, Field(description="取得対象のテンプレートファイル名（拡張子込み）")],
) -> CommandResult:
    """plugins/gh-kit/templates/ 配下のテンプレートを読み出して返す。Jinja2 ファイル（.j2）も raw 文字列として返す。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "templates" / "template_get.py"), template_name],
        capture_output=True, text=True,
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout if result.returncode == 0 else result.stderr,
    )


def _project_dir() -> str:
    return os.environ["CLAUDE_PROJECT_DIR"]


@mcp.tool(
    title="ワークツリー作成",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def worktree_create(
    branch_type: Annotated[Literal["feat", "fix", "docs", "chore", "refactor", "test"], Field(description="ブランチ種別")],
    title: Annotated[str, Field(description="ブランチタイトル（英数字ケバブケース。例: my-feature）")],
) -> CommandResult:
    """ブランチ {type}/{title} とワークツリー（.claude/worktrees/ 配下）を作成する。pr-implementer / pr-draft-creator が PR 実装の準備として呼ぶ。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "worktree" / "worktree-tool.py"),
         "create", "--type", branch_type, "--title", title],
        capture_output=True, text=True, cwd=_project_dir(),
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout + result.stderr,
    )


@mcp.tool(
    title="ワークツリー削除",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
def worktree_remove(
    branch: Annotated[str, Field(description="削除対象のブランチ名（例: feat/my-feature）。ワークツリーとブランチを両方削除する")],
) -> CommandResult:
    """マージ済みブランチのワークツリーとブランチを削除する。pr-reviewer が PR マージ完了後に呼ぶ。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "worktree" / "worktree-tool.py"),
         "remove", "--branch", branch],
        capture_output=True, text=True, cwd=_project_dir(),
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout + result.stderr,
    )


if __name__ == "__main__":
    mcp.run()
