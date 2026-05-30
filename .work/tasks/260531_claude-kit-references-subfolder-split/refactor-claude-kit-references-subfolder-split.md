# refactor/claude-kit-references-subfolder-split

> 内部 ID: 223（index.yaml 採番用 — クロスリファレンス目的）

## 概要

claude-kit の `references/` はすべてのファイルがフラットに並んでいる。dev-kit が `html/`・`python/`・`next/`・`markdown/`・`yaml/` というトピック別サブフォルダを持つのに対して、claude-kit は 20 以上のファイルが 1 ディレクトリに混在している。何がどこに書かれているのか分かりにくい。

また、plugin バージョン三点セット（`plugin.json` + `marketplace.json` + `CLAUDE.md`）の同期チェックリストは現在 `plugin-structure.md` に埋め込まれているが、独立ファイルとして分離すべき。

このブランチでは以下を行う：
1. claude-kit `references/` をトピック別サブフォルダに分割
2. plugin バージョン同期チェックを独立リファレンスファイルへ分離
3. `_injection_rules.yaml` を新パス構造に合わせて更新
4. 注入ルールが適切に動作するよう整備

### 背景（PR219 からの引き継ぎ）

- PR219（feat/migrate-existing-plugins-to-have-config-skill）で dev-kit:config スキルを追加し、work:config を整理した
- plugin-structure.md には「plugin.json / marketplace.json / CLAUDE.md の版を常に揃える」というチェックリストが書かれているが、plugin-related ファイルを編集したときの injection ルールは設定済み（`**/.claude-plugin/{plugin,marketplace}.json` → `plugin-structure.md`）
- ただし CLAUDE.md を編集したときに version triple の reminder が出ないという逆方向の欠陥がある

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | 済 | `## QA` に未決定事項を記録する | - `refactor-claude-kit-references-subfolder-split.md` |
| 2 | 済 | `.work/notes/` のノートを更新する | - `.work/notes/claude-kit-references-structure.md` |
| 3 | 済 | 現在の `references/` ファイル一覧とトピック別グルーピングを設計する（QA 先決） | - |
| 4 | 済 | サブフォルダを作成しファイルを移動する | - `plugins/claude-kit/references/{plugin,skill,hook,claude-md,common}/` |
| 5 | 済 | `_index.yaml` / `_index.jp.yaml` のパスを更新する | - `plugins/claude-kit/references/.ref-injects/_index.yaml`<br>- `plugins/claude-kit/references/.ref-injects/_index.jp.yaml` |
| 6 | 済 | `_injection_rules.yaml` のパスを更新する | - `plugins/claude-kit/references/.ref-injects/_injection_rules.yaml` |
| 7 | 済 | plugin バージョン同期チェックを独立ファイルに分離する | - `plugins/claude-kit/references/plugin/version-sync.md` |
| 8 | 済 | `plugins/*/CLAUDE.md` 編集時にバージョン同期 reminder が注入されるよう injection rule を追加 | - `plugins/claude-kit/references/.ref-injects/_injection_rules.yaml` |
| 9 | 済 | claude-kit バージョンバンプ + changelog | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `plugins/claude-kit/CLAUDE.md` |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/references/common/` | 新規（サブフォルダ） | common.md / environment.md / references-sync.md / subagents.md / askuserquestion.md を移動 | - |
| 2 | `plugins/claude-kit/references/skill/` | 新規（サブフォルダ） | skills.md を移動 | - |
| 3 | `plugins/claude-kit/references/hook/` | 新規（サブフォルダ） | hooks.md / kit-hooks-sync.md / jinja2/ を移動 | - |
| 4 | `plugins/claude-kit/references/claude-md/` | 新規（サブフォルダ） | claude-md.md / rules.md を移動 | - |
| 5 | `plugins/claude-kit/references/plugin/` | 新規（サブフォルダ） | plugin-structure.md / plugin-claude-md.md / plugin-config.md / setup-wizard.md を移動 | - |
| 6 | `plugins/claude-kit/references/plugin/version-sync.md` | 新規 | plugin バージョン同期不変条件（plugin-structure.md から分離） | `.jp.md` ミラーも作成 |
| 7 | `plugins/claude-kit/references/.ref-injects/_index.yaml` | 編集 | 新パスに更新・incidents.md stale エントリ削除・version-sync.md 追加 | - |
| 8 | `plugins/claude-kit/references/.ref-injects/_index.jp.yaml` | 編集 | 〃（JP 版） | - |
| 9 | `plugins/claude-kit/references/.ref-injects/_injection_rules.yaml` | 編集 | 新パス更新・plugins/*/CLAUDE.md に version-sync.md 注入ルール追加 | - |
| 10 | `plugins/claude-kit/references/.ref-injects/CLAUDE{.jp,}.md` | 編集 | パスマップを新構造に更新 | - |
| 11 | `plugins/claude-kit/skills/plugin-update/SKILL{.jp,}.md` | 編集 | リファレンスマップを新パスに更新 | - |
| 12 | `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | v3.47.0 → v3.48.0 | - |
| 13 | `.claude-plugin/marketplace.json` | 編集 | 〃 | - |
| 14 | `plugins/claude-kit/CLAUDE{.jp,}.md` | 編集 | changelog に v3.48.0 行を追加 | - |

## テスト

なし

## QA

### QA-001: サブフォルダ構成の設計

**背景**: references/ の分割粒度をどうするか。dev-kit のようにツール/言語別か、役割別（plugin/, skills/, hooks/）か。

| 案 | 内容 |
|---|---|
| A | 役割別: `plugin/`・`skill/`・`hook/`・`claude-md/`・`common/` |
| B | 粒度を下げて 3〜4 フォルダだけ: `plugin/`・`authoring/`（skill+hook+CLAUDE.md）・`common/` |

**推奨方式**: A（役割別 5 フォルダ）。dev-kit と同じ方針でトピックが明確になる。`environment.md` / `subagents.md` など複数カテゴリに属するものは `common/` に置く。

**状態**: 解決済み（A に決定）

**決定したら反映先**: 作業内容 #3 の設計

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md`: plugin 構造ガイド（version sync チェックリスト含む）
- `plugins/claude-kit/references/_injection_rules.yaml`: 現在の injection ルール
- `.work/notes/claude-kit-references-structure.md`: この作業のノート

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/migrate-existing-plugins-to-have-config-skill（PR219） | dev-kit:config 追加・work:config 整理（前ブランチ） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | migrate-claude-kit-to-have-config-skill | claude-kit に config スキルを追加（INJECTION_LANG / TTL が対象候補） | 即時実施可 |
