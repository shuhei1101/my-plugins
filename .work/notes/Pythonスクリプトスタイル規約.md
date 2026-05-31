---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成（refactor/python-script-style-unify）
  - 2026-05-31 — python-script.md リファレンス自体を修正（logger→print・scripts/ フォルダ構成）
related_specs:
  - plugins/dev-kit/references/python/scripts/python-script.jp.md
related_branches:
  - refactor/python-script-style-unify
---

# Python スクリプトスタイル規約 — my-plugins 内スクリプトの統一方針

## 概要

my-plugins プロジェクト内の全 Python スクリプトは `dev-kit/references/python/scripts/python-script.md` に準拠する。
最重要チェック項目はコメント・ログメッセージの日本語化。

## 適用範囲

### 通常スクリプト（`scripts/*.py`）

`python-script.md` の全必須要素を適用する:

1. モジュール docstring（1 行目に要約）
2. `from __future__ import annotations`
3. `argparse` でパース（即値ハードコード禁止）
4. `main() -> int` 関数化
5. `if __name__ == "__main__": sys.exit(main())`
6. `logger` 使用（`print` 禁止）
7. 例外処理（想定外は `logger.exception`）
8. **コメント・ログメッセージは日本語**

### フックスクリプト（`hooks/scripts/*.py`）

Claude Code ハーネスが stdin から JSON を渡して呼び出す特殊構造。
`argparse` / `main()` を追加すると動作が変わるため、構造要件は対象外とする。

適用する項目:
- **コメント・ログメッセージは日本語**
- モジュール docstring（概要記述）
- `from __future__ import annotations`
- `logger` / `print` の使い方（フックは stdout/stderr に直接出力するためケースバイケース）

## 対象ファイル一覧

| # | ファイル | 種別 |
|---|---|---|
| 1 | `plugins/work/scripts/index-tool.py` | 通常スクリプト |
| 2 | `plugins/work/scripts/issue-tool.py` | 〃 |
| 3 | `plugins/work/scripts/setup-task.py` | 〃 |
| 4 | `plugins/work/scripts/trim-index.py` | 〃 |
| 5 | `plugins/work/skills/setup/scripts/setup.py` | 〃 |
| 6 | `plugins/claude-kit/scripts/apply-statusline.py` | 〃 |
| 7 | `plugins/work/hooks/scripts/_common.py` | フック共通ライブラリ |
| 8 | `plugins/work/hooks/scripts/git-guard.py` | フック |
| 9 | `plugins/work/hooks/scripts/inject_references.py` | 〃 |
| 10 | `plugins/work/hooks/scripts/master-commit-guard.py` | 〃 |
| 11 | `plugins/work/hooks/scripts/stop.py` | 〃 |
| 12 | `plugins/work/hooks/scripts/user-prompt-submit.py` | 〃 |
| 13 | `plugins/claude-kit/hooks/scripts/_common.py` | フック共通ライブラリ |
| 14 | `plugins/claude-kit/hooks/scripts/inject_references.py` | フック |
| 15 | `plugins/claude-kit/hooks/scripts/references_edit_guard.py` | 〃 |
| 16 | `plugins/ref-inject/templates/hooks/scripts/_common.py` | テンプレート（フック共通ライブラリ） |
| 17 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` | テンプレート（フック） |
| 18 | `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` | 〃 |
| 19 | `plugins/dev-kit/hooks/scripts/_common.py` | フック共通ライブラリ |
| 20 | `plugins/dev-kit/hooks/scripts/inject_references.py` | フック |
| 21 | `plugins/dev-kit/hooks/scripts/references_edit_guard.py` | 〃 |
| 22 | `plugins/dev-kit/hooks/scripts/ts_check.py` | 〃 |
