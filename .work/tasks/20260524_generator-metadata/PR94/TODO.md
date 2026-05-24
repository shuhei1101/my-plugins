# PR94 — generator-metadata

## 概要

creator スキル群が生成するファイルに **出自メタデータ**（プラグイン名・スキル名・バージョン）を HTML/Python コメント形式で埋め込む。
JP ミラーには警告コメントも付与。既存の全生成物にも遡及適用。バージョン同期スキルを新規追加。

## 作業内容

| 完了 | 作業内容 |
|---|---|
| 済 | 仕様メモ作成（メタデータ記法、警告文言、対象範囲、同期スキル仕様） |
| 済 | 仕様メモを mark-generated スキル切り出し方針に更新 |
| 済 | `mark-generated` スキル新規作成（claude-kit） |
| 済 | `version-sync` スキル新規作成（claude-kit、完全自動モード） |
| 済 | claude-kit の全 creator スキル（skill/hook/rule/claude/plugin）に mark-generated 呼び出しセクション追加 |
| 済 | work-kit/work-start / pr-handoff に mark-generated 呼び出しセクション追加 |
| 済 | ui-kit/debug-fab に mark-generated 呼び出しセクション追加 |
| 済 | 既存生成物 89 ファイルに遡及的にメタデータを書き込み |
| 済 | ルール: creator-skill-dispatch.md にメタデータ強制ルール追記 |
| 済 | ルール: skill-jp-mirror-sync.md に JP ミラー警告必須化 |
| 済 | glossary に新用語（出自メタデータ / mark-generated / version-sync）を追加 |
| 済 | claude-kit バージョン bump (3.17.1 → 3.18.0) + changelogs v3.18.0.md |
| 済 | work-kit バージョン bump (2.23.0 → 2.24.0) + changelogs v2.24.0.md |
| 済 | ui-kit バージョン bump (1.3.1 → 1.3.2) + changelogs v1.3.2.md |
| 済 | marketplace.json バージョン同期 |

## 参考ドキュメント

- `.work/notes/generator-metadata.md`: メタデータ記法・対象範囲・version-sync スキル仕様

## 次PR候補

| タイトル | 概要 |
|---|---|
| mark-generated HTML/JS/CSS 対応 | uidev.js / uidev.css / example.html / mock-skeleton.html などのテンプレに対応する記法を mark-generated に追加し、ui-kit のテンプレ全体を遡及スタンプ対象に含める |
