---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成（PR41）
related_specs: []
related_prs:
  - PR41
---

# work-kit stop hook — セッション終了前チェック

## 概要

`stop` フックは、Claude Code がレスポンスを完了する直前に実行される。
セッション中に進行中の PR に対して、完了前に以下を確認させることで、
作業漏れや未回答の QA を防ぐ。

## チェック項目

応答を完了する前に、以下を順番に確認する:

1. **TODO 更新**: 現在のセッションで対応している PR の `TODO.md` を更新し、完了した作業の `完了` 列を `済` にする
2. **QA 全回答確認**: 同 PR の `QA.md` に未回答（保留中）の QA エントリが残っていないことを確認する
3. **スペック反映確認**: 今回の作業内容が `.work/specs/` 配下の仕様書に反映・書き起こされていることを確認する

## マージ提案の条件

上記 3 項目がすべて満たされた場合にのみ、ユーザーに `/work-kit:merge` の実行を**提案するだけ**にする（自動実行しない）。

## 対象ファイル

| ファイル | 役割 |
|---|---|
| `plugins/work-kit/hooks/prompts/stop.md` | Claude Code が読み込む英語プロンプト |
| `plugins/work-kit/hooks/prompts/stop.jp.md` | 日本語ミラー（人間参照用） |
| `plugins/work-kit/hooks/hooks.json` | stop フックの登録 |
