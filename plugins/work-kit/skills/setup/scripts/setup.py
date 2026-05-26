"""
setup.py — work-kit セットアップスクリプト

カレントディレクトリに .work/ ドキュメント構造を展開する。
既存ファイルはスキップする（上書きしない）。

使い方:
  python setup.py
"""

# ── stdlib ──────────────────────────────────────────────────
import shutil
import sys
from pathlib import Path

# ── constants ───────────────────────────────────────────────
# scripts/ → setup/ → skills/ → work-kit/ → templates/.work/
TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates" / ".work"
TARGET_DIR = Path.cwd() / ".work"

# ── private helpers ─────────────────────────────────────────
def _expand(template_dir: Path, target_dir: Path) -> None:
    """
    テンプレートディレクトリをターゲットに再帰コピーする。
    既存ファイルはスキップし、.gitkeep はコピーしない。

    :param template_dir: コピー元テンプレートのパス
    :param target_dir: コピー先のパス
    """
    if not template_dir.exists():
        print(f"Error: template not found: {template_dir}", file=sys.stderr)
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
            print(f"  skip (exists): {relative}")
        else:
            shutil.copy2(src, dst)
            print(f"  created:       {relative}")

# ── main ────────────────────────────────────────────────────
def main() -> None:
    """メイン処理。.work/ をカレントディレクトリに展開する。"""
    TARGET_DIR.mkdir(exist_ok=True)
    print(f"Expanding template to: {TARGET_DIR}")
    _expand(TEMPLATE_DIR, TARGET_DIR)

    # tasks/ は動的生成フォルダなのでテンプレートには含めずここで作成する
    (TARGET_DIR / "tasks").mkdir(exist_ok=True)
    print(f"  created:       tasks/")

    # issues/ は _index.yaml を git 管理外にするため .gitignore が必要
    issues_dir = TARGET_DIR / "issues"
    issues_dir.mkdir(exist_ok=True)
    gitignore = issues_dir / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("_index.yaml\n")
        print(f"  created:       issues/.gitignore")
    else:
        print(f"  skip (exists): issues/.gitignore")

    print(f"\nSetup complete: {TARGET_DIR}")


if __name__ == "__main__":
    main()
