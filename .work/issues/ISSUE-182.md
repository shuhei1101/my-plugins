# ISSUE-182: dev-kit _common.py の read_hook_input() に stdin パースエラーハンドリングがない（ISSUE-165 横展開）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/hooks/scripts/_common.py` の `read_hook_input()` が stdin の JSON パースエラーを捕捉せず、呼び出し元へ例外を伝播させる。これは ISSUE-165（claude-kit 側の同一問題）の横展開。

```python
def read_hook_input() -> dict:
    return json.loads(sys.stdin.read())
```

`references_edit_guard.py` は `read_hook_input()` を try/except なしで直呼びしているため、不正な stdin が渡ると未捕捉の `json.JSONDecodeError` が発生し、フックが異常終了する。

## 対応方針

`read_hook_input()` 内部で例外を捕捉し、パース失敗時は空辞書を返す。ISSUE-165（claude-kit）と同一の修正を適用し、両キットを同期させる。

```python
def read_hook_input() -> dict:
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}
```

## 対象ファイル

- `plugins/dev-kit/hooks/scripts/_common.py`: `read_hook_input()` に try/except を追加
