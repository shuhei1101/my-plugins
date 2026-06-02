---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-093: `stop.py` が `sys.argv[1]` を無防備に参照し、引数欠落で IndexError クラッシュ

**作成日**: 2026-05-31

## 問題

`plugins/work/hooks/scripts/stop.py` の `main()` は次のように `sys.argv[1]` を直接参照している:

```python
prompts_dir = pathlib.Path(sys.argv[1]).parent
```

`hooks.json` では `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/stop.md` が引数として渡されるため、通常は問題ない。しかし以下のシナリオで `IndexError: list index out of range` が発生し、フックプロセスがクラッシュする:

- 開発・デバッグ時にスクリプトを直接 `python stop.py` で実行した場合
- `hooks.json` の `args` が誤って空になった、または `${CLAUDE_PLUGIN_ROOT}` の展開に失敗した場合
- テンプレートを別プラグインへ移植する際に `args` の記述を忘れた場合

Stop フックのクラッシュは**ユーザーへの「タスク更新」リマインダーが届かなくなる**副作用に加え、Claude Code が Stop フックエラーを記録してユーザーに通知するため、セッション終了のたびに赤いエラーメッセージが出る可能性がある。

`references_edit_guard.py`（claude-kit / dev-kit / ref-inject テンプレート）も同じパターンで `pathlib.Path(sys.argv[1])` を使用しているが、こちらは `emit_block_reason()` 内で `prompt_path.exists()` をチェックして early return するため、`IndexError` 発生前にクラッシュする点は共通している。

## 修正案

`sys.argv` の長さを確認してから参照する:

```python
def main() -> None:
    if not env_truthy("WORK_STOP_REMINDER", default=True):
        return

    data = read_hook_input()
    exit_if_stop_loop(data)

    if len(sys.argv) < 2:
        return  # 引数なし: fail-open で静かに終了
    prompts_dir = pathlib.Path(sys.argv[1]).parent
    ...
```

同様のパターンを使う `references_edit_guard.py`（claude-kit / dev-kit / ref-inject テンプレート）も `len(sys.argv) < 2` ガードを追加する。

## 水平展開

`hooks.json` の `args` に依存するすべてのフックスクリプトに同様のリスクがある。新規スクリプト追加時は `sys.argv` アクセス前に長さチェックを必ず入れること。
