# ISSUE-138: plugin-config が管理する env 変数名が CLAUDE.md・実装と不一致

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する

## QA

### QA-1: どちらの変数名を正とするか

A) CLAUDE.md の `WORKSPACE_STOP_REMINDER` / `WORKSPACE_MERGE_PROPOSAL` に統一する（スクリプト側も変更） / B) スクリプト実装の `WORK_STOP_REMINDER` / `WORK_MERGE_PROPOSAL` に統一する（CLAUDE.md と plugin-config を変更）

**推奨**: B — `stop.py` / `user-prompt-submit.py` の実際の変数名が `WORK_STOP_REMINDER` / `WORK_BRANCH_ENFORCEMENT` / `WORK_MERGE_PROPOSAL` であり、コードを変えずドキュメント側を合わせる方が変更範囲が少ない

**回答**: A / B

---

## 概要

`plugins/work/skills/plugin-config/SKILL.md` の「Managed Toggles」テーブルおよびステップ内の変数名が、CLAUDE.md の Environment Variables テーブルと実際のフックスクリプトの変数名と不一致になっている。

## 背景

`work:plugin-config` スキルは環境変数トグルを対話的に設定する。ユーザーがこのスキルを使って設定した変数名が実際にフックが読む変数名と異なると、設定が無効になる（サイレント no-op）。これは incidents No.22（`path-home-cross-env-mismatch`）に類する「名前のズレによる無効適用」の問題。

## 現状

`plugins/work/skills/plugin-config/SKILL.md` 内:
- 行 20: `| WORK_BRANCH_ENFORCEMENT | UserPromptSubmit work-start 強制注入 | 有効 |`
- 行 21: `| WORK_STOP_REMINDER | Stop TODO/QA リマインダー注入 | 有効 |`
- 行 85: `WORK_MERGE_PROPOSAL` は記載あり（これは正しい）

`plugins/work/CLAUDE.md` 内（Environment Variables テーブル）:
- 行 95: `${WORKSPACE_STOP_REMINDER}` → `WORK_STOP_REMINDER` と名前が異なる
- 行 96: `${WORKSPACE_MERGE_PROPOSAL}` → `WORK_MERGE_PROPOSAL` は plugin-config 側と一致するが CLAUDE.md は古い名前

実際のフックスクリプト:
- `hooks/scripts/stop.py` 行 22: `env_truthy("WORK_STOP_REMINDER", ...)` — `WORK_STOP_REMINDER` を使用
- `hooks/scripts/stop.py` 行 31: `env_truthy("WORK_MERGE_PROPOSAL", ...)` — `WORK_MERGE_PROPOSAL` を使用
- `hooks/scripts/user-prompt-submit.py` 行 21: `WORK_BRANCH_ENFORCEMENT` を使用

つまり実装は `WORK_STOP_REMINDER` / `WORK_MERGE_PROPOSAL` / `WORK_BRANCH_ENFORCEMENT` を使っており、`plugin-config` はこれを正しく記載しているが、CLAUDE.md の Environment Variables テーブルが古い `WORKSPACE_STOP_REMINDER` / `WORKSPACE_MERGE_PROPOSAL` のままになっている。

## 原因

v2.43.0 で `${WORKSPACE_MERGE_PROPOSAL}` が追加されたが、その後のリファクタリングで実際の変数名が `WORK_MERGE_PROPOSAL` / `WORK_STOP_REMINDER` に変更されたにもかかわらず、CLAUDE.md の Environment Variables テーブルの更新が漏れたと推定される。

## 期待される状態

- CLAUDE.md の Environment Variables テーブルに `${WORK_STOP_REMINDER}` / `${WORK_MERGE_PROPOSAL}` / `${WORK_BRANCH_ENFORCEMENT}` が正しい名前で掲載される
- `plugin-config` SKILL.md の記述と CLAUDE.md と実装が三者一致している

## 対応案

B 案: CLAUDE.md の Environment Variables テーブルを実装の変数名に合わせて修正する。
- `${WORKSPACE_STOP_REMINDER}` → `${WORK_STOP_REMINDER}`
- `${WORKSPACE_MERGE_PROPOSAL}` → `${WORK_MERGE_PROPOSAL}`
- `${WORK_BRANCH_ENFORCEMENT}` を新規追加（現在テーブルに存在しない）

変更対象ファイル: `plugins/work/CLAUDE.md`（+ JP ミラー）
