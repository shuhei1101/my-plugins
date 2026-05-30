# PR206 — ref-inject-references-edit-guard

## 概要

ref-inject に「`references/` 配下のファイルが追加・編集された際、対応する `_index.yaml` / `_injection_rules.yaml` のパス登録を忘れていないかリマインドする」フックを追加する。

### 背景（PR199 からの引き継ぎ）

PR199（dev-kit yaml サブフォルダ化）のマージ間際に、`yaml/yaml.md` が dev-kit の `_index.yaml` / `_injection_rules.yaml` に未登録だったことが判明した。今回はユーザー指摘によって発覚したが、同種の登録漏れは構造変更時に頻発しうるため、自動検知の仕組みを設けたい。

**設計方針**:

- `references/` 配下にファイル追加・編集（Edit / Write / MultiEdit）が行われた際にフックが発火
- 対応する `_index.yaml` / `_injection_rules.yaml` の更新を促すリマインダープロンプトを Claude のコンテキストに注入
- ref-inject が導入されているプラグインでのみ発火（プラグインの責務範囲を守る — ref-inject 同梱の hooks.json に組み込む）
- session 内一度きりの注入（既存の TTL トークン仕組みを再利用）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `## QA` の未解決事項をユーザーに確認 | - |
| 済 | フックスクリプトの仕様を決める（path matching・出力プロンプト・dedup 方針） | - |
| 済 | `references/` 編集を検知するフックスクリプトを実装 | - `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` |
| 済 | フックを `templates/hooks/hooks.json` の既存 PreToolUse matcher 配下に登録 | - `plugins/ref-inject/templates/hooks/hooks.json` |
| 済 | リマインダープロンプト本文（英 + JP）を作成 | - `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.md`<br>- `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.jp.md` |
| 済 | ref-inject:apply スキルが新フックをコピーするよう更新 | - `plugins/ref-inject/skills/apply/SKILL.md`<br>- `plugins/ref-inject/skills/apply/SKILL.jp.md` |
| 済 | 既存 ref-inject 利用先（dev-kit / claude-kit）の hooks.json / scripts / prompts に新フックを波及 | - `plugins/dev-kit/hooks/{hooks.json,scripts/references_edit_guard.py,prompts/references-edit-guard.md,prompts/references-edit-guard.jp.md}`<br>- `plugins/claude-kit/hooks/{hooks.json,scripts/references_edit_guard.py,prompts/references-edit-guard.md,prompts/references-edit-guard.jp.md}` |
| 済 | ref-inject / dev-kit / claude-kit バージョン bump + changelog | - 3 つの `plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/ref-inject/changelogs/v1.6.0.md`<br>- `plugins/claude-kit/changelogs/v3.44.0.md`<br>- `plugins/dev-kit/CLAUDE.md` Changelog 行追加 |
| 済 | ノート更新（対象なし — 設計詳細は changelog に記録済） | - |
| 済 | CLAUDE.md / ルール更新（dev-kit CLAUDE.md Changelog を更新） | `plugins/dev-kit/CLAUDE.md` + JP |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` | 新規 | references/ 編集時の登録漏れ検知スクリプト | - |
| `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.md` | 新規 | 注入プロンプト（英） | - |
| `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.jp.md` | 新規 | JP ミラー | - |
| `plugins/ref-inject/templates/hooks/hooks.json` | 編集 | 新フック登録 | - |
| `plugins/ref-inject/skills/apply/SKILL.md` | 編集 | 新フックのコピー手順を追加 | - |
| `plugins/ref-inject/skills/apply/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/ref-inject/.claude-plugin/plugin.json` | 編集 | バージョン bump | MINOR（新フック追加） |
| `.claude-plugin/marketplace.json` | 編集 | ref-inject バージョン同期 | - |
| `plugins/ref-inject/changelogs/v{X.Y.Z}.md` | 新規 | changelog | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト対象なし（フック動作は Claude セッションで手動確認） | - |

## QA

PR スコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

### QA-001: フックのイベントを PreToolUse / PostToolUse のどちらにするか

**決定**: 案 B（PreToolUse）。編集完了後だと既にミスが発生済みで意味がない。**編集前** に登録のことを意識できる方が予防効果が高い。

**反映先**: `plugins/ref-inject/templates/hooks/hooks.json` の PreToolUse(Edit/Write/MultiEdit) matcher 配下（既存の inject_references.py と同じ matcher に並べる）

### QA-002: 既存のプラグインへ波及適用するか

**決定**: 案 A（本 PR で dev-kit / claude-kit の hooks.json も併せて更新。両プラグインを MINOR バンプ）

**反映先**: `plugins/dev-kit/hooks/hooks.json`、`plugins/claude-kit/hooks/hooks.json`、両プラグインの plugin.json / marketplace.json / changelog

## 参考ドキュメント

- `.work/notes/setup-wizard-pattern.md`: 関連する別設計（setup-wizard パターン、現在は未着手）
- `plugins/ref-inject/templates/hooks/scripts/inject_references.py`: 既存の ref-inject 注入スクリプト（参考実装）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #199 | dev-kit yaml サブフォルダ化（本PRの動機となった登録漏れ事例） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
