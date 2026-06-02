<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# claude-kit プラグイン開発者ガイド

## オーサリング知識は `references/` にあり、自動注入される

各指示ファイル種別のオーサリングガイドは `references/`（`common.md`, `skills.md`,
`rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`, `glossary.md` /
`incidents.md`）にある。
`claude-kit-references-injection` フック（`hooks/scripts/inject_references.py`）が、対応するファイル
（`SKILL.md` / ルール / `CLAUDE.md` / `hooks.json` / `plugin.json` …）を編集したとき、該当ガイドを
**本文全量**で注入する。パス → reference の対応は `references/_injection_rules.yaml` 参照。

- creator スキル（`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` /
  `plugin-creator`）は references に委譲する**薄いラッパー**。対象ファイルを直接編集すれば
  ガイドが注入される。ラッパーは明示起動と呼び出し元のために残している。
- **Step 0 で他スキルを読み込まない** — スキルの起動時読み込みは 2500 × N トークンを消費する。
  注入機構が旧来の「Step 0: 背景資料を読む」パターンを置き換える。

この注入構造は全 `*-kit` プラグイン（dev-kit / claude-kit）で共通 — `kit-hooks-index-sync`
ルール参照。プラグインへの付与は `/ref-inject:apply <plugin>`。機構をプラグインごとに手編集しない
（`ref-inject` テンプレを変えて再適用する）。

## スキル

| スキル | 目的 |
|---|---|
| `claude-kit:claude-creator` | `CLAUDE.md` ファイルを作成 |
| `claude-kit:claude-refactor` | 既存の `CLAUDE.md` ファイルをリファクタ |
| `claude-kit:rule-creator` | パススコープのルールを作成 |
| `claude-kit:skill-creator` | スキルを作成 |
| `claude-kit:hook-creator` | プロンプト注入フックを作成 |
| `claude-kit:plugin-creator` | プラグインを作成・更新 |
| `claude-kit:plugin-migrate` | プラグインレベルの成果物を現在の claude-kit 規約に同期 |
| `claude-kit:jp-mirror-sync` | 英語原本から JP ミラーファイル（`.jp.md`）を同期 |
| `claude-kit:env-sync` | プラグインファイル間で env 変数宣言を同期 |
| `claude-kit:statusline-setup` | Claude Code のステータスラインを設定 |
| `claude-kit:plugin-config` | claude-kit の env 変数（JP ミラー / 注入言語 / TTL）をインタラクティブに設定 |

## フック

claude-kit のフックは 1 つだけ: `claude-kit-references-injection` フック
（`hooks/scripts/inject_references.py`, `PreToolUse(Edit | Write | MultiEdit | Read)`）。
**ディスパッチ/チェック系ガードは無い** — リファレンス注入へ寄せて廃止した
（creator-dispatch は PR159、`j2-stamp-check` と PostToolUse の `jp-mirror-check` は PR161）。
JP ミラー同期はプロジェクトの `*-jp-mirror-sync` ルールで担保。

> 今後ガード系フックを戻すときの一般指針: `UserPromptSubmit`（ユーザー入力テキストしか見ない）でなく
> `PreToolUse` を使う。セッション単位フラグ（`/tmp/{hook}-{session_id}`）でセッション 1 回だけ発火させる。
> ロジックはインライン `-c` でなくスクリプトファイルに抽出する（インライン python はクォートのネストで
> 壊れやすい — incident `statusline-python-quote-nesting`）。フックスクリプトは `hooks/scripts/` 配下に置き、
> 共通ヘルパーは plugin 内 `_common.py` に集約する（PR180 で導入）。

## 環境変数

**太字** = デフォルト値（キー未設定時に適用）。真偽値は `true` / `false` のみ記載（`1` / `yes` / `on` も truthy として扱われる）。

| 変数名 | 説明 | 値 |
|---|---|---|
| `${CLAUDE_KIT_INJECTION_DISABLE}` | マスターキルスイッチ — truthy で注入機構全体を停止 | - true<br>- **false** |
| `${CLAUDE_KIT_INJECTION_TTL}` | セッション単位注入トークンの TTL（patterns / references 共通）。秒（整数） | **3600** |
| `${CLAUDE_KIT_INJECTION_LANG}` | 注入リファレンスの言語（`jp` で `index.jp.yaml` + `injection.jp.md.j2` を使用） | - **en**<br>- jp |
| `${CLAUDE_KIT_JP_MIRROR}` | `false` で `.jp.md` ミラーを作らず本体 `.md` を日本語で直接書く | - **true**<br>- false |

## 変更履歴

| # | バージョン | 概要 |
|---|---|---|
| 1 | `3.55.0` | `claude-kit:plugin-config` スキルを復活（`config` からリネーム）。`プラグイン設定.md` 記述ガイドと `プラグイン構造.md` の `plugin-config` 必須記載を復元。SKILL.md / plugin.json パターンの注入ルールに追加 |
| 2 | `3.54.0` | 対話式 `work:plugin-config` / `dev-kit:plugin-config` スキルと config スキル記述ガイド `プラグイン設定.md` を削除。`plugin-creator` / `プラグイン構造.md` から `plugin-config` 必須記載を除去。`プラグインCLAUDE-md.md` の env テーブル仕様を統一 3 列形式（変数名 / 説明 / 値、デフォルトは太字）に再定義し各プラグインの `## 環境変数` テーブルを再フォーマット |
| 2 | `3.53.0` | `claude-kit:config` スキルを削除 |
| 3 | `3.52.0` | `claude-kit:jp-mirror-sync` スキルを追加（`utils` プラグインから移動）；`utils` プラグインを marketplace から削除 |
| 4 | `3.51.0` | `claude-kit:setup-wizard` スキルと `SessionStart` フック（`setup_check.py`）を削除 |
| 5 | `3.49.1` | `plugin-migrate` のブランチチェックステップ（master/main ガード）を削除 — work ハーネスの UserPromptSubmit フックと責務が重複しているため |
| 6 | `3.48.0` | `references/` をロール別サブフォルダ（`common/`・`skill/`・`hook/`・`claude-md/`・`plugin/`）に再編；`plugin/バージョン同期.md` を追加；`plugins/*/CLAUDE.md` 編集時にバージョン同期リマインダーを注入 |
| 7 | `3.47.0` | `references/jinja2/templates.md` を追加 — Markdown を出力する Jinja2 テンプレートのオーサリングルール；`**/hooks/templates/*.j2` 編集時に自動注入 |
| 8 | `3.46.0` | `references-edit-guard` PreToolUse フックを追加 — `references/` 編集前に `_index.yaml` / `_injection_rules.yaml` の更新漏れをリマインド |
| 9 | `3.44.0` | `${CLAUDE_KIT_JP_MIRROR}` 環境変数を追加 — `false` の場合 `.jp.md` ミラーをスキップし本体ファイルを日本語で書く |
| 10 | `3.43.0` | `references/` 配下のメタ YAML をアンダースコア接頭辞付きにリネーム；ドキュメントの plugin 名整理 (PR179) |
| 11 | `3.42.0` | `${CLAUDE_KIT_INJECTION_DISABLE}` kill switch 環境変数を追加 |
