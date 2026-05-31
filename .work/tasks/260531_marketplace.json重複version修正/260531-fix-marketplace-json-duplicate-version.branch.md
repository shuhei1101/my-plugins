# fix/marketplace-json-duplicate-version

> 内部 ID: 220（index.yaml 採番用 — クロスリファレンス目的）

## 概要

PR175 のマージ作業中、`master` を取り込んだ際の `.claude-plugin/marketplace.json` の
バージョン衝突解消で sed コマンドにミスがあり、claude-kit エントリに `"version"` 行が
**重複したまま** コミットされてしまった（コミット `82865846`）。これにより以下のような
不正な JSON が master に入った：

    {
      "name": "claude-kit",
      ...
      "version": "3.44.0"
      "version": "3.43.2"
    }

JSON パーサーで読み込めない状態のため、`marketplace.json` を参照する処理（プラグイン
インストール／更新／list など）が壊れている可能性がある。

このブランチで重複行を削除して妥当な JSON に戻す。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | 済 | 重複した `"version": "3.43.2"` 行を削除 | - `.claude-plugin/marketplace.json` |
| 2 | 済 | `python -c "import json; json.load(...)"` で JSON 妥当性を検証 | - 同上 |
| 3 | 済 | 再発防止ノートを作成 | - `.work/notes/incident-marketplace-json-merge-conflict-sed-mistake.md` |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `.claude-plugin/marketplace.json` | 編集 | claude-kit エントリの重複 version 行を削除し、3.44.0 のみ残す | sed -i '21d' で 21 行目削除 |
| 2 | `.work/notes/incident-marketplace-json-merge-conflict-sed-mistake.md` | 新規 | 再発防止ノート（sed でのコンフリクト解消の落とし穴） | - |

## テスト

このブランチではテストファイルの追加・変更はない。妥当性は python の json.load で検証済み。

## QA

（未決定事項なし）

## 参考ドキュメント

- コミット `82865846 chore: master を取り込み、バージョンコンフリクトを解消 #PR175`: ミスが入ったコミット
- コミット `14c2badb feat: claude-kit-plugin-config-reference #175`: マージコミット（壊れた JSON を含む）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | PR175 / feat/claude-kit-plugin-config-reference（マージ済み） | 壊れ JSON が入った経緯のあるブランチ |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
