"""
trim-index — 完了済みブランチエントリを index.yaml から index.archive.yaml に移動する。

使い方:
  python trim-index.py [index_yaml]

  index_yaml  index.yaml のパス（デフォルト: .work/tasks/index.yaml）

index.yaml を読み込み、`completed: true` のエントリを全て同ディレクトリの
index.archive.yaml に移動し、アクティブなエントリだけを残して index.yaml を書き直す。
`last_id` フィールドは完了済みエントリを削除した後も保持されるため、ブランチ採番は継続できる。
"""

from __future__ import annotations

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── サードパーティ ──────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("エラー: PyYAML がインストールされていません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

# ── 定数 ────────────────────────────────────────────────────
DEFAULT_INDEX = Path(".work/tasks/index.yaml")
ARCHIVE_NAME = "index.archive.yaml"
HEADER_COMMENT = "# .work/tasks/index.archive.yaml — Archived (completed) PR entries\n\n"


# ── 内部ヘルパ ──────────────────────────────────────────────
def _load(path: Path) -> dict:
    """YAML ファイルを読み込んで dict を返す。ファイルが存在しない場合は空 dict を返す。"""
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _dump(data: dict) -> str:
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _header_comment(text: str) -> str:
    """YAML ファイル先頭のコメントブロックを返す。"""
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            lines.append(line)
        else:
            break
    return "\n".join(lines) + "\n\n" if lines else ""


# ── main ────────────────────────────────────────────────────
def main() -> int:
    args = parse_args()
    index_path = Path(args.index_yaml)
    archive_path = index_path.parent / ARCHIVE_NAME

    if not index_path.exists():
        print(f"エラー: {index_path} が見つかりません。", file=sys.stderr)
        return 1

    raw = index_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}

    branches: list[dict] = data.get("branches", [])
    last_id: int = data.get("last_id") or (max((p["id"] for p in branches), default=0))

    active = [p for p in branches if not p.get("completed", False)]
    done = [p for p in branches if p.get("completed", False)]

    if not done:
        print("アーカイブ対象なし — 完了済みエントリが見つかりませんでした。")
        return 0

    # アーカイブにマージ（ID 重複はスキップ）
    archive_data = _load(archive_path)
    existing: list[dict] = archive_data.get("branches", [])
    existing_ids = {p["id"] for p in existing}
    merged = existing + [p for p in done if p["id"] not in existing_ids]
    merged.sort(key=lambda p: p["id"])

    prefix = HEADER_COMMENT if not archive_path.exists() else ""
    archive_path.write_text(prefix + _dump({"branches": merged}), encoding="utf-8")

    # index.yaml を書き直す（ヘッダーコメント + last_id + アクティブエントリのみ保持）
    comment = _header_comment(raw)
    index_path.write_text(comment + _dump({"last_id": last_id, "branches": active}), encoding="utf-8")

    print(f"{len(done)} 件の完了済みブランチを {archive_path} にアーカイブしました。")
    print(f"index.yaml: アクティブ {len(active)} 件、last_id={last_id}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "index_yaml",
        nargs="?",
        default=str(DEFAULT_INDEX),
        help=f"index.yaml のパス（デフォルト: {DEFAULT_INDEX}）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
