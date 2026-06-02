---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-096: `git-guard.py` / `master-commit-guard.py` が stdin パースエラーをキャッチしない

**作成日**: 2026-05-31

## 問題

`plugins/work/hooks/scripts/git-guard.py` と `master-commit-guard.py` は `json.loads(sys.stdin.read())` を直接呼び出しており、例外処理がない:

```python
# git-guard.py, line 41
payload = json.loads(sys.stdin.read())

# master-commit-guard.py, line 57
payload = json.loads(sys.stdin.read())
```

stdin が空文字列・不正 JSON・EOF の場合、`json.JSONDecodeError` がキャッチされないままフックプロセスがクラッシュする（非ゼロ終了コード）。これらは `PreToolUse(Bash)` フックであるため、すべての Bash ツール呼び出し（`git push` / `git merge` / `git commit` を含む）の直前に発火する。クラッシュによって **Bash ツールがブロックされる**可能性がある。

`inject_references.py` は同様の `json.loads` 呼び出しを try/except で保護しているのに対し、ガードスクリプト 2 本は保護されていない（`_common.py` 経由でも `read_hook_input()` 自体が未保護のため、どちらの経路でも問題は同じ — ISSUE-092 参照）。

| No | ファイル | 呼び出し行 |
|---|---|---|
| 1 | `plugins/work/hooks/scripts/git-guard.py` | line 41 |
| 2 | `plugins/work/hooks/scripts/master-commit-guard.py` | line 57 |

## 修正案

両スクリプトの `json.loads` を try/except で包み、失敗時は fail-open で早期リターンする:

```python
# git-guard.py
try:
    payload = json.loads(sys.stdin.read())
except Exception:
    return  # stdin 不正 → fail-open

# master-commit-guard.py
try:
    payload = json.loads(sys.stdin.read())
except Exception:
    return  # stdin 不正 → fail-open
```

または、`_common.py` の `read_hook_input()` を修正（ISSUE-092）した上で、両スクリプトもそれを使うようにリファクタリングする（現在これらは `_common` を import していない）。

## 水平展開

将来 work プラグインに Bash PreToolUse フックを追加する場合は、必ず stdin パース部分を try/except で保護すること。Bash PreToolUse のクラッシュは git 操作をブロックするため影響が大きい。
