# ISSUE-130: ref-inject テンプレート hooks.json に SessionStart フックが欠落 — plugin-migrate 実行時に consumer の SessionStart が消去されるリスク

**作成日**: 2026-05-31

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

## QA

### QA-1: テンプレートに追加するか plugin-migrate を保護するか

A) テンプレート `hooks.json` に `SessionStart` エントリを追加 / B) `plugin-migrate` に SessionStart 差分マージ保護を追加

**推奨**: A — テンプレートに追加すれば `apply` / `migrate` 双方で一貫し、`setup_check.py` の消去リスクを根本から解消できる。

- [x] A
- [ ] B


### QA-2: 前提が陳腐化済み — 案A は存在しない setup_check.py を参照し apply フローを壊す

実装着手時の調査で、本イシューの前提が現リポジトリと食い違うことが判明した。実装をブロックして再判断を仰ぐ。

判明した事実:
- **`SessionStart` → `setup_check.py` は全 consumer から既に削除済み**。`claude-kit` 3.51.0 / `dev-kit` 4.13.0 / `ref-inject` 1.9.0 / `work` 2.59.0 の changelog が `setup-wizard` スキルと `SessionStart` フック削除を記録。現在の `plugins/claude-kit/hooks/hooks.json`・`plugins/dev-kit/hooks/hooks.json` に `SessionStart` エントリは存在しない（イシュー本文の「L77-89 / L115-127 に SessionStart」は現状と不一致）。`find plugins -name setup_check.py` は 0 件 — スクリプト自体がリポジトリに存在しない。
- **`plugin-migrate` は hooks.json を全体上書きしない（差分マージ方式）**。`plugins/ref-inject/skills/plugin-migrate/SKILL.md` が `PreToolUse(Edit|Write|MultiEdit|Read)` エントリのみをマージし他フックは温存すると明記（L37 / L118-120 / L149-151、禁止事項 L163「Never replace the whole hooks.json — always merge the PreToolUse entry in-place」）。よって本イシューが想定した「再適用で SessionStart が消える」リスクはそもそも発生しない。

帰結:
- 案A をそのまま実装すると、テンプレート `hooks.json` に**存在しない `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/setup_check.py` を指す SessionStart エントリ**が入る。`/ref-inject:apply` で新規プラグインに適用すると、毎セッション開始時に存在しないスクリプトを起動する壊れたフックを生成する（新規 apply フローの実害）。

選択肢:
A) このイシューをクローズ（wontfix）— 前提（消去リスク）が plugin-migrate の差分マージ仕様により既に存在せず、対象の SessionStart/setup_check.py も全廃済みのため対応不要 /
B) 別の意図（setup_check.py を復活させ全 consumer + テンプレートに SessionStart を再導入する）であれば、それは ISSUE-130 の範囲を超える別イシューとして再起票 /
C) その他（具体指示を記入）

**推奨**: A — リスクの根本（plugin-migrate の全体上書き）が存在せず、`setup_check.py` も全廃済み。テンプレートへの追加はむしろ apply フローを壊す。

- [x] A
- [ ] B
- [ ] C

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

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
