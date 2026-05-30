# PR184 — claude-kit-plugin-update-skill

## 概要

claude-kit プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。本 PR では同じ規約を **claude-kit 自身** にも適用する（規約を作ったプラグイン自身が遵守していない状態を解消）。

### 何をするか

- `plugins/claude-kit/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- 対象は「claude-kit 関連成果物」の **2 種類**:
  - **静的テンプレ**: claude-kit が `/ref-inject:apply` 経由で他プラグインに展開する injection hook スクリプト・templates/・references/ スケルトン → ref-inject の担当範囲なので claude-kit:plugin-update のスコープ外（ref-inject:plugin-update が行う）
  - **規約遵守ファイル**: ユーザーが claude-kit のスキル（`skill-creator` / `rule-creator` / `hook-creator` / `plugin-creator` 等）を使って作成した `.claude/skills/**/SKILL.md` / `.claude/rules/**` / `.claude/hooks/**` / agents/ → 現行リファレンス（`references/skills.md` / `rules.md` / `hooks.md` / `plugin-structure.md` など）と照合し、規約逸脱を発見・修正
- **参考にしない**: workspace の plugin-update は静的ファイルコピー特化の実装であり、claude-kit の規約検査フローとは目的が異なる
- claude-kit の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | claude-kit の成果物 2 種を整理する（静的テンプレ vs 規約遵守ファイル） | - 設計検討 |
| 済 | `plugins/claude-kit/skills/plugin-update/SKILL.md` (+ jp) を作成 | - 新規 |
|  | スコープ: `.claude/skills/**/SKILL.md` / `.claude/rules/**` / `.claude/hooks/**` を現行リファレンス（skills.md / rules.md / hooks.md / plugin-structure.md / claude-md.md / etc.）と照合し、最小差分を適用。注入フックがリファレンスを自動供給する点を活用 | - |
| 済 | claude-kit を MINOR bump (3.40.0 → 3.41.0) ※master 取り込みで開始時バージョンが 3.38.0 から 3.40.0 にずれていたため再算出 | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | changelog 追加（`changelogs/v3.41.0.md`） ※CLAUDE.md の `## Changelog` 表への移行はまだどの plugin でも未実施。本 PR では既存パターンを踏襲し、テーブル化は別 PR で一括対応 | - `plugins/claude-kit/changelogs/v3.41.0.md` |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/skills/plugin-update/SKILL.md` | 新規 | claude-kit 規約への追従スキル本体 | 注入フックの自動供給を前提に、規約再掲を省略 |
| `plugins/claude-kit/skills/plugin-update/SKILL.jp.md` | 新規 | JP mirror | warning コメント込み |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | `3.40.0` → `3.41.0` | MINOR (新スキル) |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit entry を `3.40.0` → `3.41.0` | 上と整合 |
| `plugins/claude-kit/changelogs/v3.41.0.md` | 新規 | リリースノート | dev-kit / work と異なる semantic-migration 設計の根拠を記載 |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証） | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/dev-kit/skills/plugin-update/SKILL.md` — 「静的テンプレ再コピー + 規約遵守ファイル検査」の 2 段構成を実装した参考例
- `plugins/claude-kit/references/plugin-structure.md` — `## Required skills` セクション（plugin-update の定義）
- `plugins/claude-kit/references/skills.md` / `rules.md` / `hooks.md` — 照合に使う規約リファレンス

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | plugin authoring guide に `plugin-update` 必須化を追加（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
