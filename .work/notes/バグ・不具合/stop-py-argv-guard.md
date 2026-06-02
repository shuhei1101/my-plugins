# stop.py / references_edit_guard.py — sys.argv 長さガード

**対象ファイル**:
- `plugins/work/hooks/scripts/stop.py`
- `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py`（テンプレート）
- `plugins/claude-kit/hooks/scripts/references_edit_guard.py`
- `plugins/dev-kit/hooks/scripts/references_edit_guard.py`

## 問題

`sys.argv[1]` を長さチェックなしで参照していたため、引数欠落時に `IndexError: list index out of range` が発生しフックプロセスがクラッシュしていた。

## 修正

`sys.argv[1]` を参照する直前に fail-open ガードを追加:

```python
if len(sys.argv) < 2:
    return  # 引数なし: fail-open で静かに終了
```

`stop.py` では `exit_if_stop_loop(data)` の後（既存の early return 位置に合わせて）に挿入。`references_edit_guard.py` 3 コピーでは `emit_block_reason(pathlib.Path(sys.argv[1]))` の直前に挿入。

## 変更履歴

| # | 日付 | 内容 |
|---|---|---|
| 1 | 2026-06-02 | ISSUE-093 で修正（fix/stop-py-argv-guard） |
