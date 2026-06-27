"""marketplace.json に登録された全プラグインのバージョンを強制でバンプする（差分チェックなし）。

# 引数省略は minor バンプ
python tools/bump-version-all.py

# minor バンプ
python tools/bump-version-all.py minor

# major バンプ
python tools/bump-version-all.py major
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

# 終了コード
EXIT_OK = 0
EXIT_MARKETPLACE_NOT_FOUND = 2
EXIT_PARTIAL_FAILURE = 3  # 1 プラグイン以上で更新失敗
EXIT_STAGE_FAILED = 4     # バージョン更新は成功したが git add に失敗


def _parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "kind",
        nargs="?",
        default="minor",
        choices=("minor", "major"),
        help="バンプ種別（デフォルト: minor）",
    )
    return parser.parse_args()


def _parse_version(version: str) -> tuple[int, int]:
    """バージョン文字列 "major.minor" を (major, minor) に変換する。"""
    parts = version.split(".")
    if len(parts) != 2:
        raise ValueError(f"バージョン形式が不正です: {version!r}（期待値: 'major.minor'）")
    return int(parts[0]), int(parts[1])


def _bump(version: str, kind: str) -> str:
    """バージョンをバンプ。major バンプ時は minor を 0 にリセット。"""
    major, minor = _parse_version(version)
    if kind == "major":
        return f"{major + 1}.0"
    return f"{major}.{minor + 1}"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _force_bump_plugin(plugin_name: str, kind: str, mp_data: dict) -> bool:
    """指定プラグインの plugin.json をバンプし、marketplace.json 側も同じ値に揃える。

    戻り値: 成功なら True、何かしらエラーなら False。
    """
    plugin_json_path = PLUGINS_DIR / plugin_name / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        print(f"  スキップ: {plugin_name} の plugin.json が見つかりません", file=sys.stderr)
        return False

    plugin_data = _load_json(plugin_json_path)
    old_ver = plugin_data.get("version", "0.0")
    new_ver = _bump(old_ver, kind)
    plugin_data["version"] = new_ver
    _save_json(plugin_json_path, plugin_data)
    print(f"  {plugin_name}/plugin.json: {old_ver} → {new_ver}")

    # marketplace.json の対応エントリも同じバージョンに揃える
    for entry in mp_data.get("plugins", []):
        if entry.get("name") == plugin_name:
            entry["version"] = new_ver
            print(f"  marketplace.json[{plugin_name}]: → {new_ver}")
            return True

    print(f"  警告: marketplace.json に {plugin_name!r} が見つかりません", file=sys.stderr)
    return False


def main() -> int:
    opts = _parse_args()

    if not MARKETPLACE_JSON.exists():
        print(f"marketplace.json が見つかりません: {MARKETPLACE_JSON}", file=sys.stderr)
        return EXIT_MARKETPLACE_NOT_FOUND

    mp_data = _load_json(MARKETPLACE_JSON)
    plugin_names = [entry.get("name") for entry in mp_data.get("plugins", []) if entry.get("name")]

    if not plugin_names:
        print("marketplace.json に登録プラグインがありません。")
        return EXIT_OK

    print(f"全プラグインを {opts.kind} バンプします（{len(plugin_names)} 件）")

    failed: list[str] = []
    for name in plugin_names:
        print(f"[{name}] {opts.kind} バンプ")
        if not _force_bump_plugin(name, opts.kind, mp_data):
            failed.append(name)

    # marketplace.json は最後に 1 度だけ書き込む（部分失敗があっても整合性を保つ）
    _save_json(MARKETPLACE_JSON, mp_data)

    # 更新したマニフェスト類をまとめてステージング（marketplace.json + 成功した plugin.json）
    staged_paths = [str(MARKETPLACE_JSON.relative_to(REPO_ROOT))]
    for name in plugin_names:
        if name in failed:
            continue
        plugin_json = PLUGINS_DIR / name / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            staged_paths.append(str(plugin_json.relative_to(REPO_ROOT)))

    print(f"\nステージング: {len(staged_paths)} ファイル")
    stage_result = subprocess.run(
        ["git", "add", "--", *staged_paths],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if stage_result.returncode != 0:
        print(f"  git add 失敗: {stage_result.stderr.strip()}", file=sys.stderr)
        return EXIT_STAGE_FAILED

    if failed:
        print(f"\n一部失敗: {', '.join(failed)}", file=sys.stderr)
        return EXIT_PARTIAL_FAILURE
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # 想定外の例外はトレースバック出力して異常終了
        traceback.print_exc()
        sys.exit(1)
