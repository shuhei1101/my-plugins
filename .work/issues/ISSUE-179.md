# ISSUE-179: pre-compact.py / user-prompt-submit.py の sys.argv[1] アクセスに IndexError ガードがない

**作成日**: 2026-06-02

## 問題

`pre-compact.py` と `user-prompt-submit.py` が `sys.argv[1]` に直接アクセスしているが、引数が渡されなかった場合の `IndexError` ガードがない。`stop.py` は `if len(sys.argv) < 2: return` でガードしているが、他の 2 ファイルは未対応。

通常は `hooks.json` の `args` に値が設定されるため問題ないが、インシデント #24（`claude-plugin-root-unset-manual-steps`）のように手動実行やテスト時に引数なしで起動されると `IndexError: list index out of range` でクラッシュする。

```python
# stop.py（ガードあり）
if len(sys.argv) < 2:
    return
# pre-compact.py（ガードなし）
emit_block_reason(pathlib.Path(sys.argv[1]))
# user-prompt-submit.py（ガードなし）
prompt_path = pathlib.Path(sys.argv[1])
```

## 対応方針

`stop.py` と同じ `len(sys.argv) < 2` チェックを `pre-compact.py` と `user-prompt-submit.py` の `sys.argv[1]` アクセス前に追加し、引数なし時は fail-open で静かに終了する。

## 対象ファイル

- `plugins/work/hooks/scripts/pre-compact.py`: `sys.argv[1]` アクセス前にガードを追加
- `plugins/work/hooks/scripts/user-prompt-submit.py`: 同上

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
