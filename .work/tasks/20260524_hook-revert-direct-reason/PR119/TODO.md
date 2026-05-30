# PR119 — hook-read-follow-remove

## 概要

PR115 で修正した "Read and follow:" パターン廃止の残作業。
`plugins/claude-kit/hooks/hooks.json` の UserPromptSubmit × 5 と PostToolUse × 1 が未修正のため、他フックと同様に直接コンテンツ埋め込み方式へ変更する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR115 | Read and follow パターンを廃止し直接コンテンツ埋め込みに戻す（claude-kit 以外を修正） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR119/QA.md` |
| 済 | `.work/notes/hook-revert-direct-reason.md` を更新する | - `.work/notes/hook-revert-direct-reason.md` |
| 済 | UserPromptSubmit フック × 5 の Read and follow を直接埋め込みに変更 | - `plugins/claude-kit/hooks/hooks.json` |
| 済 | PostToolUse フック × 1 の Read and follow を直接埋め込みに変更 | - `plugins/claude-kit/hooks/hooks.json` |
| 済 | plugin.json と marketplace.json のバージョンをバンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/hook-revert-direct-reason.md`: PR115 の設計メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
