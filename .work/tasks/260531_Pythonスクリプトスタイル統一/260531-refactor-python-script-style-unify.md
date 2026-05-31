# refactor/python-script-style-unify

> 内部 ID: 249（index.yaml 採番用 — クロスリファレンス目的）

## 概要

my-plugins 内の全 Python スクリプトを `dev-kit/references/python/scripts/python-script.md` に準拠させる。
主な問題点はコメント・ログメッセージが英語のまま残っている箇所、および logger 未使用・`main()` 未定義などの構造上の逸脱。

対象スクリプト（22 ファイル）:
- `plugins/work/scripts/` — index-tool, issue-tool, setup-task, trim-index
- `plugins/work/hooks/scripts/` — git-guard, inject_references, master-commit-guard, stop, user-prompt-submit, _common
- `plugins/claude-kit/scripts/` — apply-statusline
- `plugins/claude-kit/hooks/scripts/` — inject_references, references_edit_guard, _common
- `plugins/ref-inject/templates/hooks/scripts/` — inject_references, references_edit_guard, _common
- `plugins/dev-kit/hooks/scripts/` — inject_references, references_edit_guard, ts_check, _common
- `plugins/work/skills/setup/scripts/` — setup

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | `## QA` に未決事項を記録する |
| 2 | - | `.work/notes/` のノートを更新する |
| 3 | - | 各 Python ファイルをリファレンスと照合し、違反箇所を特定する |
| 4 | - | コメント・ログメッセージを日本語に統一する |
| 5 | - | 構造上の違反（logger/print・argparse・main()等）を修正する |
| 6 | - | CLAUDE.md / ルール類を更新する |

## 変更内容

実装後に記入する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | （実装後に記入） | - | - | - |

## テスト

テスト変更なし（スタイル修正のみ）。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | - | - |

## QA

### QA-001: フックスクリプトへの python-script リファレンス適用範囲

**背景**: `python-script.md` は「単一ファイルスクリプト（argparse / main()）」向けのテンプレート。フックスクリプトは stdin から JSON を読む独自の構造を持ち、`argparse` や `main()` は不要。どこまでリファレンスを適用すべきか。

| # | 案 | 内容 |
|---|---|---|
| 1 | A | コメント・ログ日本語化のみを全ファイルに適用。argparse/main() 等の構造要件はフックには適用しない |
| 2 | B | リファレンスを完全適用。フックにも argparse / main() を追加する |

**推奨方式**: A — フックスクリプトは Claude Code ハーネスが stdin で呼び出す特殊なエントリポイントであり、argparse や main() を追加すると動作が変わる。コメント・ログの日本語化のみを全ファイルに適用する。

**状態**: 解決済み（A を採用）

**決定したら反映先**: 作業内容 #5

## 参考ドキュメント

- `plugins/dev-kit/references/python/scripts/python-script.jp.md`: Python スクリプト標準テンプレート（日本語ミラー）
- `.work/notes/Pythonスクリプトスタイル規約.md`: my-plugins 向け適用方針（通常スクリプトとフックの使い分け）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/add-japanese-comment-log-rule | 260530 — Pythonコメント日本語化ルール追加（前提作業） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
