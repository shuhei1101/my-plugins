"""
sync_rules.py — プロジェクト側で編集したルールをプラグインのソースリポジトリに同期する。

【重要】キャッシュ (~/.claude/plugins/cache/) ではなく、
プラグインの「開発元リポジトリ」に書き込む。
キャッシュに書いても次回インストール時に上書きされるため意味がない。

使い方:
    python sync_rules.py sync <project-root> <rule-name> --plugin-repo <marketplace-repo-root>

例:
    python sync_rules.py sync C:/Users/me/repo/myproject ai-models --plugin-repo C:/Users/me/repo/my-plugins

引数:
    <project-root>         ルールを編集したプロジェクトのルートパス
    <rule-name>            同期するルール名（拡張子なし）
    --plugin-repo <path>   プラグインのソースリポジトリのルートパス
                           （marketplace.json が置いてある場所）

処理内容:
    PROJECT/.claude/rules/<rule-name>.md
        → PLUGIN_REPO/plugins/claude-rule/skills/rule-market/rules/<rule-name>.md

    コピー後にリポジトリ側でコミット・公開が必要。

注意:
    JP ミラー (rules-jp/<rule-name>.md) は自動同期されないので、実行後に手動で更新すること。
"""

import argparse
import sys
from pathlib import Path


def sync(project_root: str, rule_name: str, plugin_repo: str) -> None:
    """指定したルールをプロジェクトからプラグインのソースリポジトリへコピーする。"""
    # コピー元：プロジェクトのルール
    src = Path(project_root).resolve() / ".claude" / "rules" / f"{rule_name}.md"
    if not src.exists():
        print(f"エラー: コピー元が見つかりません: {src}", file=sys.stderr)
        sys.exit(1)

    # コピー先：プラグインのソースリポジトリ（キャッシュではない）
    dst_dir = Path(plugin_repo).resolve() / "plugins" / "claude-rule" / "skills" / "rule-market" / "rules"
    if not dst_dir.exists():
        print(f"エラー: コピー先ディレクトリが見つかりません: {dst_dir}", file=sys.stderr)
        print("  --plugin-repo に正しいマーケットプレイスリポジトリのパスを指定してください。", file=sys.stderr)
        sys.exit(1)

    dst = dst_dir / f"{rule_name}.md"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"同期完了:")
    print(f"  元: {src}")
    print(f"  先: {dst}")
    print()
    print("次のステップ:")
    print(f"  1. {dst_dir.parent}/rules-jp/{rule_name}.md (JP ミラー) を手動で更新する")
    print(f"  2. {Path(plugin_repo)}/plugins/claude-rule/.claude-plugin/plugin.json のバージョンをバンプする")
    print(f"  3. 両ファイルをリポジトリにコミットして公開する")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["sync"], help="実行するコマンド")
    parser.add_argument("project_root", help="プロジェクトのルートパス")
    parser.add_argument("rule_name", help="ルール名（拡張子なし）")
    parser.add_argument("--plugin-repo", required=True, help="プラグインのソースリポジトリのルートパス")
    args = parser.parse_args()

    sync(project_root=args.project_root, rule_name=args.rule_name, plugin_repo=args.plugin_repo)


if __name__ == "__main__":
    main()
