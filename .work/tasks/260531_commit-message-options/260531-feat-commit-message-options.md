# feat/commit-message-options

> 内部 ID: 241（index.yaml 採番用 — クロスリファレンス目的）

## 概要

コミットメッセージのフォーマットを環境変数で設定可能にする。
- `WORK_COMMIT_LANG`: メッセージ言語（`JP` = 日本語、`EN` = 英語。デフォルト: `JP`）
- `WORK_COMMIT_TYPE`: Conventional commit タイププレフィックスの付与（デフォルト: `true`）

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `## QA` に未解決事項を記録する |
| 2 | 済 | `.work/notes/` のノートを更新する |
| 3 | 済 | `plugins/work/skills/start/SKILL.md` のコミットメッセージ言語セクションを env var 対応に更新 |
| 4 | 済 | `plugins/work/skills/start/SKILL.jp.md` を同期 |
| 5 | 済 | `plugins/work/CLAUDE.md` に新 env var 2 件を追記・バージョン更新 |
| 6 | 済 | `plugins/work/CLAUDE.jp.md` を同期 |
| 7 | 済 | `plugins/work/skills/plugin-config/SKILL.md` に `WORK_COMMIT_TYPE` を追加 |
| 8 | 済 | `plugins/work/skills/plugin-config/SKILL.jp.md` を同期 |
| 9 | 済 | `plugins/work/.claude-plugin/plugin.json` のバージョンを 2.51.0 に更新 |
| 10 | 済 | ルール / CLAUDE.md を更新する（変更なし） |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/start/SKILL.md` | 編集 | コミットメッセージ言語セクションを env var 対応に変更 | - |
| 2 | `plugins/work/skills/start/SKILL.jp.md` | 編集 | 上記の JP ミラー | - |
| 3 | `plugins/work/CLAUDE.md` | 編集 | 環境変数テーブルに 2 件追加・changelog 追記 | - |
| 4 | `plugins/work/CLAUDE.jp.md` | 編集 | 上記の JP ミラー | - |
| 5 | `plugins/work/skills/plugin-config/SKILL.md` | 編集 | WORK_COMMIT_TYPE をトグル一覧に追加 | - |
| 6 | `plugins/work/skills/plugin-config/SKILL.jp.md` | 編集 | 上記の JP ミラー | - |
| 7 | `plugins/work/.claude-plugin/plugin.json` | 編集 | バージョンを 2.51.0 に更新 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | — | — | テスト変更なし | — |

## QA

未解決事項なし。

## 参考ドキュメント

- `plugins/work/CLAUDE.md`: work プラグインの環境変数・スキル一覧

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/branch-author-env | 直前に追加された `WORK_BRANCH_AUTHOR` 実装（同パターン） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | — | — | — |
