"""dev-kit TypeScript type-check hook.

PostToolUse(Edit | Write | MultiEdit) で発火し、編集対象が *.ts / *.tsx の場合に
tsconfig.json を上方向に探索して `tsc --noEmit --incremental` を実行する。

エラーがあれば stdout に出力（Claude がコンテキストとして受け取る）。
decision: block は使わず、作業フローを止めない。

env トグル: `DEV_KIT_NEXT_TS_CHECK=false`/`0`/`no`/`off` で無効化（デフォルト有効）。
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

# ── 内部ヘルパ ────────────────────────────────────────────────


def _eprint(msg: str) -> None:
    sys.stderr.write(f"[dev-kit-ts-check] {msg}\n")


def _find_tsconfig(start: pathlib.Path) -> pathlib.Path | None:
    """start から親方向に tsconfig.json を探す（モノレポ対応）。"""
    current = start.resolve()
    for _ in range(20):
        candidate = current / "tsconfig.json"
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


# ── main ──────────────────────────────────────────────────────


def main() -> int:
    if os.environ.get("DEV_KIT_NEXT_TS_CHECK", "true").lower() in ("false", "0", "no", "off"):
        return 0
    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin parse error: {e}")
        return 0

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0

    file_path: str = data.get("tool_input", {}).get("file_path", "") or ""
    if not file_path:
        return 0

    # *.ts / *.tsx のみ対象
    if pathlib.Path(file_path).suffix not in (".ts", ".tsx"):
        return 0

    tsconfig = _find_tsconfig(pathlib.Path(file_path).parent)
    if tsconfig is None:
        _eprint(f"tsconfig.json not found above {pathlib.Path(file_path).parent}, skipping")
        return 0

    project_dir = str(tsconfig.parent)

    try:
        result = subprocess.run(
            ["tsc", "--noEmit", "--incremental"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        _eprint("tsc not found in PATH, skipping")
        return 0
    except subprocess.TimeoutExpired:
        _eprint("tsc timed out after 60s")
        return 0
    except Exception as e:
        _eprint(f"tsc execution error: {e}")
        return 0

    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        # stdout に出力 → Claude がツール結果コンテキストとして受け取り、型エラーを認識できる
        sys.stdout.write(
            f"[dev-kit-ts-check] TypeScript errors detected in {project_dir}:\n\n{output}\n"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
