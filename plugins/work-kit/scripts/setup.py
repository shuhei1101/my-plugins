"""
setup.py — work-kit セットアップスクリプト

プラグインのテンプレートを指定のプロジェクトディレクトリに展開する。
既存ファイルはスキップする（上書きしない）。

使い方:
  python setup.py <target_dir>

  <target_dir>: テンプレートを展開するプロジェクトルート（例: docs）
"""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import shutil
import sys
from pathlib import Path

# ── constants ───────────────────────────────────────────────
# スクリプト自身の位置からテンプレートフォルダを解決する
TEMPLATE_DIR = Path(__file__).parent.parent / "skills" / "setup" / "templates" / "docs"

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

        # .gitkeep はフォルダ維持用のみでコピー対象外
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
def main(args: argparse.Namespace) -> None:
    """メイン処理。テンプレートをターゲットに展開する。"""
    target = Path(args.target_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)

    print(f"Expanding template to: {target}")
    _expand(TEMPLATE_DIR, target)

    # tasks/ は動的生成フォルダなのでテンプレートには含めず、ここで作成する
    tasks_dir = target / "tasks"
    tasks_dir.mkdir(exist_ok=True)
    print(f"  created:       tasks/")

    print(f"\nSetup complete.")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。:return: 解析済み引数"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target_dir", help="テンプレートを展開するプロジェクトルート")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
