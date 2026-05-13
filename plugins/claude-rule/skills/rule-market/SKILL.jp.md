---
name: rule-market
description: （日本語訳）Claude Code プロジェクト向けのルールライブラリ・インストーラー。「ルールマーケット」「ルールをインストール」「ルールを追加したい」などで起動。利用可能なルールの一覧表示、プロジェクトへのインストール、編集したルールのライブラリへの同期ができる。
---

> このファイルは `SKILL.md` の日本語翻訳です。Claude Code には自動読み込みされません。
> 変更する場合は、まずこのファイルを更新し、その後 `SKILL.md`（英語本体）にも同じ変更を反映してください。

---

# rule-market — Claude Code プロジェクト向けルールライブラリ

このプラグインのライブラリから、実績のあるプロジェクト非依存のルールをインストールする。
新しいルールをゼロから作る前に、まずここで検索する。

---

## 利用可能なルール

| ルール名 | 対象パス | 説明 |
|---|---|---|
| `cascade-sync` | `**/*` | ルール・wiki・JP ミラーを編集のたびに同期させる |
| `auto-register` | `**/*` | 編集するファイルが path-scoped ルールでカバーされているか確認する |

> `rule-market-managed` は選択したルールと必ず一緒にインストールされる（管理用ルール）

---

## 操作

### `list` — ルールライブラリの一覧表示

上の表を表示する。ファイルは作成しない。

### `install <rule-name>` または `install-all` — プロジェクトへ展開

1. **対象プロジェクトを特定。** カレントディレクトリ（`$PWD`）をプロジェクトルートとして使用。worktree や サブディレクトリの場合は確認する
2. **競合チェック。** 同名ファイルが `PROJECT/.claude/rules/` に存在する場合は差分を表示して確認する
3. ルールテンプレートを `PROJECT/.claude/rules/<rule-name>.md` に書き込む
4. JP ミラーを `PROJECT/.claude/rules-jp/<rule-name>.md` に書き込む
5. `rule-market-managed.md` が未インストールなら一緒に配置する
6. `CLAUDE.md` に `Folder-scoped rules` テーブルがあれば行を追加する
7. 作成したファイルを報告する

### `sync <rule-name>` — プロジェクトでの編集をライブラリに戻す

プロジェクトでカスタマイズしたルールを、プラグインのテンプレートに反映させたいときに使う。

1. 同期スクリプトを探す:
   ```powershell
   Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" |
     Where-Object { $_.FullName -like "*claude-rule*" }
   ```
2. 実行する:
   ```
   python <script-path> sync <project-root> <rule-name>
   ```
3. JP ミラー（`rules-jp/`）の更新とプラグインバージョンバンプをユーザーに案内する

---

## ルールテンプレートについて

各ルールのテンプレートは `SKILL.md`（英語本体）にインラインで埋め込まれています。
人間が読める形式のソースは `skills/rule-market/rules/` フォルダに、JP ミラーは `rules-jp/` フォルダにあります。
