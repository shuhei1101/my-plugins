# ISSUE-146: references_edit_guard.py が CLAUDE_PLUGIN_ROOT を使わず parents[2] のみでルートを解決

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` はプラグインルートを `pathlib.Path(__file__).resolve().parents[2]` のみで解決している。

```python
plugin_root = pathlib.Path(__file__).resolve().parents[2]
```

一方、同じディレクトリの `inject_references.py` は `CLAUDE_PLUGIN_ROOT` 環境変数を優先し、フォールバックとして `parents[2]` を使う `_plugin_root()` 関数を持っている。

```python
def _plugin_root() -> pathlib.Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return pathlib.Path(env)
    return pathlib.Path(__file__).resolve().parents[2]
```

インシデント 24 (`claude-plugin-root-unset-manual-steps`) の通り、スキル手順を Bash ツールで手動実行する場合は `CLAUDE_PLUGIN_ROOT` が未設定で `parents[2]` フォールバックが必要になる。しかしシンボリックリンクや特殊な配置では `parents[2]` が正しいプラグインルートを指さないケースがある。`CLAUDE_PLUGIN_ROOT` が設定されているときはそれを優先する方が安全かつ一貫性がある。

## 対応方針

`references_edit_guard.py` の `plugin_root` 解決を `inject_references.py` と同じパターンに統一する。

```python
import os
# ...
plugin_root_env = os.environ.get("CLAUDE_PLUGIN_ROOT")
plugin_root = pathlib.Path(plugin_root_env) if plugin_root_env else pathlib.Path(__file__).resolve().parents[2]
```

消費者プラグイン（`claude-kit` / `dev-kit` / `work`）の `references_edit_guard.py` にも同じ変更が必要。`/ref-inject:plugin-migrate` で伝播可能。

## 対象ファイル

- `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py`: `plugin_root` 解決ロジックを修正

