# claude-kit リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。カテゴリ別に分類。

---

## ファイル種別ガイド

Claude Code の設定ファイル（CLAUDE.md・rules・skills・hooks）を書くためのガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [共通ガイド.md](common/共通ガイド.md) | 全 Claude 設定オーサリングの共通ベース。ファイル種別の判定基準・増殖防止ガード・JP/EN ミラー規則 |
| 2 | [CLAUDE-md記述ガイド.md](claude-md/CLAUDE-md記述ガイド.md) | CLAUDE.md（ルート / サブフォルダ）の作り方。読み込みタイミング・薄肉原則・抽出先ガイド |
| 3 | [記述ルール.md](claude-md/記述ルール.md) | `.claude/rules/<name>.md` の作り方。ルールの種類・paths 設計・必須セクション |
| 4 | [スキル.md](skill/スキル.md) | `.claude/skills/<name>/SKILL.md` の作り方。ステップ構造テンプレ・JP ミラー先行ワークフロー |
| 5 | [フック.md](hook/フック.md) | プロンプト注入フックの作り方。フックイベント・注入メカニズム・ループ防止 |
| 6 | [AskUserQuestion制約.md](common/AskUserQuestion制約.md) | スキルから AskUserQuestion を呼ぶ条件と方法。使用制限（スキル/ユーザーの明示指示時のみ）・options 制約（2〜4 個・Other 自動付与）・multiSelect・preview |

---

## プラグイン開発

プラグイン構造・マニフェスト・オンボーディングスキルに関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [プラグイン構造.md](plugin/プラグイン構造.md) | プラグインの作成 / 更新の仕方。標準ディレクトリ構成・plugin.json フィールド・バージョンバンプ規則 |
| 2 | [プラグインCLAUDE-md.md](plugin/プラグインCLAUDE-md.md) | プラグインのルート CLAUDE.md の書き方。必須セクション・テーブル形式・コピペ用フルテンプレート |
| 3 | [プラグイン設定.md](plugin/プラグイン設定.md) | プラグインに config スキルを追加する方法。AskUserQuestion ループパターン・スコープ選択 |
| 4 | [バージョン同期.md](plugin/バージョン同期.md) | plugin.json / marketplace.json / CLAUDE.md のバージョン同期不変条件。プリコミットチェックリスト・バンプ規則 |

---

## サブシステム・環境変数

サブエージェント委譲・環境変数による設定可能化に関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [サブエージェント.md](common/サブエージェント.md) | ステップ処理のサブエージェント委譲ガイド。委譲マーカー・委譲の判断基準・制約 |
| 2 | [環境変数.md](common/環境変数.md) | フック/スクリプトを環境変数で設定可能にする方法。settings.json の env ブロック・デフォルト/検証 |
| 3 | [環境変数記法.md](common/環境変数記法.md) | スキル・ルール・CLAUDE.md・プロンプト内での環境変数名の記法ルール。`${VAR_NAME}` 記法・ALL_CAPS_SNAKE_CASE・ドキュメントテーブル形式 |

---

## テンプレート作成

Jinja2 テンプレートのオーサリングに関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [テンプレート注意点.md](hook/jinja2/テンプレート注意点.md) | Markdown を出力する Jinja2 テンプレート（injection.md.j2 等）のオーサリング規則。trim_blocks の改行食い・`{% endif %}{% if X %}` + `---` setext 見出しバグ・`}}` と Handlebars パーサ衝突（`<!-- -->` で回避）・チェックリスト |
| 2 | [執筆ガイド.md](hook/jinja2/執筆ガイド.md) | Jinja2 テンプレートオーサリングの落とし穴。trim_blocks=True + lstrip_blocks=True 時の既知トラップ — setext 見出し・ATX 見出し内 `{{ expr }}`・ブロックタグ周辺の空行・インデント消失 |

---

## 同期・保守

ファイル間の同期ルールに関するガイド。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [リファレンス同期.md](common/リファレンス同期.md) | プラグインリファレンスファイルの JP ミラー同期ルール |
| 2 | [キットフック同期.md](hook/キットフック同期.md) | dev-kit と claude-kit の注入インフラ構造同期ルール（inject_references.py / _index / _injection_rules を共有） |
