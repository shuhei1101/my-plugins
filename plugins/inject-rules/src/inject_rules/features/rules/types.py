"""ルールドメインのデータモデル。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RuleDefinition:
    """索引 1 行分のルール定義。"""

    # 索引のベースと相対パスを結合した、解決済みの取得先（raw URL またはローカル絶対パス）
    location: str
    patterns: tuple[str, ...]
