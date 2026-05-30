<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# dev-kit — 開発規約統合プラグイン

Python / HTML-CSS-JS / Next.js 16 App Router / YAML / Markdown を 1 プラグインに統合。
リファレンス自動注入は `settings.json` の env で言語ごとに opt-in する。

## スキル

| スキル | 用途 |
|---|---|
| `dev-kit:py-script` | 単一ファイル / 数ファイル Python スクリプトのスキャフォールド |
| `dev-kit:py-project` | Python プロジェクトのスキャフォールド（機能フォルダ型レイアウト / 関数ファースト） |
| `dev-kit:html-implement` | UI 画面実装ワークフロー（FLOCSS + デザイントークン） |
| `dev-kit:html-logging` | フロントエンドロガー整備 |
| `dev-kit:html-mock` | UI モック生成 |
| `dev-kit:html-debug-fab` | 開発用フローティングデバッグボタン（FAB） |
| `dev-kit:next-implement` | Next.js 実装ワークフロー |
| `dev-kit:next-plan` | Next.js 計画ドキュメント生成 |
| `dev-kit:plugin-update` | プロジェクトに展開済みの dev-kit 生成物（html-implement のルール / html-debug-fab のウィジェット）をインストール済み dev-kit のバージョンに同期する（手動 `/dev-kit:plugin-update` のみ） |

## フック

フックスクリプトは `hooks/scripts/` 配下に集約し、共通ヘルパは plugin 内 `_common.py` に置く。

| フック | トリガー | 用途 |
|---|---|---|
| `scripts/inject_references.py` | PreToolUse(Edit/Write/MultiEdit/Read) | 言語ごとのリファレンス自動注入 |
| `scripts/ts_check.py` | PostToolUse(Edit/Write/MultiEdit) | `*.ts` / `*.tsx` に対する `tsc --noEmit --incremental` |
| `scripts/_common.py` | — （ライブラリ） | stdin 読み・env truthy 判定・once-per-session トークン・block 理由出力 |

## env トグル

`settings.json` の `env` （またはユーザー `~/.claude/settings.json`）に設定。
truthy = `true`/`1`/`yes`/`on`（大文字小文字無視）、falsy = それ以外。

### 言語 opt-in（リファレンス自動注入）

| env 変数 | デフォルト | 効果 |
|---|---|---|
| `DEV_KIT_PYTHON` | OFF | `*.py` 等を編集した時に Python リファレンスを注入 |
| `DEV_KIT_HTML` | OFF | `*.html` / `*.css` / `*.js` 編集時に HTML リファレンス注入 |
| `DEV_KIT_NEXT` | OFF | `*.ts` / `*.tsx` 等の編集時に Next.js リファレンス注入 |
| `DEV_KIT_MARKDOWN` | OFF | `*.md` 編集時に Markdown リファレンス注入 |

デフォルトは **全 OFF**。プロジェクトで使用する言語のみ明示的に有効化する。

### その他のトグル

| env 変数 | デフォルト | 効果 |
|---|---|---|
| `DEV_KIT_NEXT_TS_CHECK` | ON | `*.ts` / `*.tsx` 編集後の `tsc --noEmit` チェック |
| `DEV_KIT_INJECTION_DISABLE` | OFF | **truthy** で全リファレンス注入を停止（緊急停止） |
| `DEV_KIT_INJECTION_TTL` | 3600（秒） | パターン / リファレンスのトークンキャッシュ TTL |
| `DEV_KIT_INJECTION_LANG` | `en` | `jp` で日本語版リファレンスを注入 |

## リファレンス構造

```
references/
├── python/      # Python 規約（47ファイル: architecture/, core/, fastapi/, llm/ など）
├── html/        # HTML/CSS/JS 原則（principles.md, ui-design.md）
├── next/        # Next.js 規約（90ファイル: backend/, frontend/, testing/ など）
├── markdown/    # Markdown 規約（markdown-table.md, markdown-editing.md）
├── _index.yaml   # 各リファレンスの path + lang + description
├── _injection_rules.yaml   # 各ルールの pattern + lang + required/optional
└── ...
```

`_injection_rules.yaml` の各ルールは `lang: python|html|next|markdown` を持つ。env で OFF の lang のルールは
フックがスキップする。`~/.claude/tokens/dev-kit/{session_id}.yaml` の TTL トークンで二重注入を防ぐ。

## Changelog

| Version | Date | Summary |
|---|---|---|
| 4.11.0 | 2026-05-31 | `dev-kit:config` スキルを追加 — 6 つの env トグル（`DEV_KIT_PYTHON/HTML/NEXT/MARKDOWN` opt-in + `DEV_KIT_NEXT_TS_CHECK/MARKDOWN_CHECK` デフォルト ON）を番号付きリストループで対話的に設定（PR229） |
| 4.10.0 | 2026-05-31 | `markdown_frontmatter_check.py` フックを削除。ルールは `**/*.md` 編集時の `references/markdown/markdown-editing.md` 自動注入で代替（PR228） |
| 4.9.0 | 2026-05-31 | `references-edit-guard` PreToolUse フックを追加（ref-inject v1.7.0 経由）。`references/` 配下のファイルを **編集／作成する直前** に `_index.yaml` / `_injection_rules.yaml` の更新も忘れていないかリマインド（PR206） |
| 4.8.0 | 2026-05-31 | `dev-kit:yaml` スキル・`references/yaml/`・`yaml_skill_dispatch.py` フック（+ プロンプト）を削除; `**/index.yaml` / `**/settings.yaml(.sample)` の注入パターンも削除; YAML 規約は dev-kit の対象外（PR202） |
| 4.7.0 | 2026-05-31 | Markdown フロントマター配置チェックフックとリファレンスを追加; `markdown-editing.md` を `markdown/` サブフォルダへ移動; `markdown-table.md` と並んで `_injection_rules.yaml` に登録; `DEV_KIT_MARKDOWN` opt-in サポートを追加（PR198） |
| 4.6.0 | 2026-05-30 | `yaml.md` / `yaml.jp.md` を `yaml/` サブフォルダへ移動し、`html/`・`next/`・`python/`・`markdown/` と構造を統一; `yaml/yaml.md` を `_index.yaml` に登録し `**/index.yaml` / `**/settings.yaml(.sample)` の注入ルールを追加（PR199） |
| 4.5.0 | 2026-05-30 | `css-js-link.md` / `common-component-first.md` を `templates/html/rules/` から `references/html/` へ移動し `_injection_rules.yaml` の html パターンに紐付け; `html-implement`（ステップ7）と `plugin-update`（ステップ2）の静的コピー手順を削除（PR200） |
| 4.4.0 | 2026-05-30 | `markdown/` リファレンスサブフォルダを追加。Markdown テーブル規約（`#` カラムルール・`〃` ダイトーマーク）を収録し、`**/*.md` 編集時に注入（PR196） |
| 4.3.0 | 2026-05-30 | `dev-kit:plugin-update` スキルを追加 — dev-kit 生成物（静的テンプレ + 規約遵守ソースファイル）を現バージョンの規約に検査・修正する。自己完結設計: 他プラグインに依存しない / master・main では実行拒否 / スキル自身はコミットしない（PR182） |
| 4.2.0 | 2026-05-30 | `references/` 配下のメタ系 YAML を `_` 接頭辞付きにリネーム: `index.yaml` / `index.jp.yaml` / `injection_rules.yaml` → `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml`（PR179） |
| 4.1.0 | 2026-05-30 | フックスクリプトを `hooks/scripts/` 配下へ移動し共通ヘルパ `_common.py` を導入。挙動変更なし（PR180） |
| 4.0.0 | 2026-05-30 | `py-kit` / `html-kit` / `next-kit` を `dev-kit` に統合。言語別の opt-in トグル `DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT` を導入（PR166） |
