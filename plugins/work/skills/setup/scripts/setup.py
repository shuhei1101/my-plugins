"""
setup.py — workspace セットアップスクリプト

カレントディレクトリに .work/ ドキュメント構造を展開する。
既存ファイルはスキップする（上書きしない）。

使い方:
  python setup.py
"""

# ── stdlib ──────────────────────────────────────────────────
import sys
from pathlib import Path

# ── constants ───────────────────────────────────────────────
TARGET_DIR = Path.cwd() / ".work"

_TASKS_GITIGNORE = "index.yaml\n"

_TASKS_INDEX_YAML = """\
# .work/tasks/index.yaml — ブランチ索引
#
# フィールド説明:
#   id        : 連番（アーカイブ参照用）
#   branch    : git ブランチ名（例: feat/my-feature）
#   title     : ブランチ文書の H1 タイトルそのまま
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
#   title     : ブランチ文書の H1 タイトルそのまま
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

# ── private helpers ─────────────────────────────────────────
def _write_if_new(path: Path, content: str) -> None:
    if path.exists():
        print(f"  skip (exists): {path.relative_to(TARGET_DIR)}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  created:       {path.relative_to(TARGET_DIR)}")


# ── main ────────────────────────────────────────────────────
def main() -> None:
    """メイン処理。.work/ をカレントディレクトリに展開する。"""
    TARGET_DIR.mkdir(exist_ok=True)
    print(f"Setting up: {TARGET_DIR}")

    (TARGET_DIR / "tasks").mkdir(exist_ok=True)
    print(f"  created:       tasks/")
    _write_if_new(TARGET_DIR / "tasks" / ".gitignore", _TASKS_GITIGNORE)
    _write_if_new(TARGET_DIR / "tasks" / "index.yaml", _TASKS_INDEX_YAML)
    _write_if_new(TARGET_DIR / "tasks" / "index.archive.yaml", _TASKS_INDEX_ARCHIVE_YAML)

    (TARGET_DIR / "notes").mkdir(exist_ok=True)
    print(f"  created:       notes/")

    (TARGET_DIR / "issues").mkdir(exist_ok=True)
    _write_if_new(TARGET_DIR / "issues" / ".gitignore", _ISSUES_GITIGNORE)
    _write_if_new(TARGET_DIR / "issues" / "_index.archive.yaml", _ISSUES_INDEX_ARCHIVE_YAML)

    # _index.yaml は issues/.gitignore で git 管理外のため、テンプレートに置けない → ここで生成する
    index_yaml = TARGET_DIR / "issues" / "_index.yaml"
    if not index_yaml.exists():
        index_yaml.write_text("# Managed by issue-scan / issue-create. Git-ignored (do not commit).\nlast_id: 0\nissues: []\n")
        print(f"  created:       issues/_index.yaml")
    else:
        print(f"  skip (exists): issues/_index.yaml")

    print(f"\nSetup complete: {TARGET_DIR}")


if __name__ == "__main__":
    main()
