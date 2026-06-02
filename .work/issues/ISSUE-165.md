# ISSUE-165: _common.py の read_hook_input() にエラーハンドリングがなく stdin パースエラーが未捕捉

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/hooks/scripts/_common.py` の `read_hook_input()` は `json.loads(sys.stdin.read())` を try/except なしで呼び出す。stdin が空またはマルフォームな JSON だった場合、`json.JSONDecodeError` が呼び出し元まで伝播する。`references_edit_guard.py` は `read_hook_input()` を try/except なしで呼び出しているため、例外はスクリプト全体のクラッシュになりうる。

一方 `inject_references.py` には独自の try/except があり、共通ヘルパーには同等の保護が存在しない。

```python
# _common.py（保護なし）
def read_hook_input() -> dict:
    return json.loads(sys.stdin.read())
```

## 対応方針

`read_hook_input()` 内に try/except を追加し、失敗時は stderr 出力 + 空 dict 返却とする。

```python
def read_hook_input() -> dict:
    try:
        return json.loads(sys.stdin.read())
    except Exception as e:
        print(f"[claude-kit] stdin parse error: {e}", file=sys.stderr)
        return {}
```

## 対象ファイル

- `plugins/claude-kit/hooks/scripts/_common.py`: `read_hook_input()` に try/except を追加

## QA

### QA-1: 失敗時の挙動

A) 空 dict を返す（呼び出し元が `None` チェック不要） / B) `sys.exit(0)` で fail-open / C) 呼び出し元側で try/except

**推奨**: A

**回答**: <!-- A / B / C -->
