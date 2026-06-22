"""template_get.py — GitHub Wiki からテンプレートを取得して stdout に出力する CLI。

使い方:
  python template_get.py <template_name>

template_name は plugins/gh-kit/templates/ 配下のファイル名（拡張子込み）。
拡張子を除いた名前で Wiki ページを検索する（例: PRドキュメント.j2 → PRドキュメント）。

Wiki は GH_KIT_WIKI_PATH 環境変数で指定されたローカル clone から読み取る。
GH_KIT_WIKI_PATH が未設定または Wiki ページが存在しない場合は終了コード 2 でエラー終了する。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _wiki_path() -> Path | None:
    """GH_KIT_WIKI_PATH 環境変数から Wiki ローカル clone のパスを返す。未設定なら None。"""
    val = os.environ.get("GH_KIT_WIKI_PATH", "").strip()
    if not val:
        return None
    return Path(val)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("ERROR: 引数は template_name の 1 つだけ", file=sys.stderr)
        return 1

    name = argv[1]
    if "/" in name or ".." in name:
        print(f"ERROR: 不正なテンプレート名: {name}", file=sys.stderr)
        return 1

    # 拡張子を除いた Wiki ページ名を導出
    page_name = Path(name).stem  # 例: "PRドキュメント.j2" -> "PRドキュメント"

    # Wiki ローカル clone から取得
    wiki_dir = _wiki_path()
    if wiki_dir is None:
        print(
            "ERROR: GH_KIT_WIKI_PATH 環境変数が未設定。\n"
            "  Wiki ローカル clone のパスを GH_KIT_WIKI_PATH に設定してください。\n"
            "  例: GH_KIT_WIKI_PATH=/path/to/repo.wiki",
            file=sys.stderr,
        )
        return 2

    wiki_page = wiki_dir / f"{page_name}.md"
    if not wiki_page.is_file():
        print(
            f"ERROR: Wiki ページが見つかりません: {wiki_page}\n"
            f"  Wiki が初期化されているか確認してください。\n"
            f"  未 clone の場合: gh repo clone {{owner}}/{{repo}}.wiki {wiki_dir}",
            file=sys.stderr,
        )
        return 2

    sys.stdout.write(wiki_page.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
