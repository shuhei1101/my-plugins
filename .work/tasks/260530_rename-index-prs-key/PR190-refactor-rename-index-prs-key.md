# PR190 — rename-index-prs-key

## 概要

workspace の `index.yaml` / `index.archive.yaml` テンプレートおよび `index-tool.py` スクリプトで使われている `prs:` キーを、ブランチ寄りの名称（`branches:` または `work_items:`）に改名する。

PR188（work-start の PR 用語をブランチ用語に統一）と並行して実施できる独立した変更。index.yaml の YAML データモデルの用語をブランチ概念に揃えることで、「PR番号管理」から「ブランチ管理」への移行を進める。

**背景（PR188 で決定した方針）：**
- workspace の用語全体を「PR（Pull Request）」から「ブランチ」ベースに移行する方針を決定
- ブランチ名から `PR{N}/` プレフィックスを除去する（PR188 担当）
- index.yaml の内部 ID 自体は当面残す（採番継続）が、`prs:` というキー名は改名する（本 PR 担当）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を確認・記録する | - |
| - | `.work/notes/` の作業メモを更新 | - |
| - | `prs:` キーの新名称を決定（QA-001 参照） | - |
| - | テンプレート index.yaml の `prs:` キーを新名称に変更 | - `plugins/workspace/templates/.work/tasks/index.yaml` |
| - | テンプレート index.archive.yaml の `prs:` キーを新名称に変更 | - `plugins/workspace/templates/.work/tasks/index.archive.yaml` |
| - | index-tool.py の `prs:` 参照を新名称に変更 | - `plugins/workspace/scripts/index-tool.py` |
| - | SKILL.md 等でキー名に言及している箇所を更新 | - workspace スキル全般 |
| - | CLAUDE.md / glossary 等の用語集を更新（必要なら） | - |
| - | 各 SKILL.jp.md を同期 | - 対象の `.jp.md` ファイル |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし | - |

## QA

### QA-001: prs: の新名称

**背景**: `prs:` キーの改名先として適切な名称を選ぶ。

| 案 | 内容 |
|---|---|
| A | `branches:` — ブランチ管理であることを明示 |
| B | `work_items:` — 作業単位という意味でより抽象的 |
| C | `tasks:` — ただし `.work/tasks/` フォルダと紛らわしい |

**推奨方式**: A（`branches:`）— PR188 の方針に最も合致し、ブランチ管理であることが明確。

**状態**: 未解決（着手時に確認）

**決定したら反映先**: `## 作業内容` のテンプレート・スクリプト変更行

### QA-002: 既存の index.yaml の移行

**背景**: テンプレートだけ変更しても、既に生成された `.work/tasks/index.yaml` は古いキー名のまま残る。

| 案 | 内容 |
|---|---|
| A | index-tool.py で新旧どちらのキー名も読み取れるようにする（後方互換） |
| B | 一括置換スクリプトで既存 index.yaml / index.archive.yaml を新キー名に書き換える |

**推奨方式**: B — ローカルファイルのみなので一括置換の方がシンプル。

**状態**: 未解決（着手時に確認）

**決定したら反映先**: `## 作業内容` の index-tool.py 変更行

## 参考ドキュメント

- `.work/notes/rename-pr-to-branch.md` — 本変更シリーズの設計メモ
- `plugins/workspace/templates/.work/tasks/index.yaml` — 変更対象テンプレート
- `plugins/workspace/scripts/index-tool.py` — 変更対象スクリプト

## 関連PR

| PR番号 | 概要 |
|---|---|
| #188 | work-start の PR 用語をブランチ用語に統一（本シリーズの起点） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
