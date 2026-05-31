# workプラグインdescription同期修正

> ブランチ: `fix/work-plugin-description-sync`

## 概要

`work` プラグインの `description` フィールドが `plugin.json` と `marketplace.json` で不一致になっている。
`plugin.json` には `v2.54.0` エントリが欠落しており、`v2.53.1` から `v2.55.0` に直接飛んでいる。

高級対策として、`バージョン同期.md` リファレンスに `description` の完全一致確認をチェックリストへ追加する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | 未解決事項を `## QA` に記録する |
| 2 | - | `plugins/work/.claude-plugin/plugin.json` に v2.54.0 エントリを追記 |
| 3 | - | `plugins/claude-kit/references/plugin/バージョン同期.md` に description 一致確認を追加（高級対策） |
| 4 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/.claude-plugin/plugin.json` | 編集 | v2.54.0 エントリを追記 | |
| 2 | `plugins/claude-kit/references/plugin/バージョン同期.md` | 編集 | description 一致確認をチェックリストに追加 | |
| 3 | `plugins/claude-kit/references/plugin/バージョン同期.jp.md` | 編集 | JPミラーも同期 | |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | plugin.json の description が marketplace.json と完全一致している | (未実施) | - |

## QA

（未解決事項なし）

## 参考ドキュメント

（最終コミット時に追記）

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-002 | work プラグインの description が marketplace.json と plugin.json で不一致 | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | — | — |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | 他プラグインのdescriptionドリフト確認 | dev-kit / claude-kit / ref-inject も同様のドリフトがないか確認 | 即時実施可 |
