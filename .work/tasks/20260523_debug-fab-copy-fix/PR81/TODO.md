# PR81 — debug-fab-copy-fix

## 概要

debug-fab ウィジェットで要素を選択してコピーボタンを押しても、特定条件でコピーが動作しないバグを修正する。
あわせて `debug-fab-modify` スキルの日本語ミラー（SKILL.jp.md）が存在しない問題も対処する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/20260523_debug-fab-copy-fix/PR81/QA.md` |
| - | `.work/specs/` の仕様書を更新する | `.work/specs/debug-fab.md` |
| - | uidev.js のコピー処理バグを修正する | `plugins/ui-kit/skills/debug-fab/templates/uidev.js` |
| - | SKILL.md のオペレーション記述を実装と同期する | `plugins/ui-kit/skills/debug-fab/SKILL.md` |
| - | templates/CLAUDE.md のオペレーション表を更新する | `plugins/ui-kit/skills/debug-fab/templates/CLAUDE.md` |
| - | debug-fab-modify に SKILL.jp.md を追加する | `plugins/ui-kit/skills/debug-fab-modify/SKILL.jp.md` |
| - | バージョンを PATCH バンプする | `plugins/ui-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する | - |

## 参考ドキュメント

- `.work/specs/ui-kit.md`: ui-kit プラグイン全体の仕様（debug-fab セクション含む）

## 次PR候補

| タイトル | 概要 |
|---|---|
| debug-fab コピー失敗時にリトライ可能にする | copy 失敗時に stop() を呼ばず選択状態を保持し再試行できるようにする |
