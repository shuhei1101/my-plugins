# dev-kit — 開発規約統合プラグイン

Python / HTML-CSS-JS / Next.js 16 App Router / Markdown を 1 プラグインに統合。
リファレンス自動注入はファイル編集時に自動発火する（lang の env opt-in は不要）。

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
| `dev-kit:plugin-migrate` | プロジェクトに展開済みの dev-kit 生成物（html-implement のルール / html-debug-fab のウィジェット）をインストール済み dev-kit のバージョンに同期する（手動 `/dev-kit:plugin-migrate` のみ） |
| `dev-kit:plugin-config` | dev-kit の env トグル（TypeScript チェック等）をインタラクティブに設定 |

## フック

リファレンス自動注入は `hooks/ref-inject/`（`main.py` + `references/` + 実行時生成の `cache.yaml`）に集約。
その他のフックは `hooks/scripts/` 配下、共通ヘルパは `_common.py`。

| フック | トリガー | 用途 |
|---|---|---|
| `ref-inject/main.py` | PreToolUse(Edit/Write/Read) | リファレンス自動注入（各リファレンスファイルのフロントマターで制御） |
| `scripts/references_edit_guard.py` | PreToolUse(Edit/Write) | references 編集時にフロントマター記述漏れをリマインド |
| `scripts/ts_check.py` | PostToolUse(Edit/Write) | `*.ts` / `*.tsx` に対する `tsc --noEmit --incremental` |
| `scripts/_common.py` | — （ライブラリ） | stdin 読み・env truthy 判定・once-per-session トークン・block 理由出力 |

## env トグル

`settings.json` の `env` （またはユーザー `~/.claude/settings.json`）に設定。
truthy = `true`/`1`/`yes`/`on`（大文字小文字無視）、falsy = それ以外。

**太字** = デフォルト値（キー未設定時に適用）。

| 変数名 | 説明 | 値 |
|---|---|---|
| `${DEV_KIT_NEXT_TS_CHECK}` | `*.ts` / `*.tsx` 編集後に `tsc --noEmit` チェックを実行するか | - **true**<br>- false |
| `${DEV_KIT_INJECTION_DISABLE}` | キルスイッチ — truthy で全リファレンス注入を停止 | - true<br>- **false** |
| `${DEV_KIT_INJECTION_TTL}` | リファレンスのトークンキャッシュ TTL。秒（整数） | **3600** |

## リファレンス構造

```
hooks/ref-inject/
├── main.py          # フロントマター判定 + 注入スクリプト
├── cache.yaml       # フロントマターのメタキャッシュ（実行時自動生成・gitignore）
└── references/
    ├── claude/      # Claude Code 全般（フック・ルール記述など）
    ├── dev/         # 開発全般（コーディング規約・YAML SoT・タイムスタンプ等）
    ├── html/        # HTML/CSS/JS 規約
    ├── markdown/    # Markdown 規約
    ├── next/        # Next.js 規約
    ├── python/      # Python 規約
    └── skill/       # スキル設計
```

各リファレンスファイルの先頭に YAML フロントマターでトリガーを記述する:

```yaml
---
paths:
  - **/*.py            # クォート有無どちらでも可
  - "**/foo.py"
required: false        # 省略時 true。false なら paths にマッチしても注入しない
tools: [e, w]          # 省略時 [Edit, Write]。e/w/r・edit/write/read・大小文字可
---
```

- **paths**: トリガーする glob パターンの配列。ダブルクォート省略可。
- **required**: 注入するか否かの単一の真偽値（既定 true）。`false` ならマッチしても注入しない（optional 概念は廃止）。
- **tools**: 発火するツール。省略時 `[Edit, Write]`（Read では発火しない）。`e`/`w`/`r`、`edit`/`write`/`read`、大文字小文字を吸収。

`main.py` は references/ を走査してフロントマターを `cache.yaml` にキャッシュし、以後はそれを読む。
**references を更新したら `cache.yaml` を削除すれば再生成される。**
注入は `~/.claude/tokens/dev-kit/{session_id}.yaml` の TTL トークンで二重注入を防ぐ。

## Changelog

| Version | Date | Summary |
|---|---|---|
| 4.17.0 | 2026-06-10 | リファレンス注入を `hooks/ref-inject/`（`main.py` + `references/` + `cache.yaml`）に集約。`~/.claude/rules`（claude/dev/html/markdown/next/python/skill）を取り込み。required を単一真偽値化（optional 概念を廃止）。paths のクォート省略・tools エイリアス（e/w/r）対応。Jinja2 テンプレートを廃止。存在しない `MultiEdit` 参照を全削除 |
| 4.16.0 | 2026-06-10 | `_injection_rules.yaml` / `_index.yaml` を廃止し、各リファレンスファイルの YAML フロントマター（paths / required / tools）で注入ルールを管理する設計に変更。`lang` env トグルを廃止。`[id]` glob バグを修正 |
| 4.15.0 | 2026-06-02 | `dev-kit:plugin-config` スキルを復活 — 言語 opt-in / 機能トグルのインタラクティブな env 設定 |
| 4.14.0 | 2026-06-02 | 対話式 `dev-kit:plugin-config` スキルを削除。env トグルのテーブルを統一 3 列形式（変数名 / 説明 / 値、デフォルトは太字）に再フォーマット |
| 4.13.0 | 2026-06-01 | `dev-kit:setup-wizard` スキルと `SessionStart` フック（`setup_check.py`）を削除 |
| 4.11.1 | 2026-05-31 | `plugin-migrate` のブランチチェックステップ（master/main ガード）を削除 — work ハーネスの UserPromptSubmit フックと責務が重複しているため |
| 4.11.0 | 2026-05-31 | `dev-kit:plugin-config` スキルを追加 — 6 つの env トグル（`DEV_KIT_PYTHON/HTML/NEXT/MARKDOWN` opt-in + `DEV_KIT_NEXT_TS_CHECK/MARKDOWN_CHECK` デフォルト ON）を番号付きリストループで対話的に設定 |
| 4.10.0 | 2026-05-31 | `markdown_frontmatter_check.py` フックを削除。ルールは `**/*.md` 編集時の `references/markdown/マークダウン編集.md` 自動注入で代替 |
| 4.9.0 | 2026-05-31 | `references-edit-guard` PreToolUse フックを追加。`references/` 配下のファイルを編集する直前に `_index.yaml` / `_injection_rules.yaml` の更新リマインド |
| 4.8.0 | 2026-05-31 | `dev-kit:yaml` スキル・`references/yaml/`・`yaml_skill_dispatch.py` フック削除 |
| 4.0.0 | 2026-05-30 | `py-kit` / `html-kit` / `next-kit` を `dev-kit` に統合 |
