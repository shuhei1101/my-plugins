# dev-kit: リファレンスフロントマター方式への移行

## 概要

`_injection_rules.yaml` / `_index.yaml` の一元管理を廃止し、各リファレンスファイルが自身の注入ルールをフロントマターで保持する設計に変更した（v4.16.0）。

## 新フロントマター形式

```yaml
---
paths:
  - "**/*.py"                      # required: true（デフォルト）
  - pattern: "**/shared/types.py"
    required: false                # optional 扱い
tools: [Edit, Write, Read]         # 省略時は Edit/Write/MultiEdit/Read 全部
---
```

- `paths` が required のデフォルトを true にする。optional にしたいパターンはオブジェクト形式で `required: false` を明示
- `tools` 省略時は全ツール対象

## 廃止したもの

| 廃止 | 理由 |
|---|---|
| `references/.ref-inject/_injection_rules.yaml` | 各ファイルのフロントマターに移行 |
| `references/.ref-inject/_index.yaml` | description はファイルの `# 見出し` から自動取得 |
| `lang` env トグル（DEV_KIT_PYTHON/HTML/NEXT/MARKDOWN） | paths パターンで制御するため不要 |
| TTL `patterns` 名前空間 | リファレンス単位の `references` 名前空間のみに統合 |

## inject_references.py の変更

- `_load_ref_entries(refs_dir)`: references/ を走査してフロントマターを読み込む
- `_parse_frontmatter(content)`: --- で囲まれたフロントマターを parse
- `_extract_description(content)`: 最初の `# 見出し` から description を取得
- `_glob_to_regex`: `[id]` を文字クラスではなくリテラルとして扱うよう修正（Next.js ダイナミックルート対応）

## 不整合の修正

injection_rules.yaml に存在しないファイルが登録されていた5件を修正:

| 旧（存在しない） | 新（実ファイル） |
|---|---|
| `next/frontend/conventions/コメント.md` | `next/frontend/conventions/コメント規約.md` |
| `next/frontend/conventions/命名規則.md` | `next/frontend/conventions/命名規約.md` |
| `next/frontend/conventions/型定義.md` | `next/frontend/conventions/型規約.md` |
| `python/architecture/依存パッケージ管理.md` | `python/architecture/依存関係管理.md` |
| `python/architecture/design-基本方針.md` | 廃止ファイル — フロントマターなし |
