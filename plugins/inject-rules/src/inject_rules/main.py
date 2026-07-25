"""ルール注入フックの composition root。"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from inject_rules.features.injection.builder import render_message
from inject_rules.features.injection.packer import pack_blocks
from inject_rules.features.injection.response import build_response
from inject_rules.features.injection.types import InjectionBlock
from inject_rules.features.rules.index import load_rules
from inject_rules.features.rules.matcher import match_rules
from inject_rules.features.rules.types import RuleDefinition
from inject_rules.features.session.store import clear_state, load_state, save_state
from inject_rules.features.session.types import SessionState
from inject_rules.integrations.cache.store import fetch_with_cache
from inject_rules.integrations.http.fetcher import fetch_text
from inject_rules.shared.logger import emit_log
from inject_rules.shared.settings import Settings
from inject_rules.shared.types import FetchText

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"
CONVENTIONS_TEMPLATE = "作業規約.txt"
TARGET_TOOLS = frozenset({"Read", "Write"})
CHAR_LIMIT = 10000
MIN_PARTIAL = 200
CACHE_TTL_SEC = 1800
DEFAULT_SESSION_ID = "default"
MAX_FETCH_WORKERS = 8


@dataclass(frozen=True, slots=True, kw_only=True)
class HookInput:
    """標準入力のペイロードから本フックが使うフィールドだけを取り出したもの。"""

    session_id: str = DEFAULT_SESSION_ID
    tool_name: str
    file_path: str
    cwd: Path


def _read_input(text: str) -> HookInput | None:
    """標準入力の JSON をフック入力に変換する。"""
    try:
        payload = json.loads(text)
    except ValueError:
        return None
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return None
    return HookInput(
        session_id=payload.get("session_id") or DEFAULT_SESSION_ID,
        tool_name=payload.get("tool_name", ""),
        file_path=file_path,
        cwd=Path(payload.get("cwd") or Path.cwd()),
    )


def _build_blocks(
    rules: list[RuleDefinition], *, state: SessionState, fetch: FetchText
) -> list[InjectionBlock]:
    """マッチしたルール定義から注入ブロックを組み立てる。"""
    # 直列に取ると件数分の待ち時間がそのままフックの待ち時間になる
    with ThreadPoolExecutor(max_workers=min(len(rules), MAX_FETCH_WORKERS)) as pool:
        futures = [pool.submit(fetch, rule.url) for rule in rules]

    blocks: list[InjectionBlock] = []
    for rule, future in zip(rules, futures, strict=True):
        try:
            body = future.result()
        except OSError as error:
            # 注入済みにしないので次のツール呼び出しで再試行される
            emit_log(
                "WARNING",
                "ルール本文を取得できませんでした",
                {"rule_url": rule.url, "error": str(error)},
                endpoint=Settings.from_env().otlp_endpoint,
            )
            continue
        offset = state.offset_of(rule.url)
        blocks.append(
            InjectionBlock(
                url=rule.url, patterns=rule.patterns, body=body[offset:], offset=offset
            )
        )
    return blocks


def main() -> int:
    """ファイル操作フックのエントリポイント。"""
    hook_input = _read_input(sys.stdin.read())
    if hook_input is None:
        return 0
    if hook_input.tool_name not in TARGET_TOOLS:
        return 0

    settings = Settings.from_env()
    state = load_state(hook_input.session_id, base_dir=settings.session_dir)
    # 通知済みの記録を落とさないよう、以降はどの経路でも状態を書き出してから戻る
    save = partial(save_state, hook_input.session_id, state, base_dir=settings.session_dir)

    # 注入元が未設定: 設定不備をセッションに 1 回だけ通知して素通しする
    if not settings.index_urls:
        if state.mark_notified("indexes_unset"):
            emit_log(
                "WARNING", "注入元が未設定のため注入しません", endpoint=settings.otlp_endpoint
            )
        save()
        return 0

    cached_fetch = partial(
        fetch_with_cache, fetch=fetch_text, cache_dir=settings.cache_dir, ttl_sec=CACHE_TTL_SEC
    )
    rules = load_rules(list(settings.index_urls), fetch=cached_fetch, state=state)
    # 索引が 1 件も取れない: Wiki 未整備とみなして 1 回だけ通知する
    if not rules:
        if state.mark_notified("index_missing"):
            emit_log(
                "WARNING",
                "索引が取得できないため注入しません",
                {"index_urls": ",".join(settings.index_urls)},
                endpoint=settings.otlp_endpoint,
            )
        save()
        return 0

    matched = [
        rule
        for rule in match_rules(rules, hook_input.file_path, base_dir=hook_input.cwd)
        if not state.is_injected(rule.url)
    ]
    if not matched:
        save()
        return 0

    blocks = _build_blocks(matched, state=state, fetch=cached_fetch)
    if not blocks:
        save()
        return 0

    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=TEMPLATE_DIR
    )
    for url in result.completed:
        state.mark_injected(url)
    for url, offset in result.partial.items():
        state.mark_partial(url, offset)
    save()

    loaded, total = len(result.completed), len(matched)
    message = render_message(
        result.blocks,
        remaining=result.remaining,
        loaded=loaded,
        total=total,
        template_dir=TEMPLATE_DIR,
    )
    response = build_response(result, message, loaded=loaded, total=total)
    print(json.dumps(response, ensure_ascii=False))
    return 0


def clear() -> int:
    """コンテキスト圧縮フックのエントリポイント。"""
    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        return 0
    settings = Settings.from_env()
    clear_state(payload.get("session_id") or DEFAULT_SESSION_ID, base_dir=settings.session_dir)
    return 0


def inject_conventions() -> int:
    """セッション開始フックのエントリポイント。"""
    conventions = (TEMPLATE_DIR / CONVENTIONS_TEMPLATE).read_text(encoding="utf-8")
    response = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": conventions,
        }
    }
    print(json.dumps(response, ensure_ascii=False))
    return 0
