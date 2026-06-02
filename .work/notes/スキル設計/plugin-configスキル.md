# plugin-config スキル — プラグイントグル設定

各プラグインが env トグル変数を対話的に設定できるスキル。`settings.json` の `env` ブロックを
手編集せずに、`AskUserQuestion` のループで現在状態の表示・値の切替・スコープ選択・適用を行う。

## 配置

env vars を公開するプラグインは `plugin-config` スキルを必ず同梱する（`プラグイン構造.md` の必須ルール）。
env vars を持たないプラグインは本来不要だが、ref-inject には将来用の skeleton を置いている。

| プラグイン | スキル名 | 管理対象 |
|---|---|---|
| work | `work:plugin-config` | WORK_BRANCH_ENFORCEMENT / WORK_STOP_REMINDER / WORK_USE_WORKTREE / WORK_MERGE_PROPOSAL / WORK_COMMIT_TYPE / WORK_PRECOMPACT_CONV2CLAUDE / WORK_MERGE_CONV2CLAUDE / AITUBER_NOTIFY |
| dev-kit | `dev-kit:plugin-config` | DEV_KIT_PYTHON / HTML / NEXT / MARKDOWN（opt-in）+ DEV_KIT_NEXT_TS_CHECK / DEV_KIT_MARKDOWN_CHECK（機能トグル） |
| claude-kit | `claude-kit:plugin-config` | CLAUDE_KIT_JP_MIRROR / CLAUDE_KIT_INJECTION_LANG / CLAUDE_KIT_INJECTION_TTL |
| ref-inject | `ref-inject:plugin-config` | なし（skeleton。各消費プラグインの plugin-config へ誘導） |

## スキル構造（5 ステップの AskUserQuestion ループ）

1. **現在の状態を読み取る** — project / user の settings.json を読み、状態テーブルを表示
2. **env 変数を選択（ループ先頭）** — 番号付きプレーンテキストリスト（`AskUserQuestion` は 4 択上限のため不使用）。`0`/`q` で終了
3. **値とスコープを選択** — `AskUserQuestion` を 1 コール 2 問（値 + 書込先 project/user）
4. **変更を適用** — settings.json を編集し変更を記録 → ステップ 2 へループ
5. **レポート** — 全変更のサマリーテーブル

## トグルの極性

| 極性 | 不在時 | 無効化 | デフォルトへ戻す | 採用例 |
|---|---|---|---|---|
| 通常極性 | ON | `"false"` に設定 | キー削除 | work 全トグル、dev-kit 機能トグル |
| opt-in 極性 | OFF | キー削除 | キー削除 | dev-kit 言語トグル |
| 文字列値 | デフォルト値 | — | キー削除 | CLAUDE_KIT_INJECTION_LANG（en/jp）、INJECTION_TTL |

## 除外対象

`{PREFIX}_INJECTION_DISABLE`（逆極性のキルスイッチ。truthy = 無効化）は plugin-config の管理対象外。
`settings.json` を手動編集する。文字列型 env var（WORK_BRANCH_AUTHOR / WORK_BASE_BRANCH / WORK_COMMIT_LANG）も
ブール型トグル専用の本スキルでは扱わず手動設定。

## 経緯

- 一度 `refactor/plugin-config-removal`（260602, claude-kit 3.54.0 等）で全廃され「settings.json 直接編集」方針に変更されたが、
  ユーザー要望により `feat/restore-plugin-config-skill` で復活（work 2.66.0 / dev-kit 4.15.0 / claude-kit 3.55.0 / ref-inject 1.10.0）。
- claude-kit はかつて `config` という名前だったが、復活時に `plugin-config` へ統一。
- 記述ガイドは `claude-kit/references/plugin/プラグイン設定.md`（SKILL.md / plugin.json 編集時に optional 注入）。

## 変更履歴

| 日付 | 変更 |
|---|---|
| 2026-06-02 | 4プラグインに plugin-config スキルを復活。claude-kit は config から改名統一、ref-inject は skeleton。記述ガイド・必須ルール・注入登録も復元 |
