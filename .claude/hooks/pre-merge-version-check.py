"""
PreToolUse フック: master へのマージ前にプラグインバージョンの更新を確認する。

変更プラグインの plugin.json と marketplace.json が master と同一バージョンの場合は
ブロックして bump-version.py の実行を促す。
"""
import sys
import json
import re
import subprocess
import pathlib

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

# TTY から直接実行された場合は空の入力として扱う（stdin 待ちで固まるのを防ぐ）
raw = "" if sys.stdin.isatty() else sys.stdin.read()
d = json.loads(raw) if raw.strip() else {}

if d.get("tool_name") != "Bash":
    sys.exit(0)

cmd = (d.get("tool_input") or {}).get("command", "") or ""

if not re.search(r"\bgit\s+merge\b", cmd):
    sys.exit(0)

# master/main を取り込む操作はスキップ
if re.search(r"\bgit\s+merge\s+(origin/)?(master|main)\b", cmd):
    sys.exit(0)

# master ブランチ上でなければスキップ
branch = subprocess.run(
    ["git", "branch", "--show-current"],
    capture_output=True, text=True, cwd=REPO_ROOT,
).stdout.strip()
if branch != "master":
    sys.exit(0)

# マージ対象ブランチ名を取得
m = re.search(r"\bgit\s+merge\s+([^\s;|&]+)", cmd)
if not m:
    sys.exit(0)
merge_branch = m.group(1)


def git_show(ref, path):
    r = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return r.stdout if r.returncode == 0 else None


# 変更されたプラグインを取得
diff = subprocess.run(
    ["git", "diff", "--name-only", f"master..{merge_branch}"],
    capture_output=True, text=True, cwd=REPO_ROOT,
)
changed_plugins = set()
for line in diff.stdout.strip().splitlines():
    pm = re.match(r"^plugins/([^/]+)/", line)
    if pm:
        changed_plugins.add(pm.group(1))

if not changed_plugins:
    sys.exit(0)

# 各プラグインのバージョンを比較
not_bumped = []
for plugin in sorted(changed_plugins):
    master_raw = git_show("master", f"plugins/{plugin}/.claude-plugin/plugin.json")
    branch_raw = git_show(merge_branch, f"plugins/{plugin}/.claude-plugin/plugin.json")
    if not master_raw or not branch_raw:
        continue
    if json.loads(master_raw).get("version") == json.loads(branch_raw).get("version"):
        not_bumped.append(plugin)

# marketplace.json のバージョンも比較
mp_not_bumped = []
mp_master_raw = git_show("master", ".claude-plugin/marketplace.json")
mp_branch_raw = git_show(merge_branch, ".claude-plugin/marketplace.json")
if mp_master_raw and mp_branch_raw:
    mp_m = {p["name"]: p.get("version") for p in json.loads(mp_master_raw).get("plugins", [])}
    mp_b = {p["name"]: p.get("version") for p in json.loads(mp_branch_raw).get("plugins", [])}
    for plugin in sorted(changed_plugins):
        if mp_m.get(plugin) == mp_b.get(plugin):
            mp_not_bumped.append(plugin)

if not not_bumped and not mp_not_bumped:
    sys.exit(0)

# ブロックしてアドバイスを返す
lines = ["## バージョン更新が必要です\n\n"]

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

lines.append("以下のコマンドで自動更新できます:\n\n")
lines.append("```bash\n")
lines.append("# 変更プラグインを自動検出してマイナーバンプ\n")
lines.append("python tools/bump-version.py minor\n\n")
lines.append("# プラグインを個別指定する場合\n")
for p in not_bumped:
    lines.append(f"python tools/bump-version.py {p} minor\n")
lines.append("```\n")

ctx = "".join(lines)
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "additionalContext": ctx,
    },
}
sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
