"""ルール注入ユースケースの結合テスト。"""
from __future__ import annotations

import json
import os
import time
import urllib.error
from pathlib import Path

from inject_rules.features.session.store import load_state, save_state
from inject_rules.features.session.types import SessionState
from inject_rules.integrations.cache.store import read_cache, write_cache

SESSION = "9f2c1b"
INDEX_URL = "https://example.com/rules.yaml"
INDEX_URL_2 = "https://example.com/other.yaml"
A = "https://example.com/a.md"
B = "https://example.com/b.md"
# 索引には索引ファイルからの相対パスを書く（ベースは索引の場所の親）
A_REL, B_REL = "a.md", "b.md"
FILE_PATH = "/repo/src/a.py"
CWD = "/repo"
CACHE_TTL_SEC = 1800
CHAR_LIMIT = 10000


def _payload(*, tool_name: str = "Read", file_path: str = FILE_PATH) -> dict:
    """フックのペイロードを組み立てる。"""
    return {
        "session_id": SESSION,
        "tool_name": tool_name,
        "cwd": CWD,
        "tool_input": {"file_path": file_path},
    }


def _response(capsys) -> dict | None:
    """標準出力の応答 JSON を返す（空なら None）。"""
    out = capsys.readouterr().out.strip()
    return json.loads(out) if out else None


def _install_fetch(monkeypatch, fetch) -> None:
    """プロジェクト Wiki への HTTP 取得を stub に差し替える。"""
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)


def _record_logs(monkeypatch, target: str) -> list[dict]:
    """観測基盤への送信を stub に差し替えて送出内容を記録する。"""
    logs: list[dict] = []

    def _emit(level: str, message: str, attributes: dict | None = None, *, endpoint: str) -> None:
        logs.append({"level": level, "message": message, "attributes": attributes or {}})

    monkeypatch.setattr(target, _emit)
    return logs


def _expire_cache(cache_dir: Path) -> None:
    """キャッシュディレクトリ配下の最終更新時刻を有効期限より過去にする。"""
    past = time.time() - CACHE_TTL_SEC - 1
    for path in cache_dir.iterdir():
        os.utime(path, (past, past))


def test_normal(monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook):
    """マッチしたルールを取得してコンテキストに追加し、実行を許可する（正常系）。"""
    # 準備
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    _install_fetch(
        monkeypatch, fetch_stub({INDEX_URL: rule_index([(A_REL, ["**/*.py"])]), A: "命名規約の本文"})
    )
    # 実行
    run_hook(_payload())
    # 検証
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "命名規約の本文" in output["additionalContext"]
    assert A in output["additionalContext"]
    assert "`**/*.py`" in output["additionalContext"]
    assert load_state(SESSION, base_dir=hook_dirs.session).is_injected(A) is True


def test_normal_when_multiple_indexes(
    monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook
):
    """複数の索引を設定順にマージしてから照合する（正常系）。"""
    # 準備: 索引 2 件がそれぞれ別のルールを持つ
    monkeypatch.setenv("INJECT_RULES_INDEXES", f"{INDEX_URL},{INDEX_URL_2}")
    _install_fetch(
        monkeypatch,
        fetch_stub(
            {
                INDEX_URL: rule_index([(A_REL, ["**/*.py"])]),
                INDEX_URL_2: rule_index([(B_REL, ["**/*.py"])]),
                A: "共通規約の本文",
                B: "プロジェクト規約の本文",
            }
        ),
    )
    # 実行
    run_hook(_payload())
    # 検証: 設定順に並び、取得元 URL がそれぞれの索引から解決されている
    output = _response(capsys)["hookSpecificOutput"]
    context = output["additionalContext"]
    assert output["permissionDecision"] == "allow"
    assert context.index("共通規約の本文") < context.index("プロジェクト規約の本文")
    assert A in context
    assert B in context


def test_normal_when_local(monkeypatch, capsys, tmp_path, hook_dirs, rule_index, run_hook):
    """索引もルール本文もローカルのファイルから読む（正常系・注入元がローカル）。"""
    # 準備: 一時ディレクトリに索引とルール本文を配置し、HTTP 取得は呼ばれないことを確かめる stub にする
    docs = tmp_path / "docs"
    (docs / "rules" / "python").mkdir(parents=True)
    rule_path = docs / "rules" / "python" / "命名規則.md"
    rule_path.write_text("ローカルの命名規約\n", encoding="utf-8")
    index_path = docs / "rules.yaml"
    index_path.write_text(rule_index([("rules/python/命名規則.md", ["**/*.py"])]), encoding="utf-8")
    monkeypatch.setenv("INJECT_RULES_INDEXES", str(index_path))
    urlopen_calls: list[str] = []
    monkeypatch.setattr(
        "inject_rules.integrations.http.fetcher.urlopen",
        lambda url, timeout=None: urlopen_calls.append(url),
    )
    # 実行
    run_hook(_payload())
    # 検証: ローカルの本文が取得元のパス付きで注入され、通信もキャッシュも発生しない
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "ローカルの命名規約" in output["additionalContext"]
    assert str(rule_path) in output["additionalContext"]
    assert urlopen_calls == []
    assert not hook_dirs.cache.exists() or list(hook_dirs.cache.glob("*.txt")) == []


def test_normal_when_cache_valid(monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook):
    """キャッシュだけで完結し、取得を発生させない（正常系）。"""
    # 準備: 索引とルール本文が有効期限内で存在する
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    write_cache(INDEX_URL, rule_index([(A_REL, ["**/*.py"])]), cache_dir=hook_dirs.cache)
    write_cache(A, "キャッシュ済みの本文", cache_dir=hook_dirs.cache)
    fetch = fetch_stub({})
    _install_fetch(monkeypatch, fetch)
    # 実行
    run_hook(_payload())
    # 検証: HTTP 取得が 1 度も発生しない
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "キャッシュ済みの本文" in output["additionalContext"]
    assert fetch.calls == []


def test_normal_when_over_limit(monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook):
    """収まる分だけ送り、続きの位置を記録して差し戻す（正常系）。"""
    # 準備: 上限を超えるサイズのルール本文
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A_REL, ["**/*.py"])]), A: "あ" * 20000})
    _install_fetch(monkeypatch, fetch)
    # 実行
    run_hook(_payload())
    # 検証
    response = _response(capsys)
    assert response["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert len(response["hookSpecificOutput"]["additionalContext"]) <= CHAR_LIMIT
    assert "残り 1" in response["systemMessage"]
    state = load_state(SESSION, base_dir=hook_dirs.session)
    assert state.offset_of(A) > 0
    assert state.is_injected(A) is False
    # 検証: 次回の呼び出しで持ち越し分の HTTP 取得が発生しない
    calls_after_first = list(fetch.calls)
    run_hook(_payload())
    capsys.readouterr()
    assert fetch.calls == calls_after_first


def test_normal_when_partial_continued(
    monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook
):
    """記録した位置から残りを送って実行を許可する（正常系）。"""
    # 準備: 当該ルールの続きの位置が記録済み
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    state = SessionState()
    state.mark_partial(A, 100)
    save_state(SESSION, state, base_dir=hook_dirs.session)
    _install_fetch(
        monkeypatch,
        fetch_stub({INDEX_URL: rule_index([(A_REL, ["**/*.py"])]), A: "あ" * 100 + "い" * 200}),
    )
    # 実行
    run_hook(_payload())
    # 検証: 前回の続きから始まる
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "い" * 200 in output["additionalContext"]
    assert "あ" not in output["additionalContext"]
    restored = load_state(SESSION, base_dir=hook_dirs.session)
    assert restored.is_injected(A) is True
    assert restored.offset_of(A) == 0


def test_normal_when_no_match(monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook):
    """何も出力せず終了する（正常系）。"""
    # 準備: 編集対象にマッチしない glob だけを返す索引
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A_REL, ["**/*.md"])]), A: "命名規約の本文"})
    _install_fetch(monkeypatch, fetch)
    # 実行
    run_hook(_payload())
    # 検証: ルール本文の取得が発生しない
    assert _response(capsys) is None
    assert fetch.calls == [INDEX_URL]


def test_normal_when_already_injected(
    monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook
):
    """全ルールが注入済みのため何も出力せず終了する（正常系）。"""
    # 準備: 当該ルールが注入済みとして記録済み
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    state = SessionState()
    state.mark_injected(A)
    save_state(SESSION, state, base_dir=hook_dirs.session)
    fetch = fetch_stub({INDEX_URL: rule_index([(A_REL, ["**/*.py"])]), A: "命名規約の本文"})
    _install_fetch(monkeypatch, fetch)
    # 実行
    run_hook(_payload())
    # 検証
    assert _response(capsys) is None
    assert fetch.calls == [INDEX_URL]


def test_error_when_indexes_unset(monkeypatch, capsys, hook_dirs, run_hook):
    """ログを 1 回出して何も注入しない（異常系）。"""
    # 準備: 注入元を未設定にする
    monkeypatch.delenv("INJECT_RULES_INDEXES", raising=False)
    logs = _record_logs(monkeypatch, "inject_rules.main.emit_log")
    # 実行
    run_hook(_payload())
    # 検証
    assert _response(capsys) is None
    assert len(logs) == 1
    # 検証: 同一セッションの 2 回目では送出されない
    run_hook(_payload())
    assert len(logs) == 1


def test_error_when_index_missing(monkeypatch, capsys, hook_dirs, fetch_stub, run_hook):
    """ログを 1 回出して何も注入しない（異常系）。"""
    # 準備: 索引の取得を失敗させ、キャッシュも持たない
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    _install_fetch(
        monkeypatch, fetch_stub({}, errors={INDEX_URL: urllib.error.URLError("見つかりません")})
    )
    logs = _record_logs(monkeypatch, "inject_rules.main.emit_log")
    # 実行
    run_hook(_payload())
    # 検証: 取得先 URL を含むログが 1 件送出される
    assert _response(capsys) is None
    assert len(logs) == 1
    assert INDEX_URL in logs[0]["attributes"]["index_locations"]
    # 検証: 同一セッションの 2 回目では送出されない
    run_hook(_payload())
    assert len(logs) == 1


def test_error_when_index_fetch_failed_with_cache(
    monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook
):
    """期限切れキャッシュを継続利用する（異常系）。"""
    # 準備: 期限切れの索引キャッシュを持ち、索引の取得は接続エラーになる
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    write_cache(INDEX_URL, rule_index([(A_REL, ["**/*.py"])]), cache_dir=hook_dirs.cache)
    _expire_cache(hook_dirs.cache)
    _install_fetch(
        monkeypatch,
        fetch_stub({A: "命名規約の本文"}, errors={INDEX_URL: urllib.error.URLError("接続不可")}),
    )
    logs = _record_logs(monkeypatch, "inject_rules.integrations.cache.store.emit_log")
    # 実行
    run_hook(_payload())
    # 検証
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "命名規約の本文" in output["additionalContext"]
    assert len(logs) == 1
    # 検証: 索引キャッシュが破棄されていない
    assert read_cache(INDEX_URL, cache_dir=hook_dirs.cache, ttl_sec=CACHE_TTL_SEC) is not None


def test_error_when_rule_fetch_failed(
    monkeypatch, capsys, hook_dirs, rule_index, fetch_stub, run_hook
):
    """該当ルールだけ送らず、次回に持ち越す（異常系）。"""
    # 準備: マッチする 2 件のうち片方の本文が存在しない
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    _install_fetch(
        monkeypatch,
        fetch_stub(
            {INDEX_URL: rule_index([(A_REL, ["**/*.py"]), (B_REL, ["**/*.py"])]), A: "取得できた本文"},
            errors={B: urllib.error.URLError("見つかりません")},
        ),
    )
    logs = _record_logs(monkeypatch, "inject_rules.main.emit_log")
    # 実行
    run_hook(_payload())
    # 検証
    output = _response(capsys)["hookSpecificOutput"]
    assert output["permissionDecision"] == "allow"
    assert "取得できた本文" in output["additionalContext"]
    assert B not in output["additionalContext"]
    assert load_state(SESSION, base_dir=hook_dirs.session).is_injected(B) is False
    # 検証: 取得先 URL を含むログが送出される
    assert len(logs) == 1
    assert logs[0]["attributes"]["rule_location"] == B
