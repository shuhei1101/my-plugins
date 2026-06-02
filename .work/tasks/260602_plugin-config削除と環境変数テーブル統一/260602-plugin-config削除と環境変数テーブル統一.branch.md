# plugin-config削除と環境変数テーブル統一

> ブランチ: `refactor/plugin-config-removal`

## 概要

各プラグインに同梱されている対話式の `plugin-config` スキル（env トグルを `AskUserQuestion` で 1 個ずつ切り替える）を全廃する。対話式より settings.json を直接編集する方が速いという判断。あわせて、各プラグインの `CLAUDE.md` の環境変数テーブルがプラグインごとにバラバラなフォーマットになっているため、3 列の統一フォーマットに揃える。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する |
| 2 | 済 | `work` / `dev-kit` の `plugin-config` スキル本体を削除する（あわせて `claude-kit:config` も削除） |
| 3 | 済 | `プラグイン設定.md`(+jp) リファレンスを削除し `_index.md` / `.ref-injects/*` の登録を除去する |
| 4 | 済 | `プラグイン構造.md`(+jp) の plugin-config 必須記載を削除する |
| 5 | 済 | `plugin-creator` / `config` スキル、各 `CLAUDE.md` の plugin-config 言及を除去する |
| 6 | 済 | `work` / `dev-kit` / `claude-kit` の `CLAUDE.md`(+jp) の環境変数テーブルを新3列フォーマットに統一する |
| 7 | 済 | フォーマット仕様元 `プラグインCLAUDE-md.md`(+jp) を新フォーマット定義に更新する |
| 8 | 済 | 各プラグイン + marketplace.json のバージョンバンプ |
| 9 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/{work,dev-kit}/skills/plugin-config/`, `plugins/claude-kit/skills/config/` | 削除 | 対話式 env 設定スキルを全廃 | SKILL.md + .jp.md |
| 2 | `plugins/claude-kit/references/plugin/プラグイン設定.md`(+jp) | 削除 | config スキル記述ガイドを廃止 | |
| 3 | `plugins/claude-kit/references/.ref-injects/{_index,_index.jp,_injection_rules}.yaml` | 編集 | プラグイン設定 の索引・注入登録を除去 | |
| 4 | `plugins/claude-kit/references/_index.md` | 編集 | プラグイン設定 行を削除 | |
| 5 | `plugins/claude-kit/references/plugin/プラグイン構造.md`(+jp) | 編集 | plugin-config 必須記載セクションを削除 | |
| 6 | `plugins/claude-kit/skills/plugin-creator/SKILL.md`(+jp) | 編集 | 必須スキルから plugin-config を除去 | |
| 7 | `plugins/{work,dev-kit,claude-kit}/CLAUDE.md`(+jp) | 編集 | 環境変数テーブルを3列形式に統一・plugin-config 言及除去・changelog/バージョン | |
| 8 | `plugins/claude-kit/references/plugin/プラグインCLAUDE-md.md`(+jp) | 編集 | env テーブル仕様を新3列形式に再定義 | |
| 9 | `plugins/{work,dev-kit,claude-kit}/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | 編集 | バージョンバンプ（work 2.65.0 / dev-kit 4.14.0 / claude-kit 3.52.0） | |
| 10 | `.work/notes/環境・設定・ポリシー/envトグル実装メモ.md` | 編集 | plugin-config 言及を現状に修正 | |
| 11 | `.work/notes/スキル設計/{プラグイン設定スキル,plugin-config-reference}.md` | 削除 | 廃止機能の設計メモを削除（`_index.md` 更新） | |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `grep -r plugin-config` で残存言及がないこと | (未実施) | - |
| 2 | 新フォーマットの env テーブルが日英ミラーで一致すること | (未実施) | - |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

（ユーザーとの対話でフォーマット・スコープともに確定済み。未解決の QA なし）

## 参考ドキュメント

- `.work/notes/環境・設定・ポリシー/envトグル実装メモ.md`: env トグルの実装メモ（plugin-config 廃止を反映）
- `plugins/claude-kit/references/plugin/プラグインCLAUDE-md.md`: 環境変数テーブルの新フォーマット定義（仕様元）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | (なし) | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | (なし) | - | - |
