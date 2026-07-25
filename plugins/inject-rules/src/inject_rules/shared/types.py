"""ドメインをまたぐ型エイリアス。"""
from __future__ import annotations

from collections.abc import Callable

type FetchText = Callable[[str], str]
