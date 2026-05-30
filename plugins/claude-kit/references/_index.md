# claude-kit リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。カテゴリ別に分類。

---

## ファイル種別ガイド

Claude Code の設定ファイル（CLAUDE.md・rules・skills・hooks）を書くためのガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [common.md](common.md) | 全 Claude 設定オーサリングの共通ベース。ファイル種別の判定基準・増殖防止ガード・JP/EN ミラー規則 |
| 2 | [claude-md.md](claude-md.md) | CLAUDE.md（ルート / サブフォルダ）の作り方。読み込みタイミング・薄肉原則・抽出先ガイド |
| 3 | [rules.md](rules.md) | `.claude/rules/<name>.md` の作り方。ルールの種類・paths 設計・必須セクション |
| 4 | [skills.md](skills.md) | `.claude/skills/<name>/SKILL.md` の作り方。ステップ構造テンプレ・JP ミラー先行ワークフロー |
| 5 | [hooks.md](hooks.md) | プロンプト注入フックの作り方。フックイベント・注入メカニズム・ループ防止 |

---

## プラグイン開発

プラグイン構造・マニフェスト・オンボーディングスキルに関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [plugin-structure.md](plugin-structure.md) | プラグインの作成 / 更新の仕方。標準ディレクトリ構成・plugin.json フィールド・バージョンバンプ規則 |
| 2 | [plugin-claude-md.md](plugin-claude-md.md) | プラグインのルート CLAUDE.md の書き方。必須セクション・テーブル形式・コピペ用フルテンプレート |
| 3 | [setup-wizard.md](setup-wizard.md) | 必須スキル `setup-wizard` の書き方。SessionStart フックによる初回オンボーディング設計 |
| 4 | [plugin-config.md](plugin-config.md) | プラグインに config スキルを追加する方法。AskUserQuestion ループパターン・スコープ選択 |

---

## サブシステム・環境変数

サブエージェント委譲・環境変数による設定可能化に関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [subagents.md](subagents.md) | ステップ処理のサブエージェント委譲ガイド。委譲マーカー・委譲の判断基準・制約 |
| 2 | [environment.md](environment.md) | フック/スクリプトを環境変数で設定可能にする方法。settings.json の env ブロック・デフォルト/検証 |

---

## 同期・保守

ファイル間の同期ルール・インシデント記録に関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [references-sync.md](references-sync.md) | プラグインリファレンスファイルの JP ミラー同期ルール |
| 2 | [kit-hooks-sync.md](kit-hooks-sync.md) | dev-kit と claude-kit の注入インフラ構造同期ルール（inject_references.py / _index / _injection_rules を共有） |
| 3 | [incidents.md](incidents.md) | `.claude/rules/incidents.md` のフォーマットガイド。2 層構造（索引 + 詳細ファイル） |
