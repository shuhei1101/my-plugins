# PR149 — hook-creator-reference-injection-pattern

## 概要

PR147 で扱った「j2 テンプレートによる reference 自動注入フック」（PreToolUse(Edit/Write/MultiEdit/Read) で対象ファイルに応じたドキュメントを注入する構造）を hook-creator スキルに反映する。py-kit/next-kit の実装で得た 3 つの注意点を必ず明記する: ① 本文全量ではなく path + description のポインタを注入し Claude に Read させる、② 注入パスは絶対パス（`${CLAUDE_PLUGIN_ROOT}` は注入テキストで展開されない）、③ セッション + ファイルハッシュトークンで 1 セッション 1 ファイル 1 回だけブロック。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #147 | py-kit/next-kit 注入フックの本文削除・絶対パス化（このパターンの実装元） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260528_hook-creator-reference-injection-pattern/PR149/QA.md` |
| 済 | hooks.md に reference 自動注入パターン + 3 注意点を追記 | - `plugins/claude-kit/references/hooks.md` |
| 済 | hooks.jp.md に JP ミラーを反映 | - `plugins/claude-kit/references/hooks.jp.md` |
| 済 | SKILL.md の Hook patterns にパターン参照を追記 | - `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | SKILL.jp.md に JP ミラーを反映 | - `plugins/claude-kit/skills/hook-creator/SKILL.jp.md` |
| 済 | claude-kit バージョンを MINOR バンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/py-kit/hooks/inject_references.py`: パターンの実装元（canonical example）
- `.claude/references/incidents/injection-hook-full-body-bloat.md`: 注意点の根拠 incident

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |

## QA

なし
