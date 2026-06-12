"""worktree-tool — ワークツリーの作成・削除とセッショントークン管理。

# 使い方

# ブランチ + ワークツリーを作成（公式デフォルトの .claude/worktrees/ 配下）
python worktree-tool.py create --type feat --title my-feature

# ワークツリーとブランチを削除
python worktree-tool.py remove --branch feat/my-feature

トークン:
  作成時に ~/.claude/tokens/work/worktree/<CLAUDE_CODE_SESSION_ID>.json を書き、削除時に消す。
  Stop フック（work_complete_check.py）がこのトークンの有無で発火を制御する。

VS Code ワークスペース連携:
  環境変数 VSCODE_WORKSPACE_FILE に .code-workspace のパスが設定されていれば、
  作成時に folders 末尾へワークツリーを追加し、削除時に取り除く。未設定ならスキップ。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TOKEN_DIR = Path.home() / ".claude" / "tokens" / "work" / "worktree"
TOKEN_TTL_SECONDS = 7 * 24 * 3600  # 放置トークンの掃除期限（7日）


def _repo_root() -> Path:
    """カレントの git リポジトリルートを返す。"""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip())


def _session_id() -> str | None:
    """Claude Code セッション ID を環境変数から取得する（直接実行時は None）。"""
    return os.environ.get("CLAUDE_CODE_SESSION_ID")


def _to_vscode_path(path: Path) -> str:
    """WSL の /mnt/<drive>/ パスを Windows 形式（C:/...）に変換する（該当しなければそのまま）。"""
    m = re.match(r"^/mnt/([a-z])/(.*)$", str(path))
    if m:
        return f"{m.group(1).upper()}:/{m.group(2)}"
    return str(path)


def _load_workspace() -> tuple[Path, dict] | None:
    """環境変数 VSCODE_WORKSPACE_FILE からワークスペース定義を読み込む。

    未設定・ファイルなし・JSON 不正の場合は None（連携スキップ）。
    """
    raw = os.environ.get("VSCODE_WORKSPACE_FILE")
    if not raw:
        return None
    ws_path = Path(raw)
    if not ws_path.is_file():
        print(f"注意: VSCODE_WORKSPACE_FILE が見つかりません: {ws_path}", file=sys.stderr)
        return None
    try:
        return ws_path, json.loads(ws_path.read_text("utf-8"))
    except json.JSONDecodeError as e:
        # コメント付き JSONC などパースできない場合は壊さずスキップする
        print(f"注意: ワークスペースファイルを解析できないためスキップ: {e}", file=sys.stderr)
        return None


def _add_to_vscode_workspace(branch: str, worktree_path: Path) -> None:
    """ワークスペースの folders 末尾にワークツリーを追加する。"""
    loaded = _load_workspace()
    if loaded is None:
        return
    ws_path, data = loaded

    entry_path = _to_vscode_path(worktree_path)
    folders = data.setdefault("folders", [])
    # 同じパスが既にあれば追加しない
    if any(f.get("path") == entry_path for f in folders):
        return
    folders.append({"name": branch, "path": entry_path})
    ws_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"VS Code ワークスペースに追加: {entry_path}")


def _remove_from_vscode_workspace(worktree_path: Path) -> None:
    """ワークスペースの folders からワークツリーを取り除く。"""
    loaded = _load_workspace()
    if loaded is None:
        return
    ws_path, data = loaded

    entry_path = _to_vscode_path(worktree_path)
    folders = data.get("folders", [])
    kept = [f for f in folders if f.get("path") != entry_path]
    if len(kept) == len(folders):
        return
    data["folders"] = kept
    ws_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"VS Code ワークスペースから削除: {entry_path}")


def _cleanup_stale_tokens() -> None:
    """期限切れの放置トークンを削除する。"""
    if not TOKEN_DIR.is_dir():
        return
    now = time.time()
    for token in TOKEN_DIR.glob("*.json"):
        if now - token.stat().st_mtime > TOKEN_TTL_SECONDS:
            token.unlink(missing_ok=True)


def _write_token(branch: str, worktree_path: Path) -> None:
    """セッショントークンにワークツリー情報を追記する。"""
    sid = _session_id()
    if not sid:
        print("注意: CLAUDE_CODE_SESSION_ID がないためトークンは作成しません", file=sys.stderr)
        return

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    _cleanup_stale_tokens()

    token_path = TOKEN_DIR / f"{sid}.json"
    # 既存トークンがあれば worktrees リストに追記する（1セッション複数ワークツリー対応）
    data = json.loads(token_path.read_text("utf-8")) if token_path.is_file() else {"worktrees": []}
    data["worktrees"] = [w for w in data["worktrees"] if w["branch"] != branch]
    data["worktrees"].append({"branch": branch, "path": str(worktree_path)})
    token_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"トークン更新: {token_path}")


def _remove_from_token(branch: str) -> None:
    """セッショントークンからワークツリー情報を除去し、空になればトークンを削除する。"""
    sid = _session_id()
    if not sid:
        return

    token_path = TOKEN_DIR / f"{sid}.json"
    if not token_path.is_file():
        return

    data = json.loads(token_path.read_text("utf-8"))
    data["worktrees"] = [w for w in data.get("worktrees", []) if w["branch"] != branch]

    # ワークツリーが残っていなければトークンごと削除（Stop リマインダーが止まる）
    if data["worktrees"]:
        token_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"トークン更新: {token_path}")
    else:
        token_path.unlink()
        print(f"トークン削除: {token_path}")


def cmd_create(branch_type: str, title: str) -> int:
    """ブランチとワークツリーを作成し、セッショントークンを書く。"""
    repo = _repo_root()
    branch = f"{branch_type}/{title}"
    # ブランチ名の / をディレクトリ名に使えないため - に変換する
    dir_name = re.sub(r"[^a-zA-Z0-9._-]", "-", branch)
    worktree_path = repo / ".claude" / "worktrees" / dir_name

    if worktree_path.exists():
        print(f"エラー: ワークツリーが既に存在します: {worktree_path}", file=sys.stderr)
        return 1

    worktree_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "worktree", "add", str(worktree_path), "-b", branch],
        capture_output=True, text=True, cwd=repo,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    _write_token(branch, worktree_path)
    _add_to_vscode_workspace(branch, worktree_path)
    print(f"ブランチ: {branch}")
    print(f"ワークツリー: {worktree_path}")
    return 0


def cmd_remove(branch: str) -> int:
    """ワークツリーとブランチを削除し、セッショントークンを消す。"""
    repo = _repo_root()
    dir_name = re.sub(r"[^a-zA-Z0-9._-]", "-", branch)
    worktree_path = repo / ".claude" / "worktrees" / dir_name

    # 旧形式（../{repo名}-wt-* 形式）のワークツリーにも対応するため git worktree list から探す
    if not worktree_path.exists():
        listing = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True, text=True, cwd=repo,
        )
        found: str | None = None
        current_path: str | None = None
        for line in listing.stdout.splitlines():
            if line.startswith("worktree "):
                current_path = line.removeprefix("worktree ")
            elif line.startswith("branch ") and line.removeprefix("branch refs/heads/") == branch:
                found = current_path
        if not found:
            print(f"エラー: ブランチ {branch} のワークツリーが見つかりません", file=sys.stderr)
            return 1
        worktree_path = Path(found)

    result = subprocess.run(
        ["git", "worktree", "remove", str(worktree_path)],
        capture_output=True, text=True, cwd=repo,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode
    print(f"ワークツリー削除: {worktree_path}")

    result = subprocess.run(
        ["git", "branch", "-d", branch],
        capture_output=True, text=True, cwd=repo,
    )
    if result.returncode != 0:
        # マージ済みでないなどの理由で消せない場合はエラーを出して継続（ワークツリーは消えている）
        print(result.stderr, file=sys.stderr)
    else:
        print(f"ブランチ削除: {branch}")

    _remove_from_token(branch)
    _remove_from_vscode_workspace(worktree_path)
    return 0


def main() -> int:
    """エントリポイント。"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    create_parser = sub.add_parser("create", help="ブランチとワークツリーを作成")
    create_parser.add_argument("--type", required=True, dest="branch_type", help="ブランチ種別（feat/fix/docs など）")
    create_parser.add_argument("--title", required=True, help="ブランチタイトル（英数字ケバブケース）")

    remove_parser = sub.add_parser("remove", help="ワークツリーとブランチを削除")
    remove_parser.add_argument("--branch", required=True, help="削除対象のブランチ名（例: feat/my-feature）")

    args = parser.parse_args()
    if args.command == "create":
        return cmd_create(args.branch_type, args.title)
    return cmd_remove(args.branch)


if __name__ == "__main__":
    sys.exit(main())
