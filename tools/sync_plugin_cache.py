#!/usr/bin/env python3
"""sync_plugin_cache — ローカル編集したプラグインをキャッシュに同期

Usage::

# 特定プラグインだけ同期
python tools/sync_plugin_cache.py <プラグイン名>

# インストール済みの全プラグインを一括同期
python tools/sync_plugin_cache.py

# 特定プラグインをマーケットプレイスの最新版に更新
python tools/sync_plugin_cache.py --update <プラグイン名>

# インストール済みの全プラグインを最新版に更新
python tools/sync_plugin_cache.py --update
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
PLUGINS_DIR: Final[Path] = REPO_ROOT / "plugins"
MARKETPLACE_NAME: Final[str] = "mentaiko-claude-plugins"
CACHE_DIR: Final[Path] = Path.home() / ".claude" / "plugins" / "cache" / MARKETPLACE_NAME
MARKETPLACE_DIR: Final[Path] = Path.home() / ".claude" / "plugins" / "marketplaces" / MARKETPLACE_NAME / "plugins"
CLAUDE_CMD: Final[list[str]] = ["cmd", "/c", "claude"] if sys.platform == "win32" else ["claude"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ローカルで編集したプラグインをキャッシュに同期する。"
        "キャッシュの場所: ~/.claude/plugins/cache/my-plugins/<プラグイン名>/<バージョン>/ "
        "ソースとキャッシュのバージョンが異なる場合、キャッシュ側のバージョンに同期する。"
        "元に戻す場合: claude plugin update <プラグイン名>@my-plugins",
    )
    parser.add_argument("plugin", nargs="?", default=None, help="プラグイン名（省略時は全プラグインを同期）")
    parser.add_argument("--update", action="store_true",
        help="マーケットプレイスの最新版に更新する（マーケットプレイス→キャッシュへコピー）")
    return parser.parse_args()


def _get_plugin_version(plugin_dir: Path) -> str | None:
    """plugin.json からバージョンを読み取る。"""
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.is_file():
        return None
    with plugin_json.open() as f:
        return json.load(f).get("version")


def _find_cached_version(plugin_name: str) -> str | None:
    """キャッシュ内にインストール済みのバージョンディレクトリを探す。"""
    plugin_cache = CACHE_DIR / plugin_name
    if not plugin_cache.is_dir():
        return None
    versions = [d.name for d in plugin_cache.iterdir() if d.is_dir()]
    if len(versions) == 1:
        return versions[0]
    return None


def sync_plugin(plugin_name: str) -> bool:
    """指定プラグインのローカルソースをキャッシュへ上書き同期する。

    :param plugin_name: プラグイン名（plugins/ 配下のディレクトリ名）
    :return: 同期成功なら True
    """
    src: Path = PLUGINS_DIR / plugin_name

    if not src.is_dir():
        print(f"エラー: プラグインが見つかりません: {src}")
        return False

    cached_version = _find_cached_version(plugin_name)
    if not cached_version:
        print(f"スキップ: キャッシュにインストールされていません: {plugin_name}")
        return False

    src_version = _get_plugin_version(src)
    if src_version and src_version != cached_version:
        print(f" 注意: ソースのバージョン ({src_version}) とキャッシュのバージョン ({cached_version}) が異なります。キャッシュ側 ({cached_version}) に同期します。")

    dst: Path = CACHE_DIR / plugin_name / cached_version

    # キャッシュを一度削除してからコピーすることで、削除済みファイルも反映する
    shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"同期完了: {plugin_name} (キャッシュ: {cached_version})")
    return True


def sync_all() -> None:
    """全プラグインを同期する。

    plugins/ 配下の各ディレクトリを走査し、
    キャッシュ側にも同名ディレクトリが存在するもの（＝インストール済み）だけを同期する。
    """
    synced: int = 0
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        if _find_cached_version(plugin_dir.name):
            sync_plugin(plugin_dir.name)
            synced += 1
    if synced == 0:
        print("同期対象のプラグインがありません。")
    else:
        print(f"\n{synced} 個のプラグインを同期しました。")


def _update_marketplace() -> bool:
    """claude plugin marketplace update でマーケットプレイスを最新化する。"""
    print("マーケットプレイスを更新中...")
    result = subprocess.run(
        CLAUDE_CMD + ["plugin", "marketplace", "update", MARKETPLACE_NAME],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f" 警告: マーケットプレイスの更新に失敗しました: {result.stderr.strip()}")
        return False
    print(" マーケットプレイス更新完了")
    return True


def restore_plugin(plugin_name: str) -> bool:
    """マーケットプレイス側からキャッシュへコピーして正規版に復元する。"""
    src: Path = MARKETPLACE_DIR / plugin_name

    if not src.is_dir():
        print(f"エラー: マーケットプレイスにプラグインが見つかりません: {plugin_name}")
        return False

    cached_version = _find_cached_version(plugin_name)
    if not cached_version:
        print(f"スキップ: キャッシュにインストールされていません: {plugin_name}")
        return False

    dst: Path = CACHE_DIR / plugin_name / cached_version

    shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"復元完了: {plugin_name} (キャッシュ: {cached_version})")
    return True


def restore_all() -> None:
    """キャッシュ内の全プラグインをマーケットプレイスの正規版に復元する。"""
    _update_marketplace()

    restored = 0
    for plugin_dir in sorted(MARKETPLACE_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue
        if _find_cached_version(plugin_dir.name):
            restore_plugin(plugin_dir.name)
            restored += 1

    if restored == 0:
        print("復元対象のプラグインがありません。")
    else:
        print(f"\n{restored} 個のプラグインを復元しました。")


def main() -> None:
    args = parse_args()

    if args.update:
        if args.plugin:
            if not restore_plugin(args.plugin):
                sys.exit(1)
        else:
            restore_all()
        return

    if not CACHE_DIR.is_dir():
        print(f"エラー: キャッシュディレクトリが見つかりません: {CACHE_DIR}")
        print("my-plugins マーケットプレイスがインストールされていることを確認してください。")
        sys.exit(1)

    if args.plugin:
        if not sync_plugin(args.plugin):
            sys.exit(1)
    else:
        sync_all()


if __name__ == "__main__":
    main()
