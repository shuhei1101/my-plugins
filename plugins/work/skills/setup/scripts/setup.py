"""
setup.py — workspace セットアップスクリプト

カレントディレクトリに .work/ ドキュメント構造をブートストラップする。
空ディレクトリと最小スケルトンを生成する（既存ファイルはスキップし、上書きしない）。
テンプレート／構成定義の本体は references/work-dir/ にあり、ref-inject が該当パスの
作成・編集時に注入する。

使い方:
  python setup.py
"""

from __future__ import annotations

# ── 標準ライブラリ ──────────────────────────────────────────
import sys
from pathlib import Path

# ── 定数 ────────────────────────────────────────────────────
TARGET_DIR = Path.cwd() / ".work"

_TASKS_GITIGNORE = "index.yaml\n"

_TASKS_INDEX_YAML = """\
# .work/tasks/index.yaml — ブランチ索引
#
# フィールド説明:
#   id        : 連番（アーカイブ参照用）
#   branch    : git ブランチ名（例: feat/my-feature）
#   title     : タスクドキュメントの H1 タイトルそのまま
#   type      : feat / fix / docs / refactor / chore / test
#   tags      : 自由形式タグ（省略可）
#   summary   : ファイルを開かずに内容がわかる一行説明
#   task      : タスクフォルダ名（YYMMDD_{title}）
#   completed : false = 進行中、true = マージ済み / 廃止済み

last_id: 0
branches: []
"""

_TASKS_INDEX_ARCHIVE_YAML = """\
# Managed by workspace merge skill. Archived (completed / abandoned) branches.
#
# フィールド説明:
#   id        : 連番
#   branch    : git ブランチ名
#   title     : タスクドキュメントの H1 タイトルそのまま
#   type      : feat / fix / docs / refactor / chore / test
#   tags      : 自由形式タグ（省略可）
#   summary   : 一行説明
#   task      : タスクフォルダ名（YYMMDD_{title}）
#   archived  : アーカイブ日（YYYY-MM-DD）
#   resolution: merged / abandoned

branches: []
"""

_ISSUES_GITIGNORE = "_index.yaml\n"

_ISSUES_INDEX_ARCHIVE_YAML = """\
# Managed by issue-scan / issue-create / merge. Committed to git.
closed_issues: []
scan_records: []
"""


# ── 内部ヘルパ ──────────────────────────────────────────────
def _write_if_new(path: Path, content: str) -> None:
    """ファイルが無ければ生成する。既存ならスキップ（上書きしない）。"""
    if path.exists():
        print(f"  スキップ（既存）: {path.relative_to(TARGET_DIR)}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  作成:       {path.relative_to(TARGET_DIR)}")


# ── main ────────────────────────────────────────────────────
def main() -> int:
    """メイン処理。.work/ をカレントディレクトリにブートストラップする。"""
    TARGET_DIR.mkdir(exist_ok=True)
    print(f"セットアップ中: {TARGET_DIR}")

    (TARGET_DIR / "tasks").mkdir(exist_ok=True)
    print("  作成:       tasks/")
    _write_if_new(TARGET_DIR / "tasks" / ".gitignore", _TASKS_GITIGNORE)
    _write_if_new(TARGET_DIR / "tasks" / "index.yaml", _TASKS_INDEX_YAML)
    _write_if_new(TARGET_DIR / "tasks" / "index.archive.yaml", _TASKS_INDEX_ARCHIVE_YAML)

    (TARGET_DIR / "notes").mkdir(exist_ok=True)
    print("  作成:       notes/")

    (TARGET_DIR / "issues").mkdir(exist_ok=True)
    _write_if_new(TARGET_DIR / "issues" / ".gitignore", _ISSUES_GITIGNORE)
    _write_if_new(TARGET_DIR / "issues" / "_index.archive.yaml", _ISSUES_INDEX_ARCHIVE_YAML)

    # _index.yaml は issues/.gitignore で git 管理外のため、テンプレートに置けない → ここで生成する
    index_yaml = TARGET_DIR / "issues" / "_index.yaml"
    if not index_yaml.exists():
        index_yaml.write_text(
            "# issue-scan / issue-create が管理する。Git 管理外（コミットしない）。\nlast_id: 0\nissues: []\n",
            encoding="utf-8",
        )
        print("  作成:       issues/_index.yaml")
    else:
        print("  スキップ（既存）: issues/_index.yaml")

    print(f"\nセットアップ完了: {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
