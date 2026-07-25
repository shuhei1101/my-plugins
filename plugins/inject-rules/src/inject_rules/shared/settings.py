"""環境変数から読む設定。"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_OTLP_ENDPOINT = "http://localhost:4317"
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "inject-rules"
DEFAULT_SESSION_DIR = Path.home() / ".claude" / "tokens" / "inject-rules"


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    """ルール注入フックの設定。"""

    index_urls: tuple[str, ...] = ()
    otlp_endpoint: str = DEFAULT_OTLP_ENDPOINT
    cache_dir: Path = DEFAULT_CACHE_DIR
    session_dir: Path = DEFAULT_SESSION_DIR

    @classmethod
    def from_env(cls) -> Settings:
        """環境変数を読んで設定を組み立てる。"""
        raw_indexes = os.environ.get("INJECT_RULES_INDEXES", "")
        index_urls = tuple(part.strip() for part in raw_indexes.split(",") if part.strip())
        cache_dir = os.environ.get("INJECT_RULES_CACHE_DIR")
        session_dir = os.environ.get("INJECT_RULES_SESSION_DIR")
        return cls(
            index_urls=index_urls,
            otlp_endpoint=os.environ.get("INJECT_RULES_OTLP_ENDPOINT", DEFAULT_OTLP_ENDPOINT),
            cache_dir=Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR,
            session_dir=Path(session_dir) if session_dir else DEFAULT_SESSION_DIR,
        )
