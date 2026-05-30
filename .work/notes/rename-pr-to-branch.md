---
created_at: 2026-05-30
updates:
  - 2026-05-30 — PR188: work-start の PR 用語をブランチ用語に統一
  - 2026-05-30 — PR190: index.yaml / index.archive.yaml の prs: キーを branches: に改名
related_prs:
  - PR188
  - PR190
---

# PR → ブランチ用語移行 — 設計メモ

## 概要

workspace プラグイン全体の用語を「PR（Pull Request）」から「ブランチ」ベースに移行する変更シリーズ。
PR 番号による採番自体は継続するが、内部キー名・UI 表示をブランチ概念に揃える。

## 変更シリーズ

| PR | 内容 |
|---|---|
| PR188 | work-start スキルの PR 用語をブランチ用語に統一 |
| PR190 | index.yaml / index.archive.yaml の `prs:` キーを `branches:` に改名 |

## PR190 の実施内容

### 変更方針

- QA-001: 新名称 → `branches:` を採用（`work_items:` / `tasks:` より明確）
- QA-002: 移行方針 → 一括置換（ローカルファイルなので後方互換不要）

### 変更対象

| ファイル | 変更内容 |
|---|---|
| `plugins/work/scripts/index-tool.py` | `data.get("prs")` → `data.get("branches")`、変数名も統一 |
| `plugins/work/scripts/trim-index.py` | 同上 |
| `plugins/work/templates/.work/tasks/index.yaml` | `prs: []` → `branches: []` |
| `plugins/work/templates/.work/tasks/index.archive.yaml` | `archived_prs: []` → `branches: []`（既存バグ修正） |
| 各 `.work/tasks/index*.yaml`（gitignored） | 一括 sed 置換 |

### 既存バグについて

テンプレート `index.archive.yaml` が `archived_prs:` キーを使っていたが、
スクリプトは `"prs"` キーで読み書きしていた。
実ファイルは `prs:` で正しく動いていたが、テンプレートとの乖離があった。
PR190 で `branches:` に統一して修正済み。

## 残タスク

- ブランチ名から `PR{N}/` プレフィックスを除去する（PR188 担当、別途実施）
- 内部 ID 採番（last_id / id フィールド）は当面変更しない
