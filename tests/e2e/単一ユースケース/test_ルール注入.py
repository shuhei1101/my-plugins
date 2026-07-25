"""単一UC「ルール注入」の E2E テスト。"""
from __future__ import annotations

import os
import time
from pathlib import Path

from inject_rules.features.session.store import load_state
from inject_rules.integrations.cache.store import write_cache

TARGET = "docs/対象.md"
OTHER_TARGET = "docs/対象2.md"
MATCHING_GLOB = "**/*.md"
UNMATCHING_GLOB = "**/*.py"
INJECTED_MARK = "> 適用ルール: "
LOG_QUERY = '{service_name="inject-rules"}'
CACHE_TTL_SEC = 1800


def _index(entries: list[tuple[str, list[str]]]) -> str:
    """ルール索引 YAML を組み立てる。"""
    lines = ["rules:"]
    for url, patterns in entries:
        lines.append(f"  - url: {url}")
        lines.append("    paths:")
        lines.extend(f'      - "{pattern}"' for pattern in patterns)
    return "\n".join(lines) + "\n"


def _rule_body(marker: str, *, padding: int = 0) -> str:
    """マーカー入りのルール本文を組み立てる。"""
    return f"# 編集規約\n\n{marker}\n\n" + "あ" * padding


def _make_target(project: Path, name: str) -> Path:
    """編集対象のファイルを作る。"""
    path = project / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("初期内容\n", encoding="utf-8")
    return path


def _expire(cache_dir: Path) -> None:
    """キャッシュディレクトリ配下の最終更新時刻を有効期限より過去にする。"""
    past = time.time() - CACHE_TTL_SEC - 1
    for path in cache_dir.iterdir():
        os.utime(path, (past, past))


def _edit_prompt(*names: str) -> str:
    """指定ファイルの末尾に 1 行追記させるプロンプトを組み立てる。"""
    targets = "、".join(f"`{name}`" for name in names)
    return (
        f"{targets} の末尾に `追記` という 1 行をそれぞれ追記してください。"
        "1 つのファイルを終えてから次に取り掛かり、複数のファイルを同時に操作しないでください。"
        "確認や質問はせずに実行し、終わったら「完了」とだけ答えてください。"
    )


def test_normal(claude_project, wiki_server, session_dir, run_claude):
    """マッチしたルールがコンテキストに取り込まれ、対象ファイルが編集される（正常系）。"""
    # 準備: 編集対象にマッチするエントリを 1 件持つ索引とルール本文を配置する
    target = _make_target(claude_project, TARGET)
    rule_url = wiki_server.put("rule.md", _rule_body("MARKER_NAMING"))
    index_url = wiki_server.put("rules.yaml", _index([(rule_url, [MATCHING_GLOB])]))
    # 実行: 同一セッションで同じファイルを 2 回編集する
    prompt = (
        f"`{TARGET}` の末尾に `追記` という 1 行を追記し、"
        "そのあともう一度同じファイルの末尾に `再追記` という 1 行を追記してください。"
        "確認や質問はせずに実行し、終わったら「完了」とだけ答えてください。"
    )
    result = run_claude(prompt, indexes=index_url)
    # 検証: ルール本文が取り込まれ、対象ファイルが編集されている
    assert "MARKER_NAMING" in result.injected_text
    assert "追記" in target.read_text(encoding="utf-8")
    # 検証: 同じルールは再注入されない
    assert len([text for text in result.injections if rule_url in text]) == 1
    assert load_state(result.session_id, base_dir=session_dir).is_injected(rule_url) is True


def test_normal_when_multiple_indexes(claude_project, wiki_server, run_claude):
    """2 件の索引のルールが設定順に取り込まれる（正常系）。"""
    # 準備: 共通規約とプロジェクト固有規約を別々の索引に置く
    target = _make_target(claude_project, TARGET)
    first_rule = wiki_server.put("共通.md", _rule_body("MARKER_COMMON"))
    second_rule = wiki_server.put("固有.md", _rule_body("MARKER_PROJECT"))
    first_index = wiki_server.put("rules1.yaml", _index([(first_rule, [MATCHING_GLOB])]))
    second_index = wiki_server.put("rules2.yaml", _index([(second_rule, [MATCHING_GLOB])]))
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=f"{first_index},{second_index}")
    # 検証: 2 件とも取り込まれ、並び順が環境変数の設定順になっている
    injected = result.injected_text
    assert "MARKER_COMMON" in injected
    assert "MARKER_PROJECT" in injected
    assert injected.index("MARKER_COMMON") < injected.index("MARKER_PROJECT")
    assert "追記" in target.read_text(encoding="utf-8")


def test_normal_when_cache_valid(claude_project, unreachable_url, cache_dir, run_claude):
    """到達できない注入元でもキャッシュだけで注入が成立する（正常系）。"""
    # 準備: 索引とルール本文を有効期限内のキャッシュとして置く
    target = _make_target(claude_project, TARGET)
    rule_url = unreachable_url.replace("rules.yaml", "rule.md")
    write_cache(rule_url, _rule_body("MARKER_CACHED"), cache_dir=cache_dir)
    write_cache(
        unreachable_url, _index([(rule_url, [MATCHING_GLOB])]), cache_dir=cache_dir
    )
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=unreachable_url)
    # 検証: Wiki を参照せずに注入が成立している
    assert "MARKER_CACHED" in result.injected_text
    assert "追記" in target.read_text(encoding="utf-8")


def test_normal_when_over_limit(claude_project, wiki_server, run_claude):
    """上限を超えるルール本文が分割されて全量取り込まれる（正常系）。"""
    # 準備: 1 回の注入上限を超えるサイズのルール本文を配置する
    target = _make_target(claude_project, TARGET)
    body = _rule_body("MARKER_HEAD", padding=15000) + "\n\nMARKER_TAIL\n"
    rule_url = wiki_server.put("rule.md", body)
    index_url = wiki_server.put("rules.yaml", _index([(rule_url, [MATCHING_GLOB])]))
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=index_url)
    # 検証: 前半と後半の両方が取り込まれている
    injected = result.injected_text
    assert "MARKER_HEAD" in injected
    assert "MARKER_TAIL" in injected
    assert len(result.injections) >= 2
    assert "追記" in target.read_text(encoding="utf-8")


def test_normal_when_no_match(claude_project, wiki_server, run_claude):
    """マッチするルールがない場合は何も取り込まれない（正常系）。"""
    # 準備: 編集対象にマッチしない glob だけを持つ索引を配置する
    target = _make_target(claude_project, TARGET)
    rule_url = wiki_server.put("rule.md", _rule_body("MARKER_UNUSED"))
    index_url = wiki_server.put("rules.yaml", _index([(rule_url, [UNMATCHING_GLOB])]))
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=index_url)
    # 検証
    assert result.injections == []
    assert "追記" in target.read_text(encoding="utf-8")


def test_error_when_indexes_unset(claude_project, run_claude, query_logs):
    """注入元が未設定でも編集は通り、ログはセッション内で 1 件だけ記録される（異常系）。"""
    # 準備: 注入元を未設定にして 2 ファイルを対象にする
    first = _make_target(claude_project, TARGET)
    second = _make_target(claude_project, OTHER_TARGET)
    since = time.time()
    # 実行: 同一セッションで 2 件のファイルを編集する
    result = run_claude(_edit_prompt(TARGET, OTHER_TARGET), indexes=None)
    # 検証: フックが編集を妨げない
    assert result.injections == []
    assert "追記" in first.read_text(encoding="utf-8")
    assert "追記" in second.read_text(encoding="utf-8")
    # 検証: 注入元が未設定である旨のログが 1 件だけ記録されている
    lines = query_logs(f"{LOG_QUERY} |= `注入元が未設定`", since=since)
    assert len(lines) == 1


def test_error_when_index_missing(claude_project, wiki_server, run_claude, query_logs):
    """索引が存在しなくても編集は通り、ログはセッション内で 1 件だけ記録される（異常系）。"""
    # 準備: 索引 URL を配信しない（キャッシュも持たない）
    first = _make_target(claude_project, TARGET)
    second = _make_target(claude_project, OTHER_TARGET)
    index_url = wiki_server.url_for("rules.yaml")
    since = time.time()
    # 実行: 同一セッションで 2 件のファイルを編集する
    result = run_claude(_edit_prompt(TARGET, OTHER_TARGET), indexes=index_url)
    # 検証: Wiki 未整備でも編集を妨げない
    assert result.injections == []
    assert "追記" in first.read_text(encoding="utf-8")
    assert "追記" in second.read_text(encoding="utf-8")
    # 検証: 取得先 URL を含むログが 1 件だけ記録されている
    lines = query_logs(f"{LOG_QUERY} |= `索引が取得できないため注入しません`", since=since)
    assert len(lines) == 1
    assert index_url in lines[0]


def test_error_when_index_fetch_failed_with_cache(
    claude_project, unreachable_url, cache_dir, run_claude, query_logs
):
    """索引の取得に失敗しても期限切れキャッシュで注入が成立する（異常系）。"""
    # 準備: 期限切れの索引キャッシュを残したうえで到達できない索引 URL を設定する
    target = _make_target(claude_project, TARGET)
    rule_url = unreachable_url.replace("rules.yaml", "rule.md")
    write_cache(rule_url, _rule_body("MARKER_STALE"), cache_dir=cache_dir)
    write_cache(unreachable_url, _index([(rule_url, [MATCHING_GLOB])]), cache_dir=cache_dir)
    _expire(cache_dir)
    since = time.time()
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=unreachable_url)
    # 検証: キャッシュ済みの索引でマッチしたルールが取り込まれている
    assert "MARKER_STALE" in result.injected_text
    assert "追記" in target.read_text(encoding="utf-8")
    # 検証: キャッシュを継続利用した旨のログが記録されている
    lines = query_logs(f"{LOG_QUERY} |= `キャッシュを継続利用`", since=since)
    assert len(lines) >= 1


def test_error_when_rule_fetch_failed(
    claude_project, wiki_server, session_dir, run_claude, query_logs
):
    """取得できたルールだけが取り込まれ、失敗したルールは持ち越される（異常系）。"""
    # 準備: 実在するルールと実在しないルールの 2 エントリを索引に置く
    target = _make_target(claude_project, TARGET)
    ok_url = wiki_server.put("実在.md", _rule_body("MARKER_OK"))
    missing_url = wiki_server.url_for("実在しない.md")
    index_url = wiki_server.put(
        "rules.yaml", _index([(ok_url, [MATCHING_GLOB]), (missing_url, [MATCHING_GLOB])])
    )
    since = time.time()
    # 実行
    result = run_claude(_edit_prompt(TARGET), indexes=index_url)
    # 検証: 取得できたルールの本文だけが取り込まれている
    assert "MARKER_OK" in result.injected_text
    assert result.injected_text.count(INJECTED_MARK) == 1
    assert "追記" in target.read_text(encoding="utf-8")
    # 検証: 失敗したルールは注入済みとして記録されていない
    assert load_state(result.session_id, base_dir=session_dir).is_injected(missing_url) is False
    # 検証: 取得先 URL を含むログが記録されている
    lines = query_logs(f"{LOG_QUERY} |= `{missing_url}`", since=since)
    assert len(lines) >= 1
