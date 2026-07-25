"""ルール索引の取得と解析。"""
from __future__ import annotations

from inject_rules.features.rules.types import RuleDefinition
from inject_rules.features.session.types import SessionState
from inject_rules.shared.logger import emit_log
from inject_rules.shared.settings import Settings
from inject_rules.shared.types import FetchText

QUOTES = "\"'"
FETCH_FAILED_KEY = "index_fetch_failed"


def load_rules(
    index_urls: list[str], *, fetch: FetchText, state: SessionState
) -> list[RuleDefinition]:
    """索引 URL の一覧からルール定義の一覧を組み立てる。"""
    rules: list[RuleDefinition] = []
    seen: set[str] = set()
    for index_url in index_urls:
        try:
            text = fetch(index_url)
        except OSError as error:
            # 取得できない索引は飛ばし、残りの索引だけで注入を続ける
            # ツール呼び出しのたびに出さないよう、同じ索引の失敗は 1 回だけ通知する
            if state.mark_notified(f"{FETCH_FAILED_KEY}:{index_url}"):
                emit_log(
                    "WARNING",
                    "索引を取得できませんでした",
                    {"index_url": index_url, "error": str(error)},
                    endpoint=Settings.from_env().otlp_endpoint,
                )
            continue
        for rule in parse_index(text):
            # 同じルールが複数の索引にある場合は先の索引を優先する
            if rule.url in seen:
                continue
            seen.add(rule.url)
            rules.append(rule)
    return rules


def parse_index(text: str) -> list[RuleDefinition]:
    """索引 YAML の本文をルール定義の一覧に変換する。"""
    rules: list[RuleDefinition] = []
    url: str | None = None
    patterns: list[str] = []
    collecting = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        # 空行・コメント行・ルート要素は解析対象にしない
        if not line or line.startswith("#") or line == "rules:":
            continue
        # 新しいエントリの開始: 直前まで組み立てていたエントリを確定させる
        if line.startswith("- url:"):
            if url and patterns:
                rules.append(RuleDefinition(url=url, patterns=tuple(patterns)))
            value = line[len("- url:") :].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in QUOTES:
                value = value[1:-1]
            url = value
            patterns = []
            collecting = False
            continue
        # 以降の箇条書きを適用パターンとして集める
        if line.startswith("paths:"):
            collecting = True
            continue
        # クォートで囲まれた値だけ採用する（クォートなしは標準 YAML パーサが壊す書き方のため）
        if collecting and line.startswith("- "):
            value = line[2:].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in QUOTES:
                patterns.append(value[1:-1])

    if url and patterns:
        rules.append(RuleDefinition(url=url, patterns=tuple(patterns)))
    return rules
