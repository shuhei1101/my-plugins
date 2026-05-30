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
| - | `## QA` の未解決事項をユーザーに確認 | - |
| - | フックスクリプトの仕様を決める（path matching・出力プロンプト・dedup 方針） | - |
| - | `references/` 編集を検知するフックスクリプトを実装 | - `plugins/ref-inject/templates/hooks/scripts/references_edit_guard.py` |
| - | フックを `templates/hooks/hooks.json` に登録（PreToolUse か PostToolUse か検討） | - `plugins/ref-inject/templates/hooks/hooks.json` |
| - | リマインダープロンプト本文（英 + JP）を作成 | - `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.md`<br>- `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.jp.md` |
| - | ref-inject:apply スキルが新フックをコピーするよう更新 | - `plugins/ref-inject/skills/apply/SKILL.md`<br>- `plugins/ref-inject/skills/apply/SKILL.jp.md` |
| - | ref-inject 自体に新フックを適用（dev-kit / claude-kit / py-kit など既存利用先への波及確認） | - 既存プラグインの `hooks.json` |
| - | ref-inject バージョン bump + changelog | - `plugins/ref-inject/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/ref-inject/changelogs/v{X.Y.Z}.md` |
| - | ノート更新 | `.work/notes/` |
| - | CLAUDE.md / ルール更新（必要なら） | - |

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

**背景**: references/ への編集を検知して登録漏れリマインダーを出す。タイミングをいつにすべきか。

| 案 | 内容 |
|---|---|
| A | PostToolUse(Edit/Write/MultiEdit) — 編集完了後に「登録した？」と問う |
| B | PreToolUse(Edit/Write/MultiEdit) — 編集直前に「登録も忘れずに」と促す |

**推奨方式**: A（PostToolUse）。編集完了後の方が「実際に追加されたファイル」に対して具体的に問えるし、誤検知も少ない。

**状態**: 未解決

**決定したら反映先**: `plugins/ref-inject/templates/hooks/hooks.json` のフックイベント

### QA-002: 既存のプラグインへ波及適用するか

**背景**: 新フックは ref-inject:apply で新規導入時にコピーされるが、既に ref-inject 適用済の dev-kit / claude-kit / py-kit 等の既存 hooks.json には自動で入らない。

| 案 | 内容 |
|---|---|
| A | 本 PR で各既存プラグインの hooks.json も併せて更新する |
| B | 別 PR（各プラグインの plugin-update 実行）で対応する |

**推奨方式**: A（本 PR でまとめて）。フックは小さく独立しているのでリスクが低く、ユーザーが個別 plugin-update を呼ぶ手間を省ける。

**状態**: 未解決

**決定したら反映先**: 作業内容テーブル

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
