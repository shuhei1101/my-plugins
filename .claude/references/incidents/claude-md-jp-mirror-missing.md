# claude-md-jp-mirror-missing

## 概要

`CLAUDE.md` を編集した際に `CLAUDE.jp.md` の JP ミラー更新を忘れた。

## 発生状況

PR110 で `CLAUDE.md` の「Plugin Creation & Update Rules」セクションを削除したが、対応する `CLAUDE.jp.md` の「プラグイン作成・更新のルール」セクションを削除しなかった。ユーザーに「日本語ミラー更新忘れてない？」と指摘され、追加コミットで対応した。

## 根本原因

`skill-jp-mirror-sync.md` は `plugins/**/skills/**/SKILL.md` のみ、`hook-prompts-jp-mirror-sync.md` は `plugins/**/hooks/prompts/*.md` のみをトリガーに設定しており、プロジェクトルートの `CLAUDE.md` や `plugins/**/CLAUDE.md` はカバーされていなかった。

## 修正内容

- `CLAUDE.jp.md` を英語版に追従して更新
- `claude-md-jp-mirror-sync.md` ルールを新規作成（`CLAUDE.md` と `plugins/**/CLAUDE.md` をトリガーに設定）
- incidents.md にこのエントリを追加

## 教訓

JP ミラーが必要なファイルカテゴリごとに専用の同期ルールを用意する。SKILL.md・hooks/prompts/*.md に続き CLAUDE.md も対象に加えた。新しいカテゴリのファイルを作成するたびに「JP ミラーが必要か」「対応する同期ルールが存在するか」を確認すること。
