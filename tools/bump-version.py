"""プラグインバージョンを plugin.json と marketplace.json の両方で更新する。

# 使い方

# auto モード: master との差分から変更プラグインを自動検出してバンプ
python tools/bump-version.py minor
python tools/bump-version.py major

# 個別指定モード: プラグイン名とバンプ種別をペアで指定（複数可）
python tools/bump-version.py work minor
python tools/bump-version.py work minor another-plugin major
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

BumpKind = str  # "major" | "minor"


def _parse_version(version: str) -> tuple[int, int]:
    """バージョン文字列 "major.minor" を (major, minor) のタプルに変換する。"""
    parts = version.split(".")
    if len(parts) != 2:
        raise ValueError(f"バージョン形式が不正です: {version!r}（期待値: 'major.minor'）")
    return int(parts[0]), int(parts[1])


def _bump(version: str, kind: BumpKind) -> str:
    """バージョン文字列をバンプして返す。major バンプ時は minor を 0 にリセットする。"""
    major, minor = _parse_version(version)
    if kind == "major":
        return f"{major + 1}.0"
    return f"{major}.{minor + 1}"


def _load_json(path: Path) -> dict:
    """JSON ファイルを読み込む。"""
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: dict) -> None:
    """JSON ファイルを整形して書き込む。"""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _detect_changed_plugins() -> list[str]:
    """master との差分から変更されたプラグイン名の一覧を返す。"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "master"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    changed: list[str] = []
    seen: set[str] = set()
    for line in result.stdout.strip().splitlines():
        m = re.match(r"^plugins/([^/]+)/", line)
        if m:
            name = m.group(1)
            if name not in seen:
                seen.add(name)
                changed.append(name)
    return changed


def _is_already_bumped(plugin_name: str) -> bool:
    """master と比較してバージョンがすでに上がっているか確認する。"""
    result = subprocess.run(
        ["git", "show", f"master:plugins/{plugin_name}/.claude-plugin/plugin.json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        # master にまだ存在しない新規プラグインはバンプ済みとみなす
        return True

    master_ver = json.loads(result.stdout).get("version", "0.0")
    plugin_json_path = PLUGINS_DIR / plugin_name / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        return False

    current_ver = _load_json(plugin_json_path).get("version", "0.0")
    return current_ver != master_ver


def _bump_plugin(plugin_name: str, kind: BumpKind) -> None:
    """指定プラグインの plugin.json と marketplace.json のバージョンをバンプする。

    すでに master よりバージョンが上がっている場合はスキップする。
    """
    # すでにバンプ済みならスキップ
    if _is_already_bumped(plugin_name):
        print(f"  スキップ: {plugin_name} はすでにバージョンが上がっています")
        return

    plugin_json_path = PLUGINS_DIR / plugin_name / ".claude-plugin" / "plugin.json"

    # plugin.json を更新
    if not plugin_json_path.exists():
        print(f"  スキップ: {plugin_name} の plugin.json が見つかりません", file=sys.stderr)
        return

    plugin_data = _load_json(plugin_json_path)
    old_ver = plugin_data.get("version", "0.0")
    new_ver = _bump(old_ver, kind)
    plugin_data["version"] = new_ver
    _save_json(plugin_json_path, plugin_data)
    print(f"  {plugin_name}/plugin.json: {old_ver} → {new_ver}")

    # marketplace.json を更新
    if not MARKETPLACE_JSON.exists():
        print("  警告: marketplace.json が見つかりません", file=sys.stderr)
        return

    mp_data = _load_json(MARKETPLACE_JSON)
    updated = False
    for entry in mp_data.get("plugins", []):
        if entry.get("name") == plugin_name:
            entry["version"] = new_ver
            updated = True
            break

    if updated:
        _save_json(MARKETPLACE_JSON, mp_data)
        print(f"  marketplace.json[{plugin_name}]: → {new_ver}")
    else:
        print(f"  警告: marketplace.json に {plugin_name!r} が見つかりません", file=sys.stderr)


def main() -> int:
    """エントリポイント。"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "args",
        nargs="+",
        metavar="ARG",
        help=(
            "auto モード: minor または major のみ指定。"
            "個別モード: <plugin> <minor|major> のペアを 1 つ以上指定。"
        ),
    )
    opts = parser.parse_args()
    raw = opts.args

    # auto モード判定: 引数が 1 つで minor/major のみ
    if len(raw) == 1 and raw[0] in ("minor", "major"):
        kind: BumpKind = raw[0]
        plugins = _detect_changed_plugins()
        if not plugins:
            print("master との差分でプラグイン変更が検出されませんでした。")
            return 0
        print(f"変更プラグインを自動検出しました: {', '.join(plugins)}")
        for plugin in plugins:
            print(f"[{plugin}] {kind} バンプ")
            _bump_plugin(plugin, kind)
        return 0

    # 個別指定モード: <plugin> <kind> のペアを解析
    if len(raw) % 2 != 0:
        print("引数エラー: <plugin> <minor|major> のペアで指定してください。", file=sys.stderr)
        return 1

    pairs: list[tuple[str, BumpKind]] = []
    for i in range(0, len(raw), 2):
        plugin_name, kind_str = raw[i], raw[i + 1]
        if kind_str not in ("minor", "major"):
            print(f"引数エラー: '{kind_str}' は無効です。minor または major を指定してください。", file=sys.stderr)
            return 1
        pairs.append((plugin_name, kind_str))

    for plugin_name, kind in pairs:
        print(f"[{plugin_name}] {kind} バンプ")
        _bump_plugin(plugin_name, kind)

    return 0


if __name__ == "__main__":
    sys.exit(main())
