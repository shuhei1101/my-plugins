# 設計メモ — py-kit / html-kit / next-kit → dev-kit 統合 (PR166)

## 背景・動機

現在 dev-kit は YAML スキルのみを持つ薄いプラグイン。
py-kit / html-kit / next-kit は言語固有の規約を提供するが、別プラグインとして存在することで
ユーザーが複数プラグインをインストール・管理しなければならない。

PR163 (worktree-kit → work-kit 統合) と PR164 (env トグル導入) の設計パターンを適用し、
言語系プラグインを dev-kit に統合することで「1 プラグインでフルスタック対応」を目指す。

---

## 現状の整理

### dev-kit (v3.0.0)
- スキル: `yaml`
- フック: YAML 編集時 PreToolUse ディスパッチ（yaml-skill-dispatch.md）
- リファレンス: `yaml.md` のみ

### py-kit (v2.5.0)
- スキル: `py-project`, `py-script`
- フック: `inject_references.py`（PreToolUse: Edit/Write/MultiEdit/Read）
- リファレンス: 多数（architecture/, core/, fastapi/, etc.）+ `injection_rules.yaml`
- TTLトークン: `~/.claude/tokens/py-kit/{session_id}.yaml`

### html-kit (v1.5.2)
- スキル: `debug-fab`, `implement`, `logging`, `mock`
- フック: UserPromptSubmit（キーワードマッチ → `ui-skill-reminder.md` 注入）
- リファレンス: `principles.md`, `ui-design.md`（小規模）
- inject_references.py: なし（UserPromptSubmit 方式）

### next-kit (v3.8.0)
- スキル: `implement`, `plan`
- フック: `inject_references.py`（PreToolUse）+ `ts_check.py`（PostToolUse）
- リファレンス: 多数（backend/, frontend/, testing/, etc.）+ `injection_rules.yaml`
- TTLトークン: `~/.claude/tokens/next-kit/{session_id}.yaml`

---

## スキル名衝突問題

html-kit と next-kit は同名の `implement` スキルを持つ。
dev-kit に統合する際、名前空間が同一になるため **どちらかをリネームする必要がある**。

候補:
- `dev-kit:html-implement` / `dev-kit:next-implement`
- `dev-kit:implement-html` / `dev-kit:implement-next`
- `dev-kit:html` / `dev-kit:next` (短縮形)

→ QA-002 で要決定

---

## env 変数の設計案

### 案A: 単一 `DEV_KIT_LANG` 変数（カンマ区切り）

```
DEV_KIT_LANG=python         # Python のみ
DEV_KIT_LANG=next           # Next.js のみ
DEV_KIT_LANG=python,next    # 複数プロジェクト対応
DEV_KIT_LANG=               # 指定なし（YAML のみ有効）
```

- pros: シンプル、1 変数で制御
- cons: カンマ区切りのパースが必要、「lang未指定＝全無効」の挙動がわかりにくい

### 案B: 個別トグル変数

```
DEV_KIT_PYTHON=true  # Python 有効
DEV_KIT_HTML=true    # HTML/CSS/JS 有効
DEV_KIT_NEXT=true    # Next.js 有効
```

- pros: 明示的、各言語を独立にトグル可能
- cons: 変数が増える

### 案C: デフォルト全有効（無効化のみ設定）

```
DEV_KIT_PYTHON_DISABLE=true  # Python 注入を無効化
DEV_KIT_HTML_DISABLE=true    # HTML 注入を無効化
DEV_KIT_NEXT_DISABLE=true    # Next.js 注入を無効化
```

- pros: 既存の `{PREFIX}_INJECTION_DISABLE` と一貫したパターン
- cons: 「使わない言語を全部 disable する」操作が必要

→ QA-003 で要決定

---

## フック統合の方針案

### inject_references.py

py-kit と next-kit がそれぞれ持つ `inject_references.py` を dev-kit に統合する場合:

**案1: 単一スクリプト（PLUGIN_NAME="dev-kit"）**
- `DEV_KIT_LANG` で active な言語の `injection_rules.yaml` だけを読み込む
- TTLトークン: `~/.claude/tokens/dev-kit/`
- ただし injection_rules.yaml を言語ごとに分ける（`injection_rules_python.yaml` 等）か、
  1 ファイルにまとめて「lang」フィールドでフィルタするかの選択が必要

**案2: 言語ごとのスクリプトを残す**
- `hooks/inject_py.py`, `hooks/inject_next.py` のように分割
- PLUGIN_NAME はどちらも "dev-kit"、TTLトークンパスは共通
- DEV_KIT_LANG チェックは各スクリプトの先頭で行う

→ QA-004 で要決定

### ts_check.py（next-kit専用）

next-kit の ts_check.py は TypeScript ファイル編集後に `tsc --noEmit` を実行する。
統合後も dev-kit 内に保持。`NEXT_KIT_TS_CHECK` → `DEV_KIT_NEXT_TS_CHECK`（またはそのまま）。

→ QA-005 で要決定

### html-kit の UserPromptSubmit フック

html-kit は UserPromptSubmit でキーワードマッチし `ui-skill-reminder.md` を注入している。
統合後は:
- そのまま dev-kit に移植（キーワードに `DEV_KIT_LANG` チェックを追加）
- inject_references.py 方式（PreToolUse）に移行する

→ QA-006 で要決定

---

## 既存プラグインの取り扱い案

### 案A: 物理的削除（marketplace から除去）

- py-kit / html-kit / next-kit を marketplace.json から削除
- リポジトリからも削除（または archive へ移動）
- pros: シンプル
- cons: 既存インストール済みユーザーへの影響

### 案B: deprecation stub として残す

- plugin.json の description に「Deprecated: dev-kit を使用してください」を記載
- スキル SKILL.md を「dev-kit:xxx を使ってください」にリダイレクト
- pros: 後方互換性
- cons: stub の維持コスト、このリポジトリはシングルユーザーなのでそもそも不要かも

→ QA-007 で要決定

---

## PR スコープの分割案

統合は大規模なため、分割が有効かもしれない。

### 案A: このPR166で一気に実装
- py-kit + html-kit + next-kit を dev-kit に統合
- 既存 3 プラグインを廃止
- pros: 一貫性、一度で完結
- cons: 変更量が多い、リスク高い

### 案B: 言語ごとに PR を分割
- PR166: 設計確定 + py-kit → dev-kit
- PR167: html-kit → dev-kit
- PR168: next-kit → dev-kit + 全廃止処理
- pros: 段階的、リスク分散
- cons: PR 数が増える

→ QA-001 で要決定

---

## 参考: PR163/164 の統合パターン

### PR163 (worktree-kit → work-kit)
- worktree-kit の 2 スキルを work-kit に移動
- `WORK_KIT_USE_WORKTREE` env で worktree 使用をトグル
- worktree-kit プラグインは廃止

### PR164 (env トグル)
- 常時発火フック/ステップに env トグルを追加
- `{PREFIX}_INJECTION_DISABLE` でリファレンス注入を無効化可能に
