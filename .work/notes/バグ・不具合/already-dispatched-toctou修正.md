# already_dispatched_this_session() TOCTOU修正

## 概要

`_common.py` の `already_dispatched_this_session()` が `exists()` + `touch()` の非原子的 check-then-act パターンを持っており、並列プロセスが同時に同じフラグファイルを作成しようとした場合に「セッション 1 回だけ発火」の保証が破れる TOCTOU 競合があった。

## 修正内容

`flag.open("x")` による排他的ファイル生成に置き換えた。`open("x")` は既存ファイルがある場合に `FileExistsError` を送出するため、check と create が原子的な 1 操作になる。

```python
# 修正後
def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    try:
        flag.open("x").close()  # 排他的作成: 既存なら FileExistsError
        return False
    except FileExistsError:
        return True
```

## 適用ファイル

| ファイル | 役割 |
|---|---|
| `plugins/ref-inject/templates/hooks/scripts/_common.py` | テンプレート（先に修正） |
| `plugins/claude-kit/hooks/scripts/_common.py` | キット版 |
| `plugins/dev-kit/hooks/scripts/_common.py` | キット版 |
| `plugins/work/hooks/scripts/_common.py` | キット版 |

## 注意

`git-guard.py` / `master-commit-guard.py` の同様パターンは ISSUE-096 で別管理。本修正のスコープ外。

## 変更履歴

| 日付 | 内容 |
|---|---|
| 2026-06-02 | ISSUE-094 対応: `already_dispatched_this_session()` を `open("x")` 排他生成に修正 |
