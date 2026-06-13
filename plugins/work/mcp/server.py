"""work プラグインのコマンド群を MCP サーバーとして公開する。

# 実行方法（プラグインの .mcp.json から自動起動）
uv run --with mcp --with pyyaml python ${CLAUDE_PLUGIN_ROOT}/mcp/server.py
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
INDEX_YAML = ".work/tasks/index.yaml"
INDEX_ARCHIVE_YAML = ".work/tasks/index.archive.yaml"

mcp = FastMCP("work-tools")


class CommandResult(BaseModel):
    success: bool = Field(description="終了コードが 0 なら True")
    output: str = Field(description="標準出力と標準エラーを結合したログ")


def _project_dir() -> str:
    return os.environ["CLAUDE_PROJECT_DIR"]


def _run_script(script: str, args: list[str]) -> CommandResult:
    """scripts/ 配下のスクリプトをプロジェクトルートで実行する。script はサブフォルダ込みのパス（例: issue/issue-tool.py）。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=_project_dir(),
    )
    return CommandResult(
        success=result.returncode == 0,
        output=result.stdout + result.stderr,
    )


# ── ワークツリー ──────────────────────────────────────────────

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


# ── タスクインデックス ────────────────────────────────────────

@mcp.tool(
    title="タスクインデックスにエントリ追加",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def index_add(
    branch: Annotated[str, Field(description="ブランチ名（例: feat/my-feature）")],
    title: Annotated[str, Field(description="日本語タイトル")],
    branch_type: Annotated[str, Field(description="ブランチ種別（feat/fix/docs など）")],
    summary: Annotated[str, Field(description="作業の概要（1〜2 文）")],
    task: Annotated[str, Field(description="タスクフォルダ名（YYMMDD_日本語タイトル 形式）")],
) -> CommandResult:
    """メインリポジトリの .work/tasks/index.yaml に新しいブランチエントリを追加する。"""
    return _run_script("index/index-tool.py", [
        "add", INDEX_YAML,
        "--branch", branch, "--title", title, "--type", branch_type,
        "--summary", summary, "--task", task,
    ])


@mcp.tool(
    title="アクティブなタスク一覧を取得",
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
def index_list_active() -> CommandResult:
    """未完了のブランチエントリを branch|title|type|task 形式で一覧表示する。"""
    return _run_script("index/index-tool.py", ["list-active", INDEX_YAML])


@mcp.tool(
    title="完了済みタスク数を取得",
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
def index_completed_count() -> CommandResult:
    """index.yaml 内の完了済みエントリ数を返す。"""
    return _run_script("index/index-tool.py", ["completed-count", INDEX_YAML])


@mcp.tool(
    title="タスクインデックスを完了にマーク",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def index_set_completed(
    branch: Annotated[str, Field(description="完了にするブランチ名（例: feat/my-feature）")],
) -> CommandResult:
    """メインリポジトリの .work/tasks/index.yaml で指定ブランチを完了とマークする。"""
    return _run_script("index/index-tool.py", ["set-completed", INDEX_YAML, "--branch", branch])


@mcp.tool(
    title="完了エントリをアーカイブ",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def index_archive(
    archive_path: Annotated[str, Field(description="書き込み先 index.archive.yaml の絶対パス（通常はワークツリー内の .work/tasks/index.archive.yaml）")],
) -> CommandResult:
    """メインリポジトリの index.yaml から完了エントリを指定先の index.archive.yaml へ移動する。"""
    return _run_script("index/index-tool.py", ["archive", INDEX_YAML, archive_path])


@mcp.tool(
    title="タスクインデックスをトリム",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def index_trim(
    keep: Annotated[int, Field(description="保持する完了済みエントリの最大数（デフォルト 20）", default=20)] = 20,
) -> CommandResult:
    """index.yaml の完了済みエントリを最新 N 件だけ残してトリムする（古い完了エントリは index.archive.yaml に保存済みであること）。"""
    return _run_script("index/trim-index.py", [INDEX_YAML, "--keep", str(keep)])


# ── イシュー ──────────────────────────────────────────────────

@mcp.tool(
    title="イシューをクローズ",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def issue_close(
    issues_dir: Annotated[str, Field(description="対象 .work/issues ディレクトリの絶対パス（通常はワークツリー内）")],
    issue_id: Annotated[str, Field(description="クローズするイシュー ID（例: ISSUE-12）")],
    resolution: Annotated[Literal["resolved", "wontfix"], Field(description="解決種別")],
    linked_branch: Annotated[str, Field(description="解決したブランチ名")] = "",
) -> CommandResult:
    """イシューを closed/ へ移動し、_index.yaml から削除して _index.archive.yaml に記録する。"""
    extra = ["--linked-branch", linked_branch] if linked_branch else []
    return _run_script("issue/issue-tool.py", [
        "close",
        "--issues-dir", issues_dir,
        "--issue-id", issue_id,
        "--resolution", resolution,
        *extra,
    ])


@mcp.tool(
    title="イシューを進行中に移動",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def issue_move_to_progress(
    issues_dir: Annotated[str, Field(description="対象 .work/issues ディレクトリの絶対パス（通常はワークツリー内）")],
    issue_id: Annotated[str, Field(description="進行中にするイシュー ID（例: ISSUE-12）")],
) -> CommandResult:
    """イシューファイルを targets/ から progress/ へ移動し、_index.yaml の status を in_progress にする。"""
    return _run_script("issue/issue-tool.py", [
        "move-to-progress",
        "--issues-dir", issues_dir,
        "--issue-id", issue_id,
    ])


@mcp.tool(
    title="イシューのステータスを更新",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def issue_set_status(
    issues_dir: Annotated[str, Field(description="対象 .work/issues ディレクトリの絶対パス")],
    issue_id: Annotated[str, Field(description="更新するイシュー ID（例: ISSUE-12）")],
    status: Annotated[Literal["not_started", "in_progress"], Field(description="設定するステータス")],
) -> CommandResult:
    """_index.yaml の該当イシューエントリの status を更新する（ファイルは移動しない）。"""
    return _run_script("issue/issue-tool.py", [
        "set-status",
        "--issues-dir", issues_dir,
        "--issue-id", issue_id,
        "--status", status,
    ])


@mcp.tool(
    title="イシューにブランチを追記",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
def issue_add_branch(
    issues_dir: Annotated[str, Field(description="対象 .work/issues ディレクトリの絶対パス")],
    issue_id: Annotated[str, Field(description="対象イシュー ID（例: ISSUE-12）")],
    branch: Annotated[str, Field(description="追記するブランチ名（例: fix/foo）")],
) -> CommandResult:
    """_index.yaml の該当イシューエントリの branches 配列にブランチ名を追記する。"""
    return _run_script("issue/issue-tool.py", [
        "add-branch",
        "--issues-dir", issues_dir,
        "--issue-id", issue_id,
        "--branch", branch,
    ])


if __name__ == "__main__":
    mcp.run()
