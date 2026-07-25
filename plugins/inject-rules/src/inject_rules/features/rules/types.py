"""ルールドメインのデータモデル。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RuleDefinition:
    """索引 1 行分のルール定義。"""

    url: str
    patterns: tuple[str, ...]
