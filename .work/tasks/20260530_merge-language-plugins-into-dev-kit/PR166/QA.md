# QA — PR166 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: PR のスコープ分割

**問題**: py-kit / html-kit / next-kit の統合は変更量が多く、一気にやると高リスク。

**選択肢**:
- A. このPR166で一気に実装（py + html + next をまとめて dev-kit に統合）
- B. 言語ごとに PR を分割
- C. このPR166は設計+py-kitのみ、残りは次PRに委ねる

**→ 決定**: **A. 一気に実装**（Opus 4.7 1M context で対応可能と判断）

---

## QA-002: スキル名の衝突解決

**問題**: html-kit と next-kit はともに `implement` というスキル名を持つ。

**→ 決定**: 言語プレフィックス方式で残す + 純粋な実装系で代替可能なものはフック注入に任せる

**統合後のスキル一覧**:
- `dev-kit:py-script`（py-kit から移行・名前変更なし）
- `dev-kit:py-project`（py-kit から移行・名前変更なし）
- `dev-kit:html-implement`（html-kit:implement から rename）
- `dev-kit:html-logging`（html-kit:logging から rename）
- `dev-kit:html-mock`（html-kit:mock から rename）
- `dev-kit:html-debug-fab`（html-kit:debug-fab から rename）
- `dev-kit:next-implement`（next-kit:implement から rename）
- `dev-kit:next-plan`（next-kit:plan から rename）
- `dev-kit:yaml`（既存維持）

**方針**: ユーザーが「実装系はフックで結びつけるので削除OK」と発言したが、補助スキル（logging/mock/debug-fab/plan）は ref-inject では完全に代替できない機能を含むため、保守的に言語プレフィックスをつけて残す。

---

## QA-003: env 変数の設計方針

**→ 決定**: **B. 個別トグル**

```
DEV_KIT_PYTHON=true   # Python リファレンス注入を有効化
DEV_KIT_HTML=true     # HTML/CSS/JS リファレンス注入を有効化
DEV_KIT_NEXT=true     # Next.js リファレンス注入を有効化
```

**デフォルト**: 全て false（明示的に opt-in 方式）—プロジェクトで使う言語だけを ON にする。

---

## QA-004: inject_references.py の統合方針

**→ 決定**: **A. 単一スクリプト**

- `plugins/dev-kit/hooks/inject_references.py` 1 本に統合
- `PLUGIN_NAME = "dev-kit"`, `ENV_PREFIX = "DEV_KIT"`
- TTLトークン: `~/.claude/tokens/dev-kit/{session_id}.yaml`
- `injection_rules.yaml` には全言語のルールをまとめて記述、各ルールに `lang: python|html|next` フィールドを付与
- スクリプトは `DEV_KIT_PYTHON / HTML / NEXT` をチェックし、active な言語のルールのみ適用する

---

## QA-005: ts_check.py の env 変数名

**→ 決定**: **A. `DEV_KIT_NEXT_TS_CHECK`**

- 既存の `NEXT_KIT_TS_CHECK` 設定は廃止（プラグイン削除に伴う破壊的変更）
- `plugins/dev-kit/hooks/ts_check.py` に移動
- `DEV_KIT_NEXT_TS_CHECK=false`/`0`/`no`/`off` で無効化

---

## QA-006: html-kit の UserPromptSubmit フックの扱い

**→ 決定**: **B. PreToolUse inject_references.py 方式に統一**

- html-kit の UserPromptSubmit (`ui-skill-reminder.md` 注入) は廃止
- `principles.md`, `ui-design.md` を `plugins/dev-kit/references/html/` に配置
- `injection_rules.yaml` に html 対応のルールを追加（`*.html`, `*.css`, `*.js` などのパターンで注入）
- HTML 系も py-kit / next-kit と同じ ref-inject 形式に揃える

---

## QA-007: 既存プラグイン（py-kit / html-kit / next-kit）の取り扱い

**→ 決定**: **A. 完全削除**

- `plugins/py-kit/`, `plugins/html-kit/`, `plugins/next-kit/` をディレクトリごと削除
- `.claude-plugin/marketplace.json` から 3 エントリ削除
- このリポジトリはシングルユーザー使用のため後方互換性は不要
