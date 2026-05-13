---
name: claude-rule
description: （日本語訳）Claude Code の設定・ドキュメント作業すべてのゲートウェイスキル。CLAUDE.md・SKILL.md・.claude/rules/ の作成・編集、ルール/スキル/フック/MCP の設定、ルールマーケットからのルールインストール、プロジェクトへの Claude Code セットアップ、規約の確認など、Claude Code に関するあらゆるリクエストで自動適用される。
---

> このファイルは `SKILL.md` の日本語翻訳です。Claude Code には自動読み込みされません。
> 変更する場合は、まずこのファイルを更新し、その後 `SKILL.md`（英語本体）にも同じ変更を反映してください。

---

# claude-rule — Claude Code 設定ゲートウェイ

Claude Code のドキュメント・設定作業すべてのエントリーポイント。記述規約を保持し、ニーズに応じて専門スキルに振り分ける。

---

## Step 0: まず公式ドキュメントを読む

作業前に最新仕様を確認すること。
公式 Claude Code ドキュメント: **https://code.claude.com/docs/**

| タスク | ドキュメント |
|---|---|
| スキル作成 | https://code.claude.com/docs/ja/skills |
| パスルール/メモリ | https://code.claude.com/docs/ja/memory |
| プラグイン開発 | https://code.claude.com/docs/ja/plugins |
| フック設定 | https://code.claude.com/docs/ja/hooks |
| MCP サーバー | https://code.claude.com/docs/ja/mcp |

**スキルを作る場合は `skill-creator` も合わせて読み込む。** 未インストールなら:
```
/plugin install skill-creator@claude-plugins-official
```

---

## 振り分けガイド

| ユーザーのニーズ | アクション |
|---|---|
| 実績あるルールをインストール | `/claude-rule:rule-market` |
| 新規プロジェクト固有のルール作成 | まず rule-market を確認、なければ `/rules-creator` |
| スキル作成・更新 | `skill-creator` をロード（未インストールなら先にインストール） |
| 既存の CLAUDE.md / SKILL.md / ルールの編集 | このスキルの規約をそのまま適用 |
| フック設定 | フックドキュメントを読んで `.claude/settings.json` を直接編集 |
| 新規プロジェクトへの Claude Code セットアップ | rule-market → CLAUDE.md 作成 の順 |

**rule-market vs rules-creator の使い分け:**
まず `/claude-rule:rule-market list` を実行。必要なルールがライブラリにあればインストールする。
市場に該当がない場合のみ rules-creator でゼロから作成する。

---

## 基本ルール

- **Claude が読むファイルはすべて英語で書く。** CLAUDE.md・SKILL.md・`.claude/rules/*.md` は自動ロードされる指示ファイル
- **英語ファイルごとに日本語ミラーを対にする。** ミラーは人間の著者用
- **英語本体の中に日本語コンテンツを書かない**
- **片方だけ更新してはいけない。常に両方を同期させる**

---

## ミラーファイルの置き場所

**ファイル名一致型（CLAUDE.md, SKILL.md）**: 同じディレクトリに `<basename>.jp.md` として置く

| 自動ロード（英語） | 人間ミラー（日本語） |
|---|---|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `SKILL.md` | `SKILL.jp.md` |

**再帰スキャン型（`.claude/rules/`）**: サフィックスに関係なくすべての `.md` をロードする。
`.jp.md` を `.claude/rules/` 内に置くと自動ロードされてしまう。**並列ディレクトリ**に隔離する:

| 自動ロード（英語） | 人間ミラー（日本語） |
|---|---|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |

`.claude/rules-jp/` は Claude Code がスキャンしないため、設定不要で除外される。

---

## 編集ワークフロー

1. **JP ミラーを先に更新** — 日本語で意図を確定させる
2. **英語本体を翻訳・更新** — 権威あるファイルに同じ変更を反映
3. **両ファイルを同じコミットに含める** — 片方だけのコミットは禁止

---

## XML タグによる構造明確化

Claude Code 指示ファイルには XML タグでセマンティックなセクション境界を明示する。
Claude は XML 構造で訓練されており、タグ付きセクションをより確実に解析できる。

**使う場面:** `CLAUDE.md`・`SKILL.md`・`.claude/rules/*.md`
**使わない場面:** JP ミラー・YAML/JSON データファイル・wiki ドキュメント

| タグ | 用途 |
|---|---|
| `<when_to_apply>` | 適用条件・スコープ |
| `<hard_rules>` | 絶対的なルール |
| `<steps>` | 順序付きの手順 |
| `<policy>` | 行動規範・ガイドライン |
| `<checklist>` | 完了条件リスト |
| `<dispatch_guide>` | サブスキルへの振り分け表 |
| `<references>` | wiki・ドキュメントへのリンク |

Markdown のヘッダーは人間の可読性のために残し、セクション本文を XML タグで囲む。

---

## CLAUDE.md vs `.claude/rules/` の使い分け

| 指示の種類 | 置き場所 |
|---|---|
| 毎セッション・全ファイルに適用 | `CLAUDE.md` |
| プロジェクトのメタワークフロー | `CLAUDE.md` |
| 特定フォルダ編集時だけ必要 | `.claude/rules/<name>.md`（`paths:` 付き） |
| あるフォルダを支配する仕様書リスト | `.claude/rules/<name>.md`（`paths:` 付き） |

CLAUDE.md は約200行以内に保つ。ドメイン固有の内容は path-scoped ルールに分ける。

---

## path-scoped ルールの2パターン

1. **プロセス/規約ルール** — そのフォルダでの作業方法（コーディング規約、チェックリストなど）。自己完結
2. **ソース ↔ ドキュメント紐付けルール** — そのフォルダを支配する wiki/spec への参照リスト。Claude がソースを編集するとき「この仕様が関係する」と即座に提示される

---

## メタルール：ルールファイルを編集するとき

1. ルールに参照されている wiki/docs と内容が整合しているか確認し、乖離があれば更新
2. `.claude/rules-jp/<同名>.md` を更新する
3. EN 本体 + JP ミラーを同じコミットに含める

---

## ファイルまとめ

| ファイル | 言語 | 自動ロード | 目的 |
|---|---|---|---|
| `CLAUDE.md` | 英語 | はい | プロジェクト全体の指示 |
| `CLAUDE.jp.md` | 日本語 | いいえ | 人間向け参照 |
| `SKILL.md` | 英語 | はい | スキル定義 |
| `SKILL.jp.md` | 日本語 | いいえ | 人間向け参照 |
| `.claude/rules/<name>.md` | 英語 | はい（パスマッチ or 常時） | スコープ指定/常時ルール |
| `.claude/rules-jp/<name>.md` | 日本語 | いいえ | ルールの人間向け参照 |
