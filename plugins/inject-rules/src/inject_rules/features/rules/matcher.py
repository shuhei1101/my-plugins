"""編集対象パスと glob の照合。"""
from __future__ import annotations

import re
from pathlib import Path

from inject_rules.features.rules.types import RuleDefinition


def match_rules(
    rules: list[RuleDefinition], file_path: str, *, base_dir: Path
) -> list[RuleDefinition]:
    """編集対象パスにマッチするルール定義を索引順に抽出する。"""
    candidates = _build_candidates(file_path, base_dir)
    matched: list[RuleDefinition] = []
    for rule in rules:
        for pattern in rule.patterns:
            regex = _glob_to_regex(pattern)
            # 1 パターンでも当たれば対象（同じルールを重複して積まない）
            if any(regex.match(candidate) for candidate in candidates):
                matched.append(rule)
                break
    return matched


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """glob パターンを全体一致用の正規表現に変換する。"""
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        # `**` は区切りをまたぐ（直後の区切りごと吸収して `**/foo` が `foo` にも当たるようにする）
        if pattern.startswith("**", index):
            parts.append(".*")
            index += 2
            if pattern.startswith("/", index):
                index += 1
            continue
        if char == "*":
            parts.append("[^/]*")
        elif char == "?":
            parts.append("[^/]")
        elif char == "{":
            parts.append("(?:")
        elif char == "}":
            parts.append(")")
        elif char == ",":
            parts.append("|")
        else:
            parts.append(re.escape(char))
        index += 1
    return re.compile("^" + "".join(parts) + "$")


def _build_candidates(file_path: str, base_dir: Path) -> list[str]:
    """照合に使うパス表現（絶対パスと基準ディレクトリからの相対パス）を組み立てる。"""
    target = Path(file_path)
    candidates = [str(target).replace("\\", "/")]
    try:
        relative = target.relative_to(base_dir)
    except ValueError:
        # 基準ディレクトリの外にあるパスは相対表現を持たない
        return candidates
    candidates.append(str(relative).replace("\\", "/"))
    return candidates
