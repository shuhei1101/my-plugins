<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# dev-kit — 開発規約統合プラグイン

Python / HTML-CSS-JS / Next.js 16 App Router / YAML を 1 プラグインに統合。
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
| `dev-kit:yaml` | YAML 規約 |
| `dev-kit:plugin-update` | プロジェクトに展開済みの dev-kit 生成物（html-implement のルール / html-debug-fab のウィジェット）をインストール済み dev-kit のバージョンに同期する（手動 `/dev-kit:plugin-update` のみ） |

## フック

| フック | トリガー | 用途 |
|---|---|---|
| `inject_references.py` | PreToolUse(Edit/Write/MultiEdit/Read) | 言語ごとのリファレンス自動注入 |
| `ts_check.py` | PostToolUse(Edit/Write/MultiEdit) | `*.ts` / `*.tsx` に対する `tsc --noEmit --incremental` |
| `yaml-skill-dispatch` | PreToolUse(Edit/Write) | YAML 編集時に `dev-kit:yaml` 起動をリマインド |

## env トグル

`settings.json` の `env` （またはユーザー `~/.claude/settings.json`）に設定。
truthy = `true`/`1`/`yes`/`on`（大文字小文字無視）、falsy = それ以外。

### 言語 opt-in（リファレンス自動注入）

| env 変数 | デフォルト | 効果 |
|---|---|---|
| `DEV_KIT_PYTHON` | OFF | `*.py` 等を編集した時に Python リファレンスを注入 |
| `DEV_KIT_HTML` | OFF | `*.html` / `*.css` / `*.js` 編集時に HTML リファレンス注入 |
| `DEV_KIT_NEXT` | OFF | `*.ts` / `*.tsx` 等の編集時に Next.js リファレンス注入 |

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
├── yaml.md      # YAML 規約
├── index.yaml   # 各リファレンスの path + lang + description
├── injection_rules.yaml   # 各ルールの pattern + lang + required/optional
└── ...
```

`injection_rules.yaml` の各ルールは `lang: python|html|next` を持つ。env で OFF の lang のルールは
フックがスキップする。`~/.claude/tokens/dev-kit/{session_id}.yaml` の TTL トークンで二重注入を防ぐ。

## Changelog

| Version | Date | Summary |
|---|---|---|
| 4.1.0 | 2026-05-30 | `dev-kit:plugin-update` スキルを追加 — html-implement のルールテンプレと html-debug-fab のウィジェットをプロジェクトに再同期する。自己完結設計: workspace 等の他プラグインに依存しない / master・main では実行を拒否 / スキル自身はコミットしない（PR182） |
| 4.0.0 | 2026-05-30 | `py-kit` / `html-kit` / `next-kit` を `dev-kit` に統合。言語別の opt-in トグル `DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT` を導入（PR166） |
