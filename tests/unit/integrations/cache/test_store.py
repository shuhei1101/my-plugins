"""`integrations/cache/store.py` の単体テスト。"""
from __future__ import annotations

import os
import time
import urllib.error

import pytest

from inject_rules.integrations.cache.store import fetch_with_cache, read_cache, write_cache

A = "https://example.com/a.md"
TTL_SEC = 1800


def _expire(cache_dir, *, ttl_sec: int = TTL_SEC) -> None:
    """キャッシュディレクトリ配下の最終更新時刻を有効期限より過去にする。"""
    past = time.time() - ttl_sec - 1
    for path in cache_dir.iterdir():
        os.utime(path, (past, past))


# =========================
# read_cache
# =========================


def test_read_cache(tmp_path):
    """期限内の読み込み（正常系）。"""
    # 準備
    write_cache(A, "ルール本文", cache_dir=tmp_path)
    # 実行
    text = read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証
    assert text == "ルール本文"


def test_read_cache_when_missing(tmp_path):
    """未取得（正常系）。"""
    # 実行・検証
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) is None


def test_read_cache_when_expired(tmp_path):
    """期限切れ（正常系）。"""
    # 準備: 最終更新時刻を過去にする
    write_cache(A, "ルール本文", cache_dir=tmp_path)
    _expire(tmp_path)
    # 実行・検証
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) is None


# =========================
# write_cache
# =========================


def test_write_cache(tmp_path):
    """保存と読み込みの往復（正常系）。"""
    # 実行
    write_cache(A, "ルール本文", cache_dir=tmp_path)
    # 検証
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) == "ルール本文"


def test_write_cache_when_dir_missing(tmp_path):
    """ディレクトリの自動作成（正常系）。"""
    # 準備
    target = tmp_path / "未作成" / "配下"
    # 実行
    write_cache(A, "ルール本文", cache_dir=target)
    # 検証
    assert read_cache(A, cache_dir=target, ttl_sec=TTL_SEC) == "ルール本文"


# =========================
# fetch_with_cache
# =========================


def test_fetch_with_cache(tmp_path, fetch_stub):
    """初回の取得と保存（正常系）。"""
    # 準備: キャッシュなし
    fetch = fetch_stub({A: "ルール本文"})
    # 実行
    text = fetch_with_cache(A, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証
    assert text == "ルール本文"
    assert fetch.calls == [A]
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) == "ルール本文"


def test_fetch_with_cache_when_cached(tmp_path, fetch_stub):
    """キャッシュ優先（正常系）。"""
    # 準備: 期限内のキャッシュあり
    write_cache(A, "キャッシュの本文", cache_dir=tmp_path)
    fetch = fetch_stub({A: "取得した本文"})
    # 実行
    text = fetch_with_cache(A, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証: 通信を発生させない
    assert text == "キャッシュの本文"
    assert fetch.calls == []


def test_fetch_with_cache_when_expired(tmp_path, fetch_stub):
    """期限切れの再取得（正常系）。"""
    # 準備: 期限切れのキャッシュあり
    write_cache(A, "古い本文", cache_dir=tmp_path)
    _expire(tmp_path)
    fetch = fetch_stub({A: "新しい本文"})
    # 実行
    text = fetch_with_cache(A, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証: キャッシュが更新される
    assert text == "新しい本文"
    assert fetch.calls == [A]
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) == "新しい本文"


def test_fetch_with_cache_when_fetch_failed_with_cache(tmp_path, fetch_stub):
    """期限切れキャッシュの継続利用（正常系）。"""
    # 準備: 期限切れのキャッシュがあり、取得は失敗する
    write_cache(A, "前回の本文", cache_dir=tmp_path)
    _expire(tmp_path)
    fetch = fetch_stub({}, errors={A: urllib.error.URLError("接続できません")})
    # 実行
    text = fetch_with_cache(A, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証: 取得元が落ちても注入を止めない（有効期限が延びる）
    assert text == "前回の本文"
    assert read_cache(A, cache_dir=tmp_path, ttl_sec=TTL_SEC) == "前回の本文"


def test_fetch_with_cache_when_local(tmp_path, fetch_stub):
    """ローカルはキャッシュしない（正常系）。"""
    # 準備: ローカル絶対パスの場所
    local = "/home/user/repo/my-plugins/docs/rules/python/core/命名規則.md"
    fetch = fetch_stub({local: "本文"})
    # 実行: 2 回呼ぶ
    first = fetch_with_cache(local, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    second = fetch_with_cache(local, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
    # 検証: 毎回読み直し、キャッシュを作らない
    assert first == second == "本文"
    assert fetch.calls == [local, local]
    assert list(tmp_path.glob("*.txt")) == []


def test_fetch_with_cache_when_fetch_failed(tmp_path, fetch_stub):
    """取得失敗の伝播（異常系）。"""
    # 準備: キャッシュを持たない状態で取得が失敗する
    fetch = fetch_stub({}, errors={A: urllib.error.URLError("接続できません")})
    # 実行・検証
    with pytest.raises(urllib.error.URLError):
        fetch_with_cache(A, fetch=fetch, cache_dir=tmp_path, ttl_sec=TTL_SEC)
