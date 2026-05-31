# chore/sync-ref-inject-template

> 内部 ID: 239（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`ref-inject` テンプレート (`inject_references.py`, `_common.py`) と、コンシューマープラグイン
（`claude-kit` / `dev-kit` / `work`）の間で機能的ドリフトが発生している。

コンシューマーはテンプレートより **先進** しており:
- `TRUTHY` 定数をモジュールレベルに追加
- キルスイッチ (`INJECTION_DISABLE`) を依存チェックより **前** に移動
- `_common.py` のコメントブロックが古いまま

テンプレート側を最新コンシューマーの共通改善に合わせ、`_common.py` はコンシューマーも更新する。
コンシューマー固有の拡張（claude-kit の JP_MIRROR、dev-kit の lang ゲーティング）には触れない。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録する |
| 2 | 済 | ノートを `.work/notes/` に作成・更新する |
| 3 | 済 | `ref-inject` テンプレートの `inject_references.py` を更新（TRUTHY + キルスイッチ前置き） |
| 4 | 済 | `ref-inject` テンプレートの `_common.py` コメントを更新 |
| 5 | 済 | コンシューマー 3 件の `_common.py` コメントを更新（テンプレートに合わせる） |
| 6 | 済 | ルール / CLAUDE.md を確認（変更不要）|

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` | 編集 | TRUTHY 定数追加、キルスイッチを依存チェック前に移動 | テンプレートなのでプレースホルダーのまま |
| 2 | `plugins/ref-inject/templates/hooks/scripts/_common.py` | 編集 | コメントブロック更新 | 〃 |
| 3 | `plugins/claude-kit/hooks/scripts/_common.py` | 編集 | コメントブロック更新 | コード本体は変更なし |
| 4 | `plugins/dev-kit/hooks/scripts/_common.py` | 編集 | コメントブロック更新 | 〃 |
| 5 | `plugins/work/hooks/scripts/_common.py` | 編集 | コメントブロック更新 | 〃 |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

このブランチのスコープの未決定事項なし。

## 参考ドキュメント

- `.work/notes/ref-inject.md`: ref-inject プラグインの設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
