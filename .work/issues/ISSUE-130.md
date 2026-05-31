# ISSUE-130: ref-inject テンプレート hooks.json に SessionStart フックが欠落 — plugin-migrate 実行時に consumer の SessionStart が消去されるリスク

**作成日**: 2026-05-31

## 問題

**該当ファイル**: `plugins/ref-inject/templates/hooks/hooks.json`

`ref-inject` テンプレートの `hooks.json`（L1–L78）には `PreToolUse`（injection 用: Edit / Write / MultiEdit / Read）のみが定義されており、`SessionStart` フックが含まれていない。

一方、このテンプレートをベースとしている injection consumer（`claude-kit` / `dev-kit`）の本体 `hooks.json` にはいずれも `SessionStart` フックが後から追加されている:

- `plugins/claude-kit/hooks/hooks.json` L77–L89: `SessionStart` → `hooks/scripts/setup_check.py`
- `plugins/dev-kit/hooks/hooks.json` L115–L127: `SessionStart` → `hooks/scripts/setup_check.py`

この乖離により、`/ref-inject:plugin-migrate` を実行してテンプレートを consumer に再適用した際、スキルとして機能している `SessionStart` エントリが上書き・消去される危険性がある。結果として `setup-wizard` の初回セットアップ検出機能（`setup_check.py`）がサイレントに無効化される。

## 推奨対応

以下 2 つの選択肢がある:

**A. テンプレートに SessionStart エントリを追加する（推奨）**

`ref-inject/templates/hooks/hooks.json` の `PreToolUse` ブロックの後に `SessionStart` → `setup_check.py` エントリを追加する。これにより `/ref-inject:apply` で新規セットアップした場合も一貫した `hooks.json` が生成される。

**B. `/ref-inject:plugin-migrate` に SessionStart 保護ロジックを追加する**

テンプレートを injection machinery のみに絞るという設計方針（ref-inject CLAUDE.md 記載）を維持する場合は、`plugin-migrate` スキルに「`SessionStart` はテンプレート外のため hooks.json 全体上書きを行わず、`PreToolUse` / `PostToolUse` の差分マージのみ行う」という明示的な保護を記述する。

いずれの対処もなされない場合、`plugin-migrate` 後に `setup-wizard` 連携が壊れサイレント障害となる。

## 水平展開

`plugins/ref-inject/skills/plugin-migrate/SKILL.md` の実装内容を確認し、hooks.json を全体上書きしているか差分マージ方式かを明確にする必要がある。全体上書きであれば本問題は高優先度に格上げすべき。
