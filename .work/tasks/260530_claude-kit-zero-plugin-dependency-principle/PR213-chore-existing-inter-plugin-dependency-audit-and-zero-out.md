# PR213 — existing-inter-plugin-dependency-audit-and-zero-out

## 概要

全プラグインの `skills/`・`hooks/`・`references/` を一括 grep し、他プラグインのスキル・コマンド・スクリプトパスを呼び出している箇所をリストアップ。ユーザーへのレビュー提示後、可能なものから順次「プラグイン内自己完結」へ書き換え、最終的にプラグイン間依存件数ゼロを目指す。

### 背景（PR210 から引き継ぎ）

PR210 で `plugins/claude-kit/references/plugin-structure.md`（+ jp）に `## Zero inter-plugin dependency principle` セクションを追加し、**全プラグインの判断軸**として整備した。本 PR はその原則に照らした棚卸しの実施 PR。

PR210 で定義した「許容される例外」:
- 同プラグイン内のスキル同士の呼び出し
- `ref-inject:apply` による静的テンプレ展開（配布先で閉じる）
- `claude-kit` の references injection 機構（opt-in 型）

上記以外に他プラグインへ参照している箇所は、今 PR で「プラグイン内自己完結」に書き換える。

### 実施条件

即時実施可（PR210 マージ済）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を `## QA` に記録する | - 本ドキュメント |
| - | `.work/notes/` の関連ノートを更新する | - `zero-plugin-dependency.md`（新規） |
| - | grep で他プラグイン呼び出しを全件リストアップしユーザーに提示 | - `plugins/**/skills/**`<br>- `plugins/**/hooks/**`<br>- `plugins/**/references/**` |
| - | 許容例外に該当するか判定し、違反箇所を確定する | - 各ファイル |
| - | 違反箇所をプラグイン内自己完結に書き換え（ユーザー確認後） | - 各ファイル |
| - | 必要に応じてバージョンバンプ（PATCH） | - 対象プラグインの `plugin.json`・`marketplace.json` |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md` — プラグイン間依存ゼロ原則（判断軸）
- `.work/notes/zero-plugin-dependency.md` — 棚卸し作業ノート（新規作成予定）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #210 | claude-kit plugin-structure にプラグイン間依存ゼロ原則セクション追加（本 PR の判断軸） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
