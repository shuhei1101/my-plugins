"""gh-kit プラグインのテンプレート取得用 MCP サーバー。

# 実行方法（プラグインの .mcp.json から自動起動）
uv run --with mcp python ${CLAUDE_PLUGIN_ROOT}/mcp/server.py
"""
from __future__ import annotations

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
    "観点メニュー.md",
    "ファイル解決.md",
    "ユーザーレビュー要否判定.md",
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


if __name__ == "__main__":
    mcp.run()
