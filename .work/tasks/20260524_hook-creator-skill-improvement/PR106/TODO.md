# PR106 — hook-creator-skill-improvement

## 概要

hook-creator SKILL.md の 3 点を改善する:
1. UserPromptSubmit パターンを Stop フックと同じ "Read and follow: /path" 形式に統一
2. Plugin用・Project用の重複パターンを1本に統合し、差分はパス変数の注記のみにする
3. 既存フックを編集する場合（条件追加など）の使い方例を追加する

### 実施条件

即時実施可（PR105 とは独立）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR105 | ui-kit に UserPromptSubmit フック追加（同じ形式を採用）|

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | UserPromptSubmit パターンを "Read and follow" 形式に変更 | `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | Plugin/Project パターンを統合（パス変数の差分のみ注記） | `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | 編集例（既存フックへの条件追加）を References に追加 | `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | SKILL.jp.md を同内容で更新 | `plugins/claude-kit/skills/hook-creator/SKILL.jp.md` |
| 済 | claude-kit バージョンバンプ + changelog 追加 | `plugins/claude-kit/.claude-plugin/plugin.json` / `changelogs/` |
| 済 | marketplace.json 更新 | `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: "Read and follow" 形式の実装例

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | 即時実施可 |
