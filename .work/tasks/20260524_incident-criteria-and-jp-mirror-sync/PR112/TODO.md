# PR112 — incident-criteria-and-jp-mirror-sync

## 概要

インシデントの判定基準（conversation-to-claude SKILL）が実態とずれており、「PRで対応した作業内容」をインシデントとして記録するケースが発生していた。
また incidents.md / glossary.md の JP ミラーが英語版と同期されていない問題があり、同期を強制するルールも存在しなかった。
本PRでは判定基準の修正・JP ミラー同期ルールの追加・既存 JP ミラーの同期を行う。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260524_incident-criteria-and-jp-mirror-sync/PR112/QA.md` |
| 済 | conversation-to-claude SKILL.md のインシデント判定基準を修正 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | conversation-to-claude SKILL.jp.md も同様に修正 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | incidents / glossary の JP ミラー同期ルールを追加 | - `.claude/rules/feature/incidents-glossary-jp-mirror-sync.md` |
| 済 | JP ミラー同期ルール（rules-jp にも配置） | - `.claude/rules-jp/feature/incidents-glossary-jp-mirror-sync.md` |
| 済 | rules-jp/core/incidents.md を英語版に同期（不足エントリ追加） | - `.claude/rules-jp/core/incidents.md` |
| 済 | rules-jp/core/glossary.md を英語版に同期（不足エントリ追加） | - `.claude/rules-jp/core/glossary.md` |
| 済 | plugin.json / marketplace.json バージョンバンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/incident-criteria.md`: インシデント判定基準ノート
- `.claude/rules/core/incidents.md`: インシデントインデックス（英語本体）
- `.claude/rules-jp/core/incidents.md`: JP ミラー（同期対象）
- `.claude/rules/core/glossary.md`: 用語集（英語本体）
- `.claude/rules-jp/core/glossary.md`: JP ミラー（同期対象）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| incident-glossary-content-cleanup | 既存インシデント・用語集の内容精査（PRの作業内容が混入しているエントリの削除・修正） | 即時実施可 |
