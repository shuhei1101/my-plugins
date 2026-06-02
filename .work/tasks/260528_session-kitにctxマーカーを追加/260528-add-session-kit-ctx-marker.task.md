# PR150 — add-session-kit-ctx-marker

## 概要

注入フックの「1 セッション 1 ファイル 1 回ブロック」トークンは `/compact` や `/clear` でコンテキストが消えても session_id が同じだと再注入されないバグがある（PR149 の議論）。これを直すため、コンテキストのリセット世代を表すマーカーを管理する新プラグイン `session-kit` を新設する。session-kit は `PreCompact` と `SessionStart(source=clear)` で `/tmp/claude-session-ctx-gen-{session_id}` を touch するだけ。py-kit/next-kit のフックは per-file トークンとマーカーの mtime を比較し、マーカーが新しければ再注入する。session-kit 未インストール時（マーカー無し）は現状の once-per-session にグレースフルフォールバック。連携はファイルパス規約のみで、クロスプラグインのスクリプト呼び出しはしない。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #147 | py-kit/next-kit 注入フックの本文削除・絶対パス化 |
| #149 | hook-creator に注入パターンを文書化（Caution 3 をこの PR で発展） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260528_add-session-kit-ctx-marker/PR150/QA.md` |
| 済 | session-kit プラグイン新設（plugin.json / hooks.json / ctx_marker.py / CLAUDE.md / CLAUDE.jp.md） | - `plugins/session-kit/**` |
| 済 | py-kit inject_references.py をマーカー比較ロジックに改修 + 版上げ | - `plugins/py-kit/hooks/inject_references.py`, `plugins/py-kit/.claude-plugin/plugin.json` |
| 済 | next-kit inject_references.py をマーカー比較ロジックに改修 + 版上げ | - `plugins/next-kit/hooks/inject_references.py`, `plugins/next-kit/.claude-plugin/plugin.json` |
| 済 | hooks.md / hooks.jp.md の Caution 3 を世代マーカー方式に更新 + claude-kit 版上げ | - `plugins/claude-kit/references/hooks.{md,jp.md}`, `plugins/claude-kit/.claude-plugin/plugin.json` |
| 済 | py-kit CLAUDE.md/jp に session-kit 連携を追記 | - `plugins/py-kit/CLAUDE.md`, `plugins/py-kit/CLAUDE.jp.md` |
| 済 | marketplace.json に session-kit 追加 + 各版反映 | - `.claude-plugin/marketplace.json` |
| 済 | フック動作を検証（once-per-session / compact 後再注入 / clear 後再注入 / フォールバック） | - py-kit・next-kit 両方で確認 |

## 参考ドキュメント

- `.claude/references/incidents/injection-hook-full-body-bloat.md`: 注入フックの設計教訓
- `plugins/claude-kit/references/hooks.md`: Caution 3（更新対象）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |

## QA

なし
