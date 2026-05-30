# PR185 — ref-inject-plugin-update-skill

## 概要

ref-inject プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。本 PR では同じ規約を ref-inject にも適用する。

### 何をするか

- `plugins/ref-inject/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- ref-inject の「プラグイン関連成果物」の構造:
  - **静的テンプレ**: ref-inject が `/ref-inject:apply` でターゲットプラグインに展開した injection hook スクリプト（`inject_references.py`）・`hooks.json` 更新・Jinja2 テンプレ（`injection.md.j2` / `.jp.md.j2`）・`references/` スケルトン
  - **規約遵守ファイル**: ref-inject が直接作成するファイルは injection 機構のみなので、規約遵守ファイルの検査対象は injection hook を導入済みの各プラグインの injection 構成（injection_rules.yaml / inject_references.py のバージョン整合性）
- **plugin-update の主要動作**:
  1. `plugins/*/hooks/inject_references.py` を検索し、ref-inject が apply 済みのプラグインを列挙
  2. 各プラグインの injection hook を現在の ref-inject バージョンのテンプレートと照合
  3. 差分があれば再 apply 相当の更新を提案（ユーザー確認必須）
- ref-inject の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `plugins/ref-inject/skills/plugin-update/SKILL.md` (+ jp) を作成 | - 新規 |
|  | スコープ: apply 済みプラグイン列挙 → 各 inject_references.py を現バージョンテンプレと照合 → 差分あればユーザー確認後に更新 | - |
| 済 | ref-inject を MINOR bump | - `plugins/ref-inject/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | CLAUDE.md の Changelog 表に追記 | - `plugins/ref-inject/CLAUDE.md` / `.jp.md` |
| 済 | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/ref-inject/skills/plugin-update/SKILL.md` | 新規 | plugin-update スキル定義（英語） | |
| `plugins/ref-inject/skills/plugin-update/SKILL.jp.md` | 新規 | JP ミラー | |
| `plugins/ref-inject/CLAUDE.md` | 編集 | 構成ツリーに plugin-update 追記 / Changelog 追加 | |
| `plugins/ref-inject/CLAUDE.jp.md` | 編集 | 同上（日本語） | |
| `plugins/ref-inject/.claude-plugin/plugin.json` | 編集 | 1.5.0 → 1.6.0 | |
| `.claude-plugin/marketplace.json` | 編集 | ref-inject 1.5.0 → 1.6.0 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証） | - |

## QA

特になし。（QA-001 は概要「何をするか」にて 案A で決着済み）

## 参考ドキュメント

- `plugins/workspace/skills/plugin-update/SKILL.md` — 参考実装
- `plugins/claude-kit/references/plugin-structure.md` — `## Required skills` セクションで規定
- `plugins/ref-inject/skills/apply/SKILL.md` — ref-inject の本体スキル（plugin-update との責務分担を整理する材料）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | plugin authoring guide に `plugin-update` 必須化を追加（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
