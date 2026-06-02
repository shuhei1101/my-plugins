# ISSUE-130: ref-inject テンプレート hooks.json に SessionStart フックが欠落 — plugin-migrate 実行時に consumer の SessionStart が消去されるリスク

**作成日**: 2026-05-31

## 概要

`ref-inject` テンプレートの `hooks.json` に `SessionStart` フックが含まれていないため、`/ref-inject:plugin-migrate` でテンプレートを consumer に再適用すると、consumer 側で機能している `SessionStart` エントリが上書き・消去される危険性がある。

## 背景

`ref-inject` テンプレートは consumer（`claude-kit` / `dev-kit`）の `hooks.json` のベースになっている。consumer 側はテンプレートに無い `SessionStart` フックを後から追加して使っている。

## 現状

**該当ファイル**: `plugins/ref-inject/templates/hooks/hooks.json`

テンプレートの `hooks.json`（L1–L78）には `PreToolUse`（injection 用: Edit / Write / MultiEdit / Read）のみが定義されており、`SessionStart` フックが含まれていない。一方、consumer の本体 `hooks.json` にはいずれも `SessionStart` フックが後から追加されている:

- `plugins/claude-kit/hooks/hooks.json` L77–L89: `SessionStart` → `hooks/scripts/setup_check.py`
- `plugins/dev-kit/hooks/hooks.json` L115–L127: `SessionStart` → `hooks/scripts/setup_check.py`

この乖離により、`/ref-inject:plugin-migrate` 実行時に `SessionStart` エントリが上書き・消去され、`setup-wizard` の初回セットアップ検出機能（`setup_check.py`）がサイレントに無効化される危険性がある。

## 期待される状態

`plugin-migrate` 実行後も consumer の `SessionStart` フックが保持され、`setup-wizard` 連携がサイレントに壊れない。

## 対応案

| 案 | 内容 | メリット | デメリット |
|---|---|---|---|
| A | テンプレート `hooks.json` の `PreToolUse` ブロックの後に `SessionStart` → `setup_check.py` エントリを追加 | `/ref-inject:apply` 新規セットアップでも一貫した `hooks.json` が生成される | テンプレートを injection machinery のみに絞る設計方針から外れる |
| B | `/ref-inject:plugin-migrate` に SessionStart 保護ロジックを追加（hooks.json 全体上書きせず PreToolUse/PostToolUse の差分マージのみ） | 設計方針（テンプレートは injection のみ）を維持できる | plugin-migrate 側の実装が複雑化 |

いずれの対処もなされない場合、`plugin-migrate` 後に `setup-wizard` 連携が壊れサイレント障害となる。

**推奨: 案A**

## 横展開

`plugins/ref-inject/skills/plugin-migrate/SKILL.md` の実装内容を確認し、hooks.json を全体上書きしているか差分マージ方式かを明確にする必要がある。全体上書きであれば本問題は高優先度に格上げすべき。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する

## QA

### QA-1: テンプレートに追加するか plugin-migrate を保護するか

A) テンプレート `hooks.json` に `SessionStart` エントリを追加 / B) `plugin-migrate` に SessionStart 差分マージ保護を追加

**推奨**: A — テンプレートに追加すれば `apply` / `migrate` 双方で一貫し、`setup_check.py` の消去リスクを根本から解消できる。

**回答**: A
