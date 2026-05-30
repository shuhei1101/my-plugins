# PR12 — hook-creator-stop-note

## 概要

Stop フックのプロンプトは `reason` 経由でユーザーの画面に直接表示されるため短くすべき旨を hook-creator スキルに追記。
あわせて work-kit の UserPromptSubmit フックを `stdin.read + decision:block` パターンに変更（Stop フックと同形式に統一）。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | Stop フックプロンプトは短くする旨を注意に追記 | - `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`<br>- `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | claude-kit バージョンを 3.4.0 → 3.4.1 に PATCH バンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | UserPromptSubmit フックを decision:block パターンに変更 | - `plugins/work-kit/hooks/hooks.json` |

## 参考ドキュメント

- `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`: hook-creator スキル定義

## QA

なし
