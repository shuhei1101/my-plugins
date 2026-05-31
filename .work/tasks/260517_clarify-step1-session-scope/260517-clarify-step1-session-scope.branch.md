# PR34 — clarify-step1-session-scope

## 概要

`user-prompt-submit` フックのステップ1で「進行中のPR」が現在の Claude Code との会話セッション内のものに限定されることを明確化する。
従来の曖昧な書き方だと、`index.yaml` 等を読んで過去の他セッションの PR を「進行中」と誤認する問題があった。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | ステップ1の処理内容を「現在の Claude Code との会話セッション」に限定するよう書き換え | - `plugins/work-kit/hooks/prompts/user-prompt-submit.jp.md`<br>- `plugins/work-kit/hooks/prompts/user-prompt-submit.md` |
| 済 | 補足として「index.yaml は読まない」「不明ならPRなし扱い」を追記 | 同上 |
| 済 | PR32 アーカイブエントリを index.archive.yaml に追加（未コミット分の修正） | - `.work/tasks/index.archive.yaml` |

## 参考ドキュメント

- `plugins/work-kit/hooks/prompts/user-prompt-submit.md`: 対象フックファイル（英語）
- `plugins/work-kit/hooks/prompts/user-prompt-submit.jp.md`: 対象フックファイル（日本語ミラー）

## QA

なし
