"""
sync_rules.py — プロジェクト側で編集したルールをルールマーケットのテンプレートに同期する。

使い方:
    python sync_rules.py sync <project-root> <rule-name>

例:
    python sync_rules.py sync C:/Users/me/repo/myproject cascade-sync

処理内容:
    PROJECT/.claude/rules/<rule-name>.md
        → <plugin>/skills/rule-market/rules/<rule-name>.md にコピーする

注意: JP ミラー (rules-jp/) は自動同期されないので、実行後に手動で更新すること。
"""

import sys
from pathlib import Path


def sync(project_root: str, rule_name: str) -> None:
    """指定したルールをプロジェクトからプラグインのテンプレートへコピーする。"""
    project = Path(project_root).resolve()
    src = project / ".claude" / "rules" / f"{rule_name}.md"

    if not src.exists():
        print(f"エラー: {src} が見つかりません", file=sys.stderr)
        sys.exit(1)

    # スクリプト自身の場所を基準にプラグインの rules/ ディレクトリを特定する
    plugin_rules = Path(__file__).parent.parent / "rules"
    dst = plugin_rules / f"{rule_name}.md"

    if not plugin_rules.exists():
        print(f"エラー: プラグインの rules/ ディレクトリが見つかりません: {plugin_rules}", file=sys.stderr)
        sys.exit(1)

    content = src.read_text(encoding="utf-8")
    dst.write_text(content, encoding="utf-8")

    print(f"同期完了: {src}")
    print(f"      → {dst}")
    print()
    print("次のステップ:")
    print(f"  1. rules-jp/{rule_name}.md (JP ミラー) を手動で更新する")
    print("  2. .claude-plugin/plugin.json のバージョンをバンプする")
    print("  3. 両ファイルを同じコミットに含める")


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] != "sync":
        print(__doc__)
        sys.exit(1)
    sync(project_root=sys.argv[2], rule_name=sys.argv[3])


if __name__ == "__main__":
    main()
