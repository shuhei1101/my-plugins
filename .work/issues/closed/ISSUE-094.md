# ISSUE-094: `already_dispatched_this_session()` の check-then-touch が TOCTOU 競合を持つ

**作成日**: 2026-05-31

## 概要

`_common.py` の `already_dispatched_this_session()` が `exists()` 確認と `touch()` の間に TOCTOU 競合を持ち、並列実行時に「セッション 1 回だけ発火」の保証が破れる。

## 背景

Claude Code は複数の並列エージェントや並列フックを起動する（例: `work:issue-scan` が複数の `issue-scanner` サブエージェントを同時実行）。セッション単位で 1 回だけ発火させたい guard フックがこの関数に依存している。

## 現状

`already_dispatched_this_session()` は以下の実装:

```python
def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    if flag.exists():
        return True
    flag.touch()
    return False
```

`flag.exists()` の True 確認と `flag.touch()` の間に別プロセスが同じフラグファイルを作成できる（TOCTOU: Time-Of-Check to Time-Of-Use）。両プロセスが `flag.exists()` を `False` と判定して両方とも `False` を返す可能性がある。結果として guard フック（`references_edit_guard.py` 等）が同一セッションで複数回発火し、重複した `decision: block` インジェクションでコンテキストが汚染される。

影響ファイル:

| No | ファイル | 呼び出し元 |
|---|---|---|
| 1 | `plugins/claude-kit/hooks/scripts/_common.py` | `references_edit_guard.py` |
| 2 | `plugins/dev-kit/hooks/scripts/_common.py` | 〃 |
| 3 | `plugins/work/hooks/scripts/_common.py` | （将来追加されるフックでの利用を含む）|
| 4 | `plugins/ref-inject/templates/hooks/scripts/_common.py` | テンプレート |

## 原因

`exists()` チェックとファイル作成（`touch()`）が分離した非原子的な check-then-act になっており、その間に他プロセスが割り込める窓が開いている。

## 期待される状態

フラグファイルの生成が原子的に行われ、並列プロセスのうち 1 つだけが「未発火（`False`）」を得る。修正が全 `_common.py` コピーに反映されている。

## 対応案

`flag.touch()` に `exist_ok=False` 相当の排他的生成を使い、`FileExistsError` を例外として扱うことで原子的に判定する:

```python
def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    try:
        flag.open("x").close()  # 排他的作成: 既存なら FileExistsError
        return False
    except FileExistsError:
        return True
```

`open("x")` モードは原子的なファイル生成を保証し、ファイルが既に存在する場合は `FileExistsError` を送出する。これにより check-then-act の窓が閉じる。全 `_common.py` コピーに同様の修正を適用すること。

## 横展開

`git-guard.py` / `master-commit-guard.py` も同じ check-then-touch パターンでトークンファイルを管理しているが、こちらは「1 回ブロックしたら次は通す」仕様のため TOCTOU の影響は軽微（重複ブロックが起きるだけ）。それでも同じ修正を適用することを推奨する。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する
