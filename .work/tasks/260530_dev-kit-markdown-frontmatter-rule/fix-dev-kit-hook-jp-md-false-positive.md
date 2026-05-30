# fix/dev-kit-hook-jp-md-false-positive

> 内部 ID: 228（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`dev-kit` の `markdown_frontmatter_check.py` が `.jp.md` ファイルや Edit 操作の断片に対して誤って advisory を出すバグを修正する。

**バグの内容（2 件）:**
1. `.jp.md` ファイルを除外していない — JP ミラーは仕様上 HTML コメントがフロントマター前に来るが、これを「違反」と判定する
2. `Edit` / `MultiEdit` ツールでも `new_string`（ファイル断片）をチェックしている — 断片に `---` が含まれると誤検知する

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を記録する | - |
| - | `.jp.md` ファイルの除外条件を追加する | - `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` |
| - | `Edit` / `MultiEdit` ツールのチェックを除外する（`Write` のみチェック） | - 〃 |
| - | ノートを更新する | - `.work/notes/dev-kit-plugin.md` |
| - | ルール / CLAUDE.md を確認・更新する | - |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` | 編集 | `.jp.md` 除外・Edit 除外の条件追加 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| - | （テスト変更なし） | - | - | - |

## QA

なし

## 参考ドキュメント

- `.work/notes/dev-kit-plugin.md`: dev-kit プラグインの設計メモ

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| feat/dev-kit-markdown-frontmatter-rule (#198) | このチェックを実装したブランチ |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
