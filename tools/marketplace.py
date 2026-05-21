#!/usr/bin/env python3
"""marketplace — レビュー用マーケットプレイスの追加・削除・一覧管理.

Usage::

# リモートブランチ一覧を確認
python tools/marketplace.py list

# 登録済みレビュー用マーケットプレイスの状態を表示
python tools/marketplace.py status

# 指定ブランチのマーケットプレイスを追加
python tools/marketplace.py add <ブランチ名>

# 指定ブランチの指定プラグインをインストール [-l でローカルスコープ]
python tools/marketplace.py install <ブランチ名> <プラグイン名> [-l]

# メインマーケットプレイスの全プラグインをインストール/更新（削除済みは自動アンインストール）
python tools/marketplace.py sync [-l]

# 指定ブランチのマーケットプレイスを追加 + 全プラグインをインストール/更新 [-l でローカルスコープ]
python tools/marketplace.py sync <ブランチ名> [-l]

# マーケットプレイス追加 + master と差分のあるプラグインのみインストール [-l でローカルスコープ]
python tools/marketplace.py install-diff <ブランチ名> [-l]

# 指定ブランチのマーケットプレイスを更新
python tools/marketplace.py update <ブランチ名>

# 指定ブランチのマーケットプレイスを削除
python tools/marketplace.py remove <ブランチ名>

# インストール済みプラグインのみ全て最新バージョンに更新（未インストールは触らない）
python tools/marketplace.py upgrade
"""

import argparse
import filecmp
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Final

KNOWN_MARKETPLACES: Final[Path] = Path.home() / ".claude" / "plugins" / "known_marketplaces.json"
MARKETPLACE_URL: Final[str] = "https://github.com/shuhei1101/my-plugins.git"
KEY_PREFIX: Final[str] = "mentaiko-claude-plugins"
CLAUDE_CMD: Final[list[str]] = ["cmd", "/c", "claude"] if sys.platform == "win32" else ["claude"]

MarketplaceData = dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="レビュー用マーケットプレイスの管理")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="リモートブランチ一覧")
    sub.add_parser("status", help="登録済みレビュー用マーケットプレイスの状態")

    add_parser = sub.add_parser("add", help="マーケットプレイスを追加（登録 + update のみ）")
    add_parser.add_argument("branch", help="レビュー対象のGitブランチ名")

    install_parser = sub.add_parser("install", help="指定プラグインをインストール")
    install_parser.add_argument("branch", help="対象のGitブランチ名")
    install_parser.add_argument("plugin", help="プラグイン名")
    install_parser.add_argument("-l", "--local", action="store_true", help="ローカルスコープでインストール")

    sync_parser = sub.add_parser("sync", help="全プラグインをインストール/更新（省略時はメイン、ブランチ指定も可）")
    sync_parser.add_argument("branch", nargs="?", default=None, help="対象のGitブランチ名（省略時はメインマーケットプレイス）")
    sync_parser.add_argument("-l", "--local", action="store_true", help="ローカルスコープでインストール")

    install_diff_parser = sub.add_parser("install-diff", help="マーケットプレイス追加 + master と差分のあるプラグインのみインストール")
    install_diff_parser.add_argument("branch", help="レビュー対象のGitブランチ名")
    install_diff_parser.add_argument("-l", "--local", action="store_true", help="ローカルスコープでインストール")

    update_parser = sub.add_parser("update", help="マーケットプレイスを更新")
    update_parser.add_argument("branch", help="更新対象のGitブランチ名")

    remove_parser = sub.add_parser("remove", help="マーケットプレイスを削除（プラグイン uninstall + キャッシュ削除）")
    remove_parser.add_argument("branch", help="削除対象のGitブランチ名")

    sub.add_parser("upgrade", help="インストール済みプラグインのみ全て最新バージョンに更新（未インストールは触らない）")

    return parser.parse_args()


def branch_to_key(branch: str) -> str:
    """ブランチ名をマーケットプレイスのキー名に変換する。

    :param branch: Gitブランチ名
    :return: known_marketplaces.json 上のキー名

    英数字以外をハイフンに置換してプレフィックスと結合する。
    例: "feat/nishikawa/add_plugins" → "my-plugins-feat-nishikawa-add-plugins"
    """
    suffix: str = re.sub(r"[^a-zA-Z0-9]", "-", branch)
    return f"{KEY_PREFIX}-{suffix}"


def load_marketplaces() -> MarketplaceData:
    """known_marketplaces.json を読み込む。

    :return: マーケットプレイス設定の辞書
    """
    return json.loads(KNOWN_MARKETPLACES.read_text(encoding="utf-8"))


def save_marketplaces(data: MarketplaceData) -> None:
    """known_marketplaces.json を書き出す。

    :param data: マーケットプレイス設定の辞書
    """
    KNOWN_MARKETPLACES.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def run_claude_cmd(args: list[str], *, allow_fail: bool = False) -> subprocess.CompletedProcess[str]:
    """claude CLI コマンドを実行する。

    :param args: claude に渡す引数リスト
    :param allow_fail: True なら非ゼロ終了でも例外を投げない
    :return: 実行結果
    """
    cmd: list[str] = CLAUDE_CMD + args
    print(f" > {' '.join(cmd)}")
    result: subprocess.CompletedProcess[str] = subprocess.run(
        cmd, capture_output=True, text=True, encoding='utf-8', errors='replace',
    )
    if result.stdout and result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and not allow_fail:
        if result.stderr and result.stderr.strip():
            print(result.stderr.strip())
        print(f"エラー: コマンドが失敗しました (exit {result.returncode})")
        sys.exit(1)
    return result


def get_installed_plugins(marketplace_key: str) -> list[str]:
    """指定マーケットプレイスからインストール済みのプラグイン名一覧を取得する。

    :param marketplace_key: マーケットプレイスのキー名
    :return: プラグイン名のリスト（"<plugin>@<marketplace>" 形式）

    claude plugin list の出力を行ごとにパースし、
    "❯ <plugin>@<marketplace_key>" 形式の行からプラグイン名を抽出する。
    """
    result: subprocess.CompletedProcess[str] = subprocess.run(
        CLAUDE_CMD + ["plugin", "list"],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
    )
    plugins: list[str] = []
    suffix: str = f"@{marketplace_key}"
    for line in result.stdout.splitlines():
        line = line.strip()
        if suffix in line and line.startswith("❯"):
            plugin_full: str = line.split("❯", 1)[1].strip()
            plugins.append(plugin_full)
    return plugins


def get_available_plugins(marketplace_key: str) -> list[str]:
    """マーケットプレイスのキャッシュから利用可能なプラグイン一覧を取得する。

    :param marketplace_key: マーケットプレイスのキー名
    :return: プラグイン名のリスト

    キャッシュの plugins/ ディレクトリ配下のサブディレクトリ名を列挙する。
    """
    cache_plugins_dir: Path = (
        Path.home() / ".claude" / "plugins" / "marketplaces" / marketplace_key / "plugins"
    )
    if not cache_plugins_dir.is_dir():
        return []
    return sorted(d.name for d in cache_plugins_dir.iterdir() if d.is_dir())


def get_plugin_scopes() -> dict[str, str]:
    """インストール済みプラグインのスコープを返す。

    :return: "plugin@marketplace" をキー、"user" or "local" を値とする辞書

    ユーザースコープは ~/.claude/plugins/installed_plugins.json、
    プロジェクトスコープは ./.claude/plugins/installed_plugins.json から読み込む。
    両方に存在する場合はプロジェクトスコープを優先する。
    """
    scopes: dict[str, str] = {}
    paths: list[tuple[Path, str]] = [
        (Path.home() / ".claude" / "plugins" / "installed_plugins.json", "user"),
        (Path(".claude") / "plugins" / "installed_plugins.json", "local"),
    ]
    for path, default_scope in paths:
        if not path.is_file():
            continue
        try:
            data: dict = json.loads(path.read_text(encoding="utf-8"))
            for plugin_full, entries in data.get("plugins", {}).items():
                if isinstance(entries, list) and entries:
                    scope: str = entries[0].get("scope", default_scope)
                    scopes[plugin_full] = scope
        except (json.JSONDecodeError, OSError):
            pass
    return scopes


def get_all_installed_plugins() -> dict[str, list[str]]:
    """インストール済みの全プラグインを取得する。

    :return: プラグイン名をキー、マーケットプレイスキーのリストを値とする辞書

    claude plugin list の出力から "❯ <plugin>@<marketplace>" 形式の行をパースする。
    """
    result: subprocess.CompletedProcess[str] = subprocess.run(
        CLAUDE_CMD + ["plugin", "list"],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
    )
    installed: dict[str, list[str]] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("❯") and "@" in line:
            plugin_full: str = line.split("❯", 1)[1].strip()
            name, marketplace = plugin_full.rsplit("@", 1)
            installed.setdefault(name, []).append(marketplace)
    return installed


def get_diff_plugins(marketplace_key: str) -> list[str]:
    """master（my-plugins）と比較して差分のあるプラグインを返す。

    :param marketplace_key: 比較対象のマーケットプレイスキー
    :return: 差分・新規プラグイン名のリスト

    master 側に存在しないプラグイン（新規）と、
    filecmp.dircmp で中身が異なるプラグイン（変更）を抽出する。
    """
    base_dir: Path = Path.home() / ".claude" / "plugins" / "marketplaces"
    master_plugins: Path = base_dir / KEY_PREFIX / "plugins"
    branch_plugins: Path = base_dir / marketplace_key / "plugins"

    if not branch_plugins.is_dir():
        return []

    all_plugins: list[str] = sorted(d.name for d in branch_plugins.iterdir() if d.is_dir())

    if not master_plugins.is_dir():
        return all_plugins

    diff: list[str] = []
    for name in all_plugins:
        master_dir: Path = master_plugins / name
        branch_dir: Path = branch_plugins / name
        if not master_dir.is_dir():
            diff.append(name)
            continue
        cmp: filecmp.dircmp = filecmp.dircmp(str(master_dir), str(branch_dir))
        if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.common_funny:
            diff.append(name)
            continue
        # サブディレクトリも再帰的に比較する
        if _has_subdiff(cmp):
            diff.append(name)

    return diff


def _has_subdiff(cmp: filecmp.dircmp) -> bool:
    """dircmp のサブディレクトリに差分があるか再帰的に判定する。

    :param cmp: filecmp.dircmp オブジェクト
    :return: 差分がある場合 True
    """
    for sub_cmp in cmp.subdirs.values():
        if sub_cmp.left_only or sub_cmp.right_only or sub_cmp.diff_files or sub_cmp.common_funny:
            return True
        if _has_subdiff(sub_cmp):
            return True
    return False


def install_plugins(plugins: list[str], marketplace_key: str, *, local: bool = False) -> None:
    """指定プラグイン群をインストールまたは更新する。

    :param plugins: プラグイン名のリスト
    :param marketplace_key: マーケットプレイスのキー名
    :param local: True ならローカルスコープでインストール

    - 未インストール → install
    - 同じマーケットプレイスからインストール済み → update
    - 別マーケットプレイスからインストール済み → uninstall → install
    """
    installed: dict[str, list[str]] = get_all_installed_plugins()

    duplicates: list[tuple[str, str]] = []
    for p in plugins:
        if p in installed:
            for existing_key in installed[p]:
                if existing_key != marketplace_key:
                    duplicates.append((p, existing_key))

    if duplicates:
        print("⚠ 以下のプラグインは別マーケットプレイスにも存在するため、切り替えます:")
        for name, existing_key in duplicates:
            print(f" {name} (元: {existing_key})")
        print()
        print("別マーケットプレイス側をアンインストール中...")
        for name, existing_key in duplicates:
            run_claude_cmd(["plugin", "uninstall", f"{name}@{existing_key}"], allow_fail=True)
        print()

    scope: str = "local" if local else "user"
    print(f"プラグインをインストール/更新中 ({len(plugins)} 個, scope: {scope})...")
    for p in plugins:
        plugin_full: str = f"{p}@{marketplace_key}"
        if p in installed and marketplace_key in installed[p]:
            cmd = ["plugin", "update", plugin_full]
        else:
            cmd = ["plugin", "install", plugin_full, "--scope", scope]
        run_claude_cmd(cmd)
    print()
    print("インストール済みプラグイン:")
    for p in plugins:
        print(f" {p}@{marketplace_key}")


def cmd_list() -> None:
    """リモートリポジトリのブランチ一覧を表示する。

    git ls-remote でリモートのブランチ参照を取得し、refs/heads/ 以下のブランチ名を抽出する。
    """
    print(f"リモートブランチ一覧 ({MARKETPLACE_URL}):")
    print()
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["git", "ls-remote", "--heads", MARKETPLACE_URL],
            capture_output=True, text=True, check=True, encoding='utf-8', errors='replace',
        )
    except subprocess.CalledProcessError as e:
        print(f"エラー: リモートへの接続に失敗しました。\n{e.stderr.strip()}")
        sys.exit(1)

    # ls-remote の出力: "<hash>\trefs/heads/<branch>" の各行からブランチ名を抽出する
    branches: list[str] = []
    for line in result.stdout.strip().splitlines():
        ref: str = line.split("\t", 1)[1]
        branch: str = ref.removeprefix("refs/heads/")
        branches.append(branch)

    if not branches:
        print(" (なし)")
    else:
        for branch in sorted(branches):
            print(f" {branch}")


def cmd_status() -> None:
    """登録済みレビュー用マーケットプレイスの状態を表示する。"""
    data: MarketplaceData = load_marketplaces()
    print("登録済みレビュー用マーケットプレイス:")
    print()
    # 全エントリからプレフィックスが一致するもの（＝レビュー用）だけを抽出して表示する
    found: int = 0
    for key in sorted(data):
        if key.startswith(KEY_PREFIX):
            ref: str = data[key].get("source", {}).get("ref", "(なし)")
            print(f" {key} → branch: {ref}")
            found += 1
    if found == 0:
        print(" (なし)")


def add_marketplace(branch: str) -> str:
    """マーケットプレイスを known_marketplaces.json に登録し、update を実行する。

    :param branch: レビュー対象のGitブランチ名
    :return: 生成されたマーケットプレイスキー
    """
    data: MarketplaceData = load_marketplaces()
    key: str = branch_to_key(branch)
    install_location: str = str(Path.home() / ".claude" / "plugins" / "marketplaces" / key)

    data[key] = {
        "source": {
            "source": "git",
            "url": MARKETPLACE_URL,
            "ref": branch,
        },
        "installLocation": install_location,
        "lastUpdated": "2026-01-01T00:00:00.000Z",
    }
    save_marketplaces(data)
    print(f"追加しました: {key} (branch: {branch})")
    print()

    print("マーケットプレイスを更新中...")
    run_claude_cmd(["plugin", "marketplace", "update", key])
    print()

    plugins: list[str] = get_available_plugins(key)
    if plugins:
        print("利用可能なプラグイン:")
        for p in plugins:
            print(f" {p}@{key}")
    else:
        print("利用可能なプラグインが見つかりませんでした。")

    return key


def cmd_add(branch: str) -> None:
    """マーケットプレイスを追加する（登録 + update のみ）。

    :param branch: レビュー対象のGitブランチ名
    """
    add_marketplace(branch)


def cmd_install(branch: str, plugin_name: str, *, local: bool = False) -> None:
    """指定ブランチの指定プラグインをインストールする。

    :param branch: 対象のGitブランチ名
    :param plugin_name: プラグイン名
    :param local: True ならローカルスコープでインストール
    """
    key: str = branch_to_key(branch)
    scope: str = "local" if local else "user"
    plugin_full: str = f"{plugin_name}@{key}"
    print(f"プラグインをインストール中: {plugin_full} (scope: {scope})")
    run_claude_cmd(["plugin", "install", plugin_full, "--scope", scope])


def uninstall_removed_plugins(available: list[str], marketplace_key: str) -> None:
    """インストール済みだが利用可能リストにないプラグインをアンインストールする。

    :param available: 現在利用可能なプラグイン名のリスト
    :param marketplace_key: 対象マーケットプレイスのキー名
    """
    installed: list[str] = get_installed_plugins(marketplace_key)
    installed_names: list[str] = [p.rsplit("@", 1)[0] for p in installed]
    to_remove: list[str] = [p for p in installed_names if p not in available]
    if not to_remove:
        return
    print(f"削除されたプラグインをアンインストール中 ({len(to_remove)} 個)...")
    for p in to_remove:
        run_claude_cmd(["plugin", "uninstall", f"{p}@{marketplace_key}"], allow_fail=True)
    print()


def cmd_sync(branch: str | None = None, *, local: bool = False) -> None:
    """全プラグインをインストール/更新し、削除済みプラグインをアンインストールする。

    :param branch: 対象のGitブランチ名（None の場合はメインマーケットプレイスを使用）
    :param local: True ならローカルスコープでインストール

    branch 省略時:
    - メインマーケットプレイス（KEY_PREFIX）を update して最新化
    - 利用可能な全プラグインを install/update
    - インストール済みだが利用可能リストにないプラグインを自動アンインストール

    branch 指定時:
    - 指定ブランチのマーケットプレイスを追加/更新
    - 同上
    """
    if branch is None:
        key: str = KEY_PREFIX
        print(f"メインマーケットプレイスを更新中: {key}")
        run_claude_cmd(["plugin", "marketplace", "update", key])
        print()
    else:
        key = add_marketplace(branch)

    available: list[str] = get_available_plugins(key)
    uninstall_removed_plugins(available, key)

    if available:
        install_plugins(available, key, local=local)
    else:
        print("利用可能なプラグインが見つかりませんでした。")


def cmd_install_diff(branch: str, *, local: bool = False) -> None:
    """マーケットプレイスを追加し、master と差分のあるプラグインのみインストールする。

    :param branch: レビュー対象のGitブランチ名
    :param local: True ならローカルスコープでインストール
    """
    key: str = add_marketplace(branch)

    diff_plugins: list[str] = get_diff_plugins(key)
    if diff_plugins:
        install_plugins(diff_plugins, key, local=local)
    else:
        print("master との差分プラグインはありません。")


def cmd_update(branch: str) -> None:
    """指定ブランチのマーケットプレイスを更新する。

    :param branch: 更新対象のGitブランチ名
    """
    data: MarketplaceData = load_marketplaces()
    key: str = branch_to_key(branch)

    if key not in data:
        print(f"登録されていません: {key}")
        sys.exit(1)

    print(f"マーケットプレイスを更新中: {key} (branch: {branch})")
    run_claude_cmd(["plugin", "marketplace", "update", key])


def cmd_remove(branch: str) -> None:
    """レビュー用マーケットプレイスを削除する。

    :param branch: 削除対象のGitブランチ名

    処理の流れ:
    1. 該当マーケットプレイスからインストール済みのプラグインを全て uninstall
    2. claude plugin marketplace remove でマーケットプレイス自体を削除
    3. 残骸を掃除
    4. 削除したプラグインのうち master マーケットプレイスにも存在するものを再 install
    """
    data: MarketplaceData = load_marketplaces()
    key: str = branch_to_key(branch)

    if key not in data:
        print(f"登録されていません: {key}")
        sys.exit(1)

    # 該当マーケットプレイスからインストール済みのプラグインを全て uninstall する
    installed: list[str] = get_installed_plugins(key)
    uninstalled_names: list[str] = []
    if installed:
        print("インストール済みプラグインを削除中...")
        for plugin_full in installed:
            name: str = plugin_full.rsplit("@", 1)[0]
            uninstalled_names.append(name)
            run_claude_cmd(["plugin", "uninstall", plugin_full], allow_fail=True)
        print()

    # マーケットプレイス自体を削除
    print("マーケットプレイスを削除中...")
    run_claude_cmd(["plugin", "marketplace", "remove", key])

    # claude plugin marketplace remove では削除されない残骸を掃除する
    plugins_dir: Path = Path.home() / ".claude" / "plugins"
    for subdir in ("cache", "marketplaces"):
        leftover: Path = plugins_dir / subdir / key
        if leftover.is_dir():
            shutil.rmtree(leftover)
            print(f" 残骸を削除: {subdir}/{key}")

    # master マーケットプレイスにも存在するプラグインを再インストールして復元する
    if uninstalled_names:
        master_plugins: list[str] = get_available_plugins(KEY_PREFIX)
        to_restore: list[str] = [p for p in uninstalled_names if p in master_plugins]
        if to_restore:
            print()
            print(f"master ({KEY_PREFIX}) から復元中 ({len(to_restore)} 個)...")
            for p in to_restore:
                run_claude_cmd(["plugin", "install", f"{p}@{KEY_PREFIX}"])
            print()
            print("復元済みプラグイン:")
            for p in to_restore:
                print(f" {p}@{KEY_PREFIX}")

    print()
    print(f"削除完了: {key} (branch: {branch})")


def cmd_upgrade() -> None:
    """インストール済みプラグインのみ全て最新バージョンに更新する。

    メインマーケットプレイス（KEY_PREFIX）からインストール済みのプラグインが対象。
    ユーザースコープ・プロジェクトスコープ両方を含む。
    未インストールのプラグインを新たにインストールすることはしない。
    スコープの変更もしない。

    マーケットプレイスから削除・リネームされたプラグインはアンインストールし、
    存在するものだけ update する。リネーム後の新名称は自動インストールしない。
    """
    print(f"マーケットプレイスキャッシュを更新中: {KEY_PREFIX}")
    run_claude_cmd(["plugin", "marketplace", "update", KEY_PREFIX])
    print()

    installed_all: dict[str, list[str]] = get_all_installed_plugins()
    targets: list[str] = sorted(
        name for name, keys in installed_all.items() if KEY_PREFIX in keys
    )

    if not targets:
        print("インストール済みプラグインが見つかりません。")
        return

    available: list[str] = get_available_plugins(KEY_PREFIX)

    removed: list[str] = [name for name in targets if name not in available]
    to_update: list[str] = [name for name in targets if name in available]

    if removed:
        print(f"削除・リネームされたプラグインをアンインストール中 ({len(removed)} 個)...")
        for name in removed:
            print(f" {name}@{KEY_PREFIX} はマーケットプレイスに存在しません — アンインストールします")
            run_claude_cmd(["plugin", "uninstall", f"{name}@{KEY_PREFIX}"], allow_fail=True)
        print()

    if not to_update:
        print("更新対象のプラグインがありません。")
        return

    scopes: dict[str, str] = get_plugin_scopes()

    print(f"プラグインを更新中 ({len(to_update)} 個)...")
    for name in to_update:
        plugin_full: str = f"{name}@{KEY_PREFIX}"
        scope: str = scopes.get(plugin_full, "user")
        print(f" {plugin_full} (scope: {scope})")
        run_claude_cmd(["plugin", "uninstall", plugin_full], allow_fail=True)
        run_claude_cmd(["plugin", "install", plugin_full, "--scope", scope])

    print()
    print("更新完了:")
    for name in to_update:
        print(f" {name}@{KEY_PREFIX}")


def main() -> None:
    if not KNOWN_MARKETPLACES.is_file():
        print(f"エラー: {KNOWN_MARKETPLACES} が見つかりません。")
        sys.exit(1)

    args = parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "status":
        cmd_status()
    elif args.command == "add":
        cmd_add(args.branch)
    elif args.command == "install":
        cmd_install(args.branch, args.plugin, local=args.local)
    elif args.command == "sync":
        cmd_sync(args.branch, local=args.local)
    elif args.command == "install-diff":
        cmd_install_diff(args.branch, local=args.local)
    elif args.command == "update":
        cmd_update(args.branch)
    elif args.command == "remove":
        cmd_remove(args.branch)
    elif args.command == "upgrade":
        cmd_upgrade()
    else:
        parse_args()
        sys.exit(1)


if __name__ == "__main__":
    main()
