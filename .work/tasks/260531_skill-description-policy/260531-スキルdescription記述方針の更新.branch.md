# スキルdescription記述方針の更新

> ブランチ: `docs/skill-description-policy`

## 概要

スキルの `description` frontmatter は短くていい、`trigger` フレーズは不要という方針に変更する。
記述量が増えるとコンテキスト圧迫につながるため、簡潔な説明のみにとどめる。
この方針変更に伴い、「descriptionにtriggerフレーズが足りない」「triggerフレーズが重複している」という前提で立てられた ISSUE-034 と ISSUE-035 をクローズする。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | 未解決事項を `## QA` に記録する |
| 2 | - | `claude-kit/references/skill/スキル.md` に「descriptionは短くていい・triggerは不要」という方針を追記する |
| 3 | - | ISSUE-034・ISSUE-035 をクローズ（関連イシューとして登録） |
| 4 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/references/skill/スキル.md` | 編集 | description・trigger記述方針を追記 | |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | スキルリファレンスに方針が記載されている | (未実施) | - |

## QA

（未解決事項なし）

## 参考ドキュメント

- （最終コミット時に追記）

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-034 | `work:branch-show` と `work:qa-review` の description にトリガー条件が不十分 | resolved |
| 2 | ISSUE-035 | 複数プラグインの `plugin-config` スキルで description トリガーフレーズが重複している | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | — | — |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | — | — | — |
