"""マージ前バージョンチェック: 変更プラグインのバージョン更新漏れを検出する。

# 使い方
python tools/pre_merge_check.py <merge_branch>

変更があればメッセージを stdout に出力、なければ何も出力しない。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _git_show(ref: str, path: str) -> str | None:
    """指定 ref のファイル内容を取得する。"""
    r = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return r.stdout if r.returncode == 0 else None


def check_pre_merge(merge_branch: str) -> str:
    """変更プラグインのバージョンを確認し、問題があれば警告メッセージを返す。

    問題がなければ空文字列を返す。
    """
    # 変更されたプラグインを取得
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"master..{merge_branch}"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    import re
    changed_plugins: set[str] = set()
    for line in diff.stdout.strip().splitlines():
        m = re.match(r"^plugins/([^/]+)/", line)
        if m:
            changed_plugins.add(m.group(1))

    if not changed_plugins:
        return ""

    # plugin.json バージョン比較
    not_bumped: list[str] = []
    for plugin in sorted(changed_plugins):
        master_raw = _git_show("master", f"plugins/{plugin}/.claude-plugin/plugin.json")
        branch_raw = _git_show(merge_branch, f"plugins/{plugin}/.claude-plugin/plugin.json")
        if not master_raw or not branch_raw:
            continue
        if json.loads(master_raw).get("version") == json.loads(branch_raw).get("version"):
            not_bumped.append(plugin)

    # marketplace.json バージョン比較
    mp_not_bumped: list[str] = []
    mp_master_raw = _git_show("master", ".claude-plugin/marketplace.json")
    mp_branch_raw = _git_show(merge_branch, ".claude-plugin/marketplace.json")
    if mp_master_raw and mp_branch_raw:
        mp_m = {p["name"]: p.get("version") for p in json.loads(mp_master_raw).get("plugins", [])}
        mp_b = {p["name"]: p.get("version") for p in json.loads(mp_branch_raw).get("plugins", [])}
        for plugin in sorted(changed_plugins):
            if mp_m.get(plugin) == mp_b.get(plugin):
                mp_not_bumped.append(plugin)

    if not not_bumped and not mp_not_bumped:
        return ""

    lines: list[str] = ["## バージョン更新が必要です\n\n"]

    if not_bumped:
        lines.append("以下のプラグインの `plugin.json` バージョンが master と同じです:\n\n")
        for p in not_bumped:
            lines.append(f"- **{p}**\n")
        lines.append("\n")

    if mp_not_bumped:
        lines.append("以下のプラグインの `marketplace.json` バージョンが更新されていません:\n\n")
        for p in mp_not_bumped:
            lines.append(f"- **{p}**\n")
        lines.append("\n")

    lines.append("以下のコマンドで自動更新できます:\n\n```bash\n")
    lines.append("# 変更プラグインを自動検出してマイナーバンプ\npython tools/bump-version.py minor\n\n")
    lines.append("# プラグインを個別指定する場合\n")
    for p in not_bumped:
        lines.append(f"python tools/bump-version.py {p} minor\n")
    lines.append("```\n")

    return "".join(lines)


def main() -> int:
    """エントリポイント。"""
    if len(sys.argv) < 2:
        print("使い方: python tools/pre_merge_check.py <merge_branch>", file=sys.stderr)
        return 1
    result = check_pre_merge(sys.argv[1])
    if result:
        print(result, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
