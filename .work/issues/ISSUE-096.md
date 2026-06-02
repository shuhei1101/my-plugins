# ISSUE-096: `git-guard.py` / `master-commit-guard.py` が stdin パースエラーをキャッチしない

**作成日**: 2026-05-31

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

## QA

### QA-1: stdin パース保護の実装方式

A) 各スクリプトに個別 try/except を追加（局所的・重複あり） / B) `read_hook_input()` に集約してリファクタ（一貫・ISSUE-092 に依存）

**推奨**: B — ISSUE-092 で `read_hook_input()` を fail-open 化するなら、両スクリプトもそれを使う方が例外処理を 1 箇所に集約でき一貫する。

- [ ] A
- [x] B

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`git-guard.py` と `master-commit-guard.py` が `json.loads(sys.stdin.read())` を例外処理なしで直接呼び出しており、不正な stdin でフックがクラッシュして Bash ツールがブロックされうる。

## 背景

これらは `PreToolUse(Bash)` フックであり、すべての Bash ツール呼び出し（`git push` / `git merge` / `git commit` を含む）の直前に発火する。クラッシュの影響範囲が大きい。

## 現状

両スクリプトは `json.loads(sys.stdin.read())` を直接呼び出しており、例外処理がない:

```python
# git-guard.py, line 41
payload = json.loads(sys.stdin.read())

# master-commit-guard.py, line 57
payload = json.loads(sys.stdin.read())
```

stdin が空文字列・不正 JSON・EOF の場合、`json.JSONDecodeError` がキャッチされないままフックプロセスがクラッシュする（非ゼロ終了コード）。`inject_references.py` は同様の `json.loads` 呼び出しを try/except で保護しているのに対し、ガードスクリプト 2 本は保護されていない（`_common.py` 経由でも `read_hook_input()` 自体が未保護のため、どちらの経路でも問題は同じ — ISSUE-092 参照）。

| No | ファイル | 呼び出し行 |
|---|---|---|
| 1 | `plugins/work/hooks/scripts/git-guard.py` | line 41 |
| 2 | `plugins/work/hooks/scripts/master-commit-guard.py` | line 57 |

## 原因

stdin パース部分が try/except で保護されておらず、不正入力時の fail-open 経路が存在しない。

## 期待される状態

両ガードスクリプトが stdin パース失敗時に fail-open で早期リターンし、不正入力でも Bash ツールをブロックしない。

## 対応案

| 案 | 内容 | メリット | デメリット |
|---|---|---|---|
| A | 両スクリプトの `json.loads` を個別に try/except で包む | 局所的で他への影響なし、即座に適用可 | fail-open ロジックが 2 箇所に重複する |
| B | ISSUE-092 で `read_hook_input()` を fail-open 化した上で、両スクリプトもそれを使うようリファクタ | 例外処理が 1 箇所に集約され一貫する | ISSUE-092 の対応に依存、両スクリプトの `_common` import 追加が必要 |

```python
# 案 A
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

**推奨: 案B**

## 横展開

将来 work プラグインに Bash PreToolUse フックを追加する場合は、必ず stdin パース部分を try/except で保護すること。Bash PreToolUse のクラッシュは git 操作をブロックするため影響が大きい。


