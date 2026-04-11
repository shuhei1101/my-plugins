"""スキル検出ロジック。"""

import re
from pathlib import Path


def _parse_version(path: Path) -> tuple[int, ...] | None:
    """パス内からセマンティックバージョン(X.Y.Z)を抽出してタプルで返す。"""
    for part in path.parts:
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", part)
        if m:
            return tuple(int(x) for x in m.groups())
    return None


def find_skills(source_dir: Path) -> list[tuple[str, str, Path]]:
    """指定ディレクトリ配下を再帰探索し、SKILL.md を含むディレクトリをスキルとして検出する。

    同名スキルが複数バージョン見つかった場合は最新バージョンのみを返す。

    Returns: [(skill_name, relative_location, path), ...]
    """
    if not source_dir.exists():
        return []

    # 同名スキルの重複を最新バージョンで解決するための辞書
    best: dict[str, tuple[str, Path, tuple[int, ...] | None]] = {}

    for skill_md in source_dir.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        name = skill_dir.name
        try:
            rel = skill_dir.relative_to(source_dir)
            location = str(rel.parent) if str(rel.parent) != "." else "(root)"
        except ValueError:
            location = ""

        version = _parse_version(skill_dir.relative_to(source_dir))

        if name not in best:
            best[name] = (location, skill_dir, version)
        else:
            existing_ver = best[name][2]
            if version is not None and (existing_ver is None or version > existing_ver):
                best[name] = (location, skill_dir, version)

    return [(name, loc, path) for name, (loc, path, _) in best.items()]
