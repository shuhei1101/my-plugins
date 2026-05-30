# PR108 — md-jp-mirror-hook

## 概要

`.md` ファイルを作成したとき、対応する `.jp.md` ミラーが存在しない場合に作成を促すフックを my-plugins ローカル設定に追加する。`/claude-kit:hook-creator` スキルで実装する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #106 | hook-creator スキルの改善（フック作成フロー整備） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| x | QA.md に未決定事項を記録する | - `.work/tasks/20260524_md-jp-mirror-hook/PR108/QA.md` |
| x | `.work/notes/` のノートを更新する | - `.work/notes/jp-mirror-policy.md` （PR108 開始時に作成済み） |
| x | `/claude-kit:hook-creator` で JP ミラー確認フックを実装 | - `plugins/claude-kit/hooks/hooks.json`, `plugins/claude-kit/hooks/prompts/jp-mirror-check.md` |
| x | ルール・CLAUDE.md を整備する | - 追加不要（既存ルールでカバー済み） |

## 参考ドキュメント

- `.work/notes/jp-mirror-policy.md`: JPミラーポリシーとフック設計メモ
- `plugins/claude-kit/skills/hook-creator/SKILL.md`: フック作成手順

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
