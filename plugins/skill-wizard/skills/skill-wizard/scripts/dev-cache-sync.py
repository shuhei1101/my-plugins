#!/usr/bin/env python3
"""
[DEV] ローカルリポジトリのプラグインをClaudeのキャッシュに同期するデバッグ用スクリプト

開発中のプラグインをClaudeに反映して動作確認する際に使用します。
本番環境での使用は想定していません。

使い方:
    # 編集したファイルのパスから自動検出
    python dev-cache-sync.py --file-path /path/to/edited/SKILL.md

    # プラグインのソースディレクトリを直接指定
    python dev-cache-sync.py --source-path /path/to/repo/plugins/skill-wizard

    # 確認のみ（コピーしない）
    python dev-cache-sync.py --file-path /path/to/SKILL.md --dry-run

動作:
    1. プラグインルートを特定（--file-path の場合は .claude-plugin/plugin.json を上方向に探索）
    2. プラグイン名 = プラグインルートのディレクトリ名
    3. ~/.claude/plugins/installed_plugins.json からキャッシュパスを取得
    4. プラグインルート → キャッシュパスにコピー（キャッシュ側を上書き）
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# Windows環境でのUnicodeエンコードエラーを回避
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("cp932", "cp1252", "mbcs"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace") # type: ignore
    sys.stderr.reconfigure(encoding="utf-8", errors="replace") # type: ignore


def find_plugin_root_from_file(start_path: Path) -> Path:
    """
    ファイルパスから上に向かって .claude-plugin/plugin.json を探す。
    見つかったディレクトリがプラグインルート。
    """
    current = start_path if start_path.is_dir() else start_path.parent
    while True:
        if (current / ".claude-plugin" / "plugin.json").exists():
            return current
        parent = current.parent
        if parent == current:
            print(f"❌ エラー: .claude-plugin/plugin.json が見つかりません")
            print(f"   探索開始パス: {start_path}")
            sys.exit(1)
        current = parent


def find_cache_path(plugin_name: str) -> Path:
    """installed_plugins.json からキャッシュパスを取得する"""
    plugins_json = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    if not plugins_json.exists():
        print(f"❌ エラー: {plugins_json} が見つかりません")
        sys.exit(1)

    with open(plugins_json, encoding="utf-8") as f:
        data = json.load(f)

    plugins = data.get("plugins", {})

    matched_key = None
    for key in plugins:
        if key.startswith(f"{plugin_name}@"):
            matched_key = key
            break

    if matched_key is None:
        print(f"❌ エラー: '{plugin_name}' がinstalled_plugins.jsonに見つかりません")
        print(f"   登録済みプラグイン: {list(plugins.keys())}")
        sys.exit(1)

    entries = plugins[matched_key]
    if not entries:
        print(f"❌ エラー: '{matched_key}' のエントリが空です")
        sys.exit(1)

    return Path(entries[0]["installPath"])


def dev_sync(plugin_root: Path, dry_run: bool = False):
    """プラグインルートからキャッシュへ同期する"""
    if not (plugin_root / ".claude-plugin" / "plugin.json").exists():
        print(f"❌ エラー: 有効なプラグインディレクトリではありません: {plugin_root}")
        print(f"   .claude-plugin/plugin.json が見つかりません")
        sys.exit(1)

    plugin_name = plugin_root.name
    cache_path = find_cache_path(plugin_name)

    print()
    print("=" * 50)
    print("[DEV] プラグインキャッシュ同期")
    print("=" * 50)
    print(f"プラグイン名: {plugin_name}")
    print(f"コピー元:     {plugin_root}")
    print(f"コピー先:     {cache_path}")
    if dry_run:
        print("（ドライラン: ファイルはコピーされません）")
    print()

    if not dry_run:
        if cache_path.exists():
            shutil.rmtree(cache_path)
        shutil.copytree(plugin_root, cache_path)
        print("✓ 同期完了")
        print("  Claude Codeを再起動するとスキルに反映されます。")
    else:
        print("✓ ドライラン完了（実際のコピーはスキップ）")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="[DEV] 開発中のプラグインをClaudeのキャッシュに同期します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--file-path",
        help="編集したファイルのパス（このファイルが属するプラグインを自動検出）",
    )
    source_group.add_argument(
        "--source-path",
        help="プラグインのソースディレクトリを直接指定（.claude-plugin/plugin.json を含むディレクトリ）",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際のコピーを行わずに動作確認する",
    )

    args = parser.parse_args()

    try:
        if args.file_path:
            plugin_root = find_plugin_root_from_file(Path(args.file_path).resolve())
        else:
            plugin_root = Path(args.source_path).resolve()

        dev_sync(plugin_root, dry_run=args.dry_run)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
