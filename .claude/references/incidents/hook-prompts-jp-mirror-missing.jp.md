<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# hook-prompts-jp-mirror-missing

## 概要

`hook-creator` スキルで `hooks/prompts/*.md` を新規作成した際、`*.jp.md` の JP ミラーを作成しなかった。

## 発生状況

PR103 で creator-dispatch フック用のプロンプトファイル5種を作成したとき、英語ファイルのみ作成し JP ミラーを省略した。ユーザーに「プロンプト作るときは必ず日本語ミラーもつくれ」と指摘され、追加コミットで対応した。

## 根本原因

`skill-jp-mirror-sync.md` ルールは `plugins/**/skills/**/SKILL.md` のみをトリガーに設定しており、`hooks/prompts/*.md` はカバーされていなかった。そのため hook prompts 作成時に JP ミラー義務がルールとして自動注入されなかった。

## 修正内容

- `hooks/prompts/*.md` 5種に `*.jp.md` JP ミラーを追加
- `hook-prompts-jp-mirror-sync.md` ルールを新規作成（`plugins/**/hooks/prompts/*.md` をトリガーに設定）
- incidents.md にこのエントリを追加

## 教訓

ファイル同期ルールを作るときは、同じ「JP ミラー必須」パターンが適用される関連ファイルカテゴリをすべて洗い出し、それぞれ別ルールに明示しておくこと。`skill-jp-mirror-sync.md` を作った時点で hook prompts もスコープに含めるべきだった。
