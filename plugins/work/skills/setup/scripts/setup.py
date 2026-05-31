"""
setup.py — workspace セットアップスクリプト

カレントディレクトリに .work/ ドキュメント構造を展開する。
既存ファイルはスキップする（上書きしない）。

使い方:
  python setup.py
"""

from __future__ import annotations

# ── 標準ライブラリ ──────────────────────────────────────────
import shutil
import sys
from pathlib import Path

# ── 定数 ────────────────────────────────────────────────────
# scripts/ → setup/ → skills/ → workspace/ → templates/.work/
TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates" / ".work"
TARGET_DIR = Path.cwd() / ".work"


# ── 内部ヘルパ ──────────────────────────────────────────────
def _expand(template_dir: Path, target_dir: Path) -> None:
    """テンプレートディレクトリをターゲットに再帰コピーする。既存ファイルはスキップし、.gitkeep はコピーしない。"""
    if not template_dir.exists():
        print(f"エラー: テンプレートが見つかりません: {template_dir}", file=sys.stderr)
        sys.exit(1)

    for src in sorted(template_dir.rglob("*")):
        relative = src.relative_to(template_dir)
        dst = target_dir / relative

        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue

        if src.name == ".gitkeep":
            dst.parent.mkdir(parents=True, exist_ok=True)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            print(f"  スキップ（既存）: {relative}")
        else:
            shutil.copy2(src, dst)
            print(f"  作成:       {relative}")


# ── main ────────────────────────────────────────────────────
def main() -> int:
    """メイン処理。.work/ をカレントディレクトリに展開する。"""
    TARGET_DIR.mkdir(exist_ok=True)
    print(f"テンプレートを展開中: {TARGET_DIR}")
    _expand(TEMPLATE_DIR, TARGET_DIR)

    # tasks/ は動的生成フォルダなのでテンプレートには含めずここで作成する
    (TARGET_DIR / "tasks").mkdir(exist_ok=True)
    print("  作成:       tasks/")

    # _index.yaml は issues/.gitignore で git 管理外のため、テンプレートに置けない → ここで生成する
    index_yaml = TARGET_DIR / "issues" / "_index.yaml"
    if not index_yaml.exists():
        index_yaml.write_text("# issue-scan / issue-create が管理する。Git 管理外（コミットしない）。\nlast_id: 0\nissues: []\n")
        print("  作成:       issues/_index.yaml")
    else:
        print("  スキップ（既存）: issues/_index.yaml")

    print(f"\nセットアップ完了: {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
