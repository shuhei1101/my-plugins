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

- [ ] `work:plugin-config` スキル（SKILL.md + SKILL.jp.md）を復元
- [ ] `dev-kit:plugin-config` スキル（SKILL.md + SKILL.jp.md）を復元
- [ ] `claude-kit:config` スキル（SKILL.md + SKILL.jp.md）を復元
- [ ] `claude-kit/references/plugin/プラグイン設定.md`（+ jp）を復元
- [ ] `claude-kit/references/plugin/プラグイン構造.md`（+ jp）に plugin-config 必須ルールを復元
- [ ] work / dev-kit / claude-kit の CLAUDE.md スキルリストに plugin-config を追記
- [ ] marketplace.json のバージョンを更新
- [ ] QA を記録する
- [ ] ノートを更新する

## 変更内容

| No | ファイル | 変更 |
|---|---|---|
| 1 | — | — |

## テスト

| No | 項目 | 結果 |
|---|---|---|
| 1 | — | — |

## QA

| ID | 質問 | 回答 |
|---|---|---|
| QA-001 | `ref-inject` プラグインにも `plugin-config` スキルを追加するか？（ref-inject 固有の設定可能な env 変数は現状なさそう） | |
| QA-002 | `claude-kit` のスキル名は `config` のまま（削除前の状態）か、それとも `plugin-config` に統一するか？ | |

## 参考ドキュメント

## 関連ブランチ

| ブランチ | 関係 |
|---|---|
| `refactor/plugin-config-removal` | 削除元ブランチ（復元対象） |

## 次ブランチ候補

| No | ブランチ名 | 概要 | 優先度 |
|---|---|---|---|
| 1 | — | — | — |
