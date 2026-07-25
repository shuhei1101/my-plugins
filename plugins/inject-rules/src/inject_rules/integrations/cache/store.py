"""取得済み本文のローカルキャッシュ。"""
from __future__ import annotations

import hashlib
import time
from pathlib import Path

from inject_rules.shared.logger import emit_log
from inject_rules.shared.settings import Settings
from inject_rules.shared.types import FetchText

CACHE_SUFFIX = ".txt"
UNLIMITED_TTL_SEC = 10**9  # 期限を問わずキャッシュを読むための実質無期限の寿命


def read_cache(url: str, *, cache_dir: Path, ttl_sec: int) -> str | None:
    """有効期限内のキャッシュを読む。"""
    path = cache_dir / (hashlib.sha256(url.encode("utf-8")).hexdigest() + CACHE_SUFFIX)
    if not path.exists():
        return None
    if time.time() - path.stat().st_mtime > ttl_sec:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        # 読めないキャッシュは無いものとして扱い、取得し直す
        return None


def write_cache(url: str, text: str, *, cache_dir: Path) -> None:
    """取得した本文をキャッシュへ書く。"""
    path = cache_dir / (hashlib.sha256(url.encode("utf-8")).hexdigest() + CACHE_SUFFIX)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError:
        # 保存できなくても次回取得し直せばよい
        return


def fetch_with_cache(url: str, *, fetch: FetchText, cache_dir: Path, ttl_sec: int) -> str:
    """キャッシュを優先し、無ければ取得して保存する。"""
    cached = read_cache(url, cache_dir=cache_dir, ttl_sec=ttl_sec)
    if cached is not None:
        return cached
    try:
        text = fetch(url)
    except OSError as error:
        stale = read_cache(url, cache_dir=cache_dir, ttl_sec=UNLIMITED_TTL_SEC)
        # 取得元が落ちていても前回の内容で注入を続ける
        if stale is None:
            raise
        emit_log(
            "WARNING",
            "取得に失敗したのでキャッシュを継続利用します",
            {"url": url, "error": str(error)},
            endpoint=Settings.from_env().otlp_endpoint,
        )
        # 次の再取得まで期限を延ばす
        write_cache(url, stale, cache_dir=cache_dir)
        return stale
    write_cache(url, text, cache_dir=cache_dir)
    return text
