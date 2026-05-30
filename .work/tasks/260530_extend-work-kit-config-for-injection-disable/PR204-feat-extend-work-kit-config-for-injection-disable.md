# PR204 — extend-work-kit-config-for-injection-disable

## 概要

`work:config` スキルを `{PREFIX}_INJECTION_DISABLE`（逆極性）対応に拡張する。

PR164 で実装された `{PREFIX}_INJECTION_DISABLE` は他のトグルと逆極性（truthy で無効化）であるため、PR167 時点では work:config の対象外とされていた。PR174 で claude-kit への実装が完了したため、このタイミングで work:config スキルに追加する。

現在 work:config が管理する変数は 7 件。今回追加するのは `CLAUDE_KIT_INJECTION_DISABLE` と `DEV_KIT_INJECTION_DISABLE` の 2 件。

### 実施条件

PR174「propagate-injection-disable-to-plugins」が完了してから（完了済み）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する（QA なし） | - |
| 済 | ノートドキュメントを更新する | `.work/notes/plugin-config-skill.md` |
| 済 | Managed Toggles テーブルに 2 変数を追加 | `plugins/work/skills/config/SKILL.md` |
| 済 | Step 1 に逆極性変数の状態判定ロジックを追加（truthy = OFF） | |
| 済 | Step 2 の AskUserQuestion オプションを更新（INJECTION_DISABLE 変数を その他 案内に追記） | |
| 済 | Step 3 に逆極性変数向けの値選択オプションを追加 | |
| 済 | Step 4 に逆極性変数の適用ロジックを追加（OFF = "true"、ON = キー削除） | |
| 済 | Notes の除外文言を削除 | |
| 済 | SKILL.jp.md を更新 | `plugins/work/skills/config/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンバンプ（MINOR: 2.46.2 → 2.47.0） | `plugins/work/.claude-plugin/plugin.json`<br>`.claude-plugin/marketplace.json` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/skills/config/SKILL.md` | 編集 | 逆極性 INJECTION_DISABLE 対応を追加 | |
| `plugins/work/skills/config/SKILL.jp.md` | 編集 | 上記の日本語ミラー更新 | |
| `plugins/work/.claude-plugin/plugin.json` | 編集 | バージョン 2.46.2 → 2.47.0 | |
| `.claude-plugin/marketplace.json` | 編集 | work プラグインのバージョン 2.46.2 → 2.47.0 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストファイルなし | - |

## QA

PR スコープの未決定事項を QA-XXX として記録する。

## 参考ドキュメント

- `.work/notes/plugin-config-skill.md`: work:config スキル設計メモ（PR167 の実装記録と UX フロー設計）
- `.work/notes/env-toggles-for-hooks-and-steps.md`: PR164 の env トグル実装メモ（INJECTION_DISABLE の逆極性設計背景）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #167 | work:config スキル初期実装 |
| #174 | claude-kit への CLAUDE_KIT_INJECTION_DISABLE 実装（本 PR の実施条件） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
