# plugin-configスキル復活

> ブランチ: `feat/restore-plugin-config-skill`

## 概要

### 実施条件

即時実施可

### 背景

`refactor/plugin-config-removal`（260602）で `work:plugin-config` / `dev-kit:plugin-config` / `claude-kit:config` の3スキルと関連リファレンス（`プラグイン設定.md`）、および `プラグイン構造.md` の「env vars を持つプラグインには plugin-config 必須」ルールが削除された。ユーザーの要望により復活する。

### 目的

- 3スキルを削除コミット（95132b91）の内容から復元する
- `プラグイン構造.md` に plugin-config 必須ルールを復元する
- `プラグイン設定.md` リファレンスを復元する
- 各プラグインの CLAUDE.md スキルリストに plugin-config を再追記する

## 作業内容

| No | タスク | 完了 |
|---|---|---|
| 1 | `work:plugin-config` スキル（SKILL.md + SKILL.jp.md）を復元 | 済 |
| 2 | `dev-kit:plugin-config` スキル（SKILL.md + SKILL.jp.md）を復元 | 済 |
| 3 | `claude-kit:plugin-config` スキル（SKILL.md + SKILL.jp.md）を作成（`config` → `plugin-config` に統一） | 済 |
| 4 | `ref-inject:plugin-config` スキル（SKILL.md + SKILL.jp.md）を新規作成（skeleton） | 済 |
| 5 | `claude-kit/references/plugin/プラグイン設定.md`（+ jp）を復元 | 済 |
| 6 | `claude-kit/references/plugin/プラグイン構造.md`（+ jp）に plugin-config 必須ルールを復元 | 済 |
| 7 | `plugin-creator` SKILL.md（+ jp）Step 5 に plugin-config 必須記載を復元 | 済 |
| 8 | `_injection_rules.yaml` / `_index.yaml`（+ jp）/ `_index.md` にプラグイン設定.md を登録 | 済 |
| 9 | work / dev-kit / claude-kit / ref-inject の CLAUDE.md(+jp) スキルリストに plugin-config を追記 | 済 |
| 10 | 4プラグインの plugin.json + marketplace.json + CLAUDE.md changelog をバージョンバンプ | 済 |
| 11 | （併修）`_index.yaml` の既存 YAML パースエラー修正（line 21 コロン+空白を引用符化） | 済 |
| 12 | QA を記録する | 済 |
| 13 | ノートを更新する | 済 |

## 変更内容

| No | ファイル | 変更 |
|---|---|---|
| 1 | `plugins/work/skills/plugin-config/SKILL.md`（+ jp） | 復元（新規） |
| 2 | `plugins/dev-kit/skills/plugin-config/SKILL.md`（+ jp） | 復元（新規） |
| 3 | `plugins/claude-kit/skills/plugin-config/SKILL.md`（+ jp） | 作成（`config`→`plugin-config` 統一） |
| 4 | `plugins/ref-inject/skills/plugin-config/SKILL.md`（+ jp） | 新規（skeleton） |
| 5 | `plugins/claude-kit/references/plugin/プラグイン設定.md`（+ jp） | 復元 |
| 6 | `plugins/claude-kit/references/plugin/プラグイン構造.md`（+ jp） | plugin-config 必須ルール復元 |
| 7 | `plugins/claude-kit/skills/plugin-creator/SKILL.md`（+ jp） | Step 5 必須スキル記載復元 |
| 8 | `plugins/claude-kit/references/.ref-inject/_injection_rules.yaml` | プラグイン設定.md を SKILL.md / plugin.json パターンに追加 |
| 9 | `plugins/claude-kit/references/.ref-inject/_index.yaml`（+ jp） | プラグイン設定.md 登録 + line21 パースエラー修正 |
| 10 | `plugins/claude-kit/references/_index.md` | プラグイン設定.md 行を復元 |
| 11 | `plugins/{work,dev-kit,claude-kit,ref-inject}/CLAUDE.md`（+ jp） | スキルリスト追記・changelog・version |
| 12 | `plugins/{work,dev-kit,claude-kit,ref-inject}/.claude-plugin/plugin.json` | version bump |
| 13 | `.claude-plugin/marketplace.json` | 4プラグインの version bump |

## テスト

| No | 項目 | 結果 |
|---|---|---|
| 1 | 全 plugin.json / marketplace.json の JSON 妥当性 | OK |
| 2 | `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` の YAML パース | OK（17/17/12 件） |
| 3 | 孤立リファレンスチェック（rules ⇔ index ⇔ ファイル実在） | プラグイン設定.md は正常バインド、新規孤立なし |
| 4 | plugin.json と marketplace.json の version 一致 | 4プラグイン全 MATCH |

## QA

| ID | 質問 | 回答 |
|---|---|---|
| QA-001 | `ref-inject` プラグインにも `plugin-config` スキルを追加するか？（ref-inject 固有の設定可能な env 変数は現状なさそう） | 追加する（env vars がなくても skeleton として作成） |
| QA-002 | `claude-kit` のスキル名は `config` のまま（削除前の状態）か、それとも `plugin-config` に統一するか？ | `plugin-config` に統一する |

## 参考ドキュメント

- `.work/notes/スキル設計/plugin-configスキル.md` — plugin-config スキルの現状仕様

## 関連ブランチ

| ブランチ | 関係 |
|---|---|
| `refactor/plugin-config-removal` | 削除元ブランチ（復元対象） |

## 次ブランチ候補

| No | ブランチ名 | 概要 | 優先度 |
|---|---|---|---|
| 1 | — | — | — |
