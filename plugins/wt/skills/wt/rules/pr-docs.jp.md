---
paths:
  - "docs/PR/**/*.md"
  - "docs/PR/index.yaml"
---

# PR ドキュメントルール

> **このファイルは日本語ミラーです。Claude には読み込まれません。本体は `pr-docs.md`。**

## PR ドキュメントを作成するタイミング

`docs/PR/PR{N}.md` はマージ前（または実装中）に作成する。マージ後の後付け作成は禁止。
計画PR（実装なし・設計/ロードマップのみ）は先にドキュメントを作成し、index.yaml で `planning: true` にする。

## 必須セクション

```markdown
# PR{N} — {短いタイトル}

## Overview（概要）

{1〜3行: このPRが何をするか・なぜ必要か。}

## Scope（スコープ）

### Includes（含むもの）
- {項目}

### Excludes（含まないもの）
- {項目}

## Changed Files（変更ファイル）

- `path/to/file` — 変更理由を一行で
```

任意セクション（必要に応じて追加）: `Background`, `Prerequisites`, `Implementation Log`, `Decisions`, `Open Issues`

## index.yaml — 必須更新

`docs/PR/PR{N}.md` を作成・大幅変更するたびに、`docs/PR/index.yaml` の対応エントリを追加または更新する。

**フィールドルール:**

| フィールド | ルール |
|---|---|
| `id` | PR 番号（int） |
| `title` | PR{N}.md の h1 テキストそのまま |
| `type` | `feat` / `fix` / `docs` / `refactor` / `chore` / `test` |
| `tags` | 自由形式リスト |
| `planning` | 実装なし（計画・設計書）の場合 `true` |
| `summary` | ファイルを開かずに内容がわかる一行説明（120字以内） |
| `children` | この計画PRが定義した子PR番号リスト |
| `parent` | 計画PRによって定義された子PRの場合、親PR番号 |

**最小例:**

```yaml
  - id: 42
    title: 'PR42 — Add user authentication'
    type: feat
    tags: [auth, api]
    planning: false
    summary: 'JWT-based auth with refresh token rotation'
```
