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
| 済 | QA を記録する | - |
| 済 | `.jp.md` ファイルの除外条件を追加する | - `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` |
| 済 | `Edit` / `MultiEdit` ツールのチェックを除外する（`Write` のみチェック） | - 〃 |
| 済 | ノートを更新する | - `.work/notes/dev-kitフック設計メモ.md` |
| 済 | ルール / CLAUDE.md を確認・更新する（変更不要と判断） | - |
| 済 | `markdown_frontmatter_check.py` フックを削除し、リファレンス文書に一本化する | - `plugins/dev-kit/hooks/hooks.json`<br>- `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` | 削除 | フック廃止 | 注入で代替 |
| 2 | `plugins/dev-kit/hooks/hooks.json` | 編集 | `markdown_frontmatter_check` エントリ削除 | - |
| 3 | `plugins/dev-kit/CLAUDE.md` | 編集 | フック一覧・`DEV_KIT_MARKDOWN_CHECK` 行削除、v4.10.0 履歴追加 | - |
| 4 | `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 4.9.0 → 4.10.0 | - |
| 5 | `plugins/dev-kit/changelogs/v4.10.0.md` | 新規 | changelog 追加 | - |
| 6 | `.claude-plugin/marketplace.json` | 編集 | dev-kit バージョン 4.9.0 → 4.10.0 | - |

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
