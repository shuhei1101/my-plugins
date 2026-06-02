# ISSUE-092: `read_hook_input()` が例外をキャッチせず、不正な stdin でフックがクラッシュする

**作成日**: 2026-05-31

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`_common.py` の `read_hook_input()` が `json.loads` の例外を捕捉しないため、不正な stdin でフックプロセスがクラッシュし、ユーザーのセッションが妨害されうる。

## 背景

Claude Code はフックのクラッシュをエラーとして扱う。特に `PreToolUse` フックがクラッシュすると、ツール呼び出し自体がブロックされる可能性がある。`_common.py` はテンプレートヘルパーであり、ここに欠陥があると生成される全フックスクリプトに伝播する。

## 現状

`_common.py` の `read_hook_input()` は以下のように実装されている:

```python
def read_hook_input() -> dict:
    return json.loads(sys.stdin.read())
```

`json.loads` は stdin が空文字列・不正 JSON・EOF のときに `json.JSONDecodeError` を送出する。この例外は呼び出し元でキャッチされていないため、フックプロセスが非ゼロ終了コードでクラッシュする。

この `read_hook_input()` は以下の全フックスクリプトから呼ばれている:

| No | ファイル | 使用箇所 |
|---|---|---|
| 1 | `plugins/claude-kit/hooks/scripts/references_edit_guard.py` | `data = read_hook_input()` |
| 2 | `plugins/dev-kit/hooks/scripts/references_edit_guard.py` | 〃 |
| 3 | `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` | 〃 |
| 4 | `plugins/work/hooks/scripts/stop.py` | 〃 |

なお `inject_references.py` 各版は `read_hook_input()` を使わず直接 `json.loads(sys.stdin.read())` を呼んでいるが、そちらは try/except で包まれている（問題なし）。`git-guard.py` と `master-commit-guard.py` も直接呼び出しで未保護（ISSUE-096 として分離）。

## 原因

問題の核心は **`_common.py` というテンプレートヘルパー自身に例外処理がない**ことで、テンプレートから生成される全フックスクリプトに同じ欠陥が伝播している。

## 期待される状態

`read_hook_input()` が stdin のパース失敗時に fail-open（空 dict を返す）で振る舞い、不正入力でもフックがクラッシュせずに静かに終了する。修正が全 `_common.py` コピーに反映されている。

## 対応案

`read_hook_input()` 内で例外を捕捉し、失敗時は空 dict を返してフックを静かに終了させる（fail-open）:

```python
def read_hook_input() -> dict:
    """フック入力 JSON を標準入力から読み込む。パースに失敗した場合は空 dict を返す。"""
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}
```

この修正を `_common.py` の全コピー（`plugins/claude-kit/`, `plugins/dev-kit/`, `plugins/work/`, `plugins/ref-inject/templates/`）に適用する。テンプレート (`ref-inject/templates/`) を先に直し、キット版は手動で同期する。

## 横展開

`git-guard.py` / `master-commit-guard.py` も同様の直接 `json.loads` 呼び出しで未保護 (ISSUE-096 参照)。今後 `_common.py` に追加するヘルパーは同じ fail-open ポリシーを守ること。


