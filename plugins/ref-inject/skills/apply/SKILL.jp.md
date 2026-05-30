---
name: apply
description: |
  ref-inject のリファレンス自動注入の仕組みを、対象プラグイン（新規でも既存でも）に適用（付与）する。注入フック（inject_references.py + hooks.json）・Jinja2 テンプレート・references/ 雛形を、プラグインごとのプレースホルダを置換しながらコピーする。プラグインレベルの関心事（plugin.json、プラグイン自身の CLAUDE.md、marketplace.json）は責務外 — 注入部分だけを扱う。
  トリガー: 「このプラグインに ref-inject を付けて」「リファレンス注入を追加して」「apply ref-inject to {plugin}」「add reference injection to a plugin」、または /ref-inject:apply の明示呼び出し。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# ref-inject:apply — プラグインに注入の仕組みを付与

`ref-inject` のリファレンス自動注入の仕組みを**対象プラグイン**に追加する。プラグインは
既存（自前の `plugin.json` / `CLAUDE.md` を持つ）でも、`plugin-creator` で作ったばかりでも
よい — このスキルは**注入部分だけ**を提供する。**Claude が各テンプレートを読んで出力先
ファイルを自分で書き**、プレースホルダを置換するので構造がコンテキストに残る。

付与される仕組み: `PreToolUse(Edit | Write | MultiEdit | Read)` フックが編集対象パスを
`references/_injection_rules.yaml` と照合し、マッチした reference を注入する —
`required` → **本文全量**、`optional` → **パス + description のみ** — 二層 TTL
トークン（パターン単位 + リファレンス単位）で重複抑制する。本セッションに既に注入済みの
リファレンスはパスのみ表示し、TTL 経過後に再注入する。

---

## 概要

このスキルは**注入の仕組みだけ**に責務を絞る。プラグインジェネレータ*ではない*:

- プラグインの `plugin.json` を作成・編集**しない**
- プラグインのルート `CLAUDE.md` を作成・所有**しない**
- `marketplace.json` を触ら**ない**

これらはプラグインレベルの関心事で `plugin-creator` の領分。ここでは対象プラグインが既に
存在する（または先に `plugin-creator` で作る）前提で、ref-inject ファイルがまだ無ければ付与する。

---

## 作業内容

### ステップ1: 対象プラグインを特定し値を導出

#### 条件

- 常に最初に実行

#### 処理内容

1. **対象プラグイン**のパス（例 `plugins/vue-kit`）を確認する。ディレクトリは既に存在すること。
2. **TTL**（再注入間隔の秒数、デフォルト `3600`）を決める。
3. プラグインのディレクトリ名（`{name}`）からプレースホルダ値を導出:

| プレースホルダ | 値 | 例（`vue-kit`） |
|---|---|---|
| `__PLUGIN_NAME__` | `name` | `vue-kit` |
| `__ENV_PREFIX__` | `name` を大文字化し英数以外の連続を `_` に | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | `ttl`（数値） | `3600` |

（`__PLUGIN_DESCRIPTION__` はここには無い — 説明はプラグインレベル。）

→ ステップ2へ

#### 出力

- 対象プラグインのパスと導出したプレースホルダ値が確定

---

### ステップ2: 注入ファイルをコピーしプレースホルダ置換

#### 条件

- ステップ1完了

#### 処理内容

`${CLAUDE_PLUGIN_ROOT}/templates/` 配下の**全ファイル**を `Read` し、対象プラグインの対応
パスに `Write` する。その際プレースホルダを導出値で置換する。テキストは置換、バイナリはそのまま。

| テンプレート（`templates/` 配下） | 出力先（対象プラグイン配下） |
|---|---|
| `hooks/scripts/inject_references.py` | `hooks/scripts/inject_references.py` |
| `hooks/scripts/_common.py` | `hooks/scripts/_common.py` |
| `hooks/hooks.json` | `hooks/hooks.json` |
| `hooks/templates/injection.md.j2` / `injection.jp.md.j2` | `hooks/templates/…`（同名） |
| `references/_index.yaml` / `_index.jp.yaml` | `references/…`（同名） |
| `references/_injection_rules.yaml` | `references/_injection_rules.yaml` |
| `references/CLAUDE.md` / `CLAUDE.jp.md` | `references/…`（同名） |
| `references/example/getting-started.md` | `references/example/getting-started.md` |

メモ:
- パスはテンプレートをそのまま反映 — 移動なし。
- `hooks.json` 内の `${CLAUDE_PLUGIN_ROOT}` はそのまま残す（Claude Code が実行時に展開）。
- **対象に既に `hooks/hooks.json` がある場合**（他のフックがある）: 上書きせず、`PreToolUse`（Edit/Write/MultiEdit/Read）エントリを既存ファイルにマージする。
- **対象に既に注入ファイルがある場合**（再適用 / 仕組み更新）: `hooks/*` は上書きするが、既存の `references/` の中身（_index.yaml / _injection_rules.yaml / 実 doc）はそのまま残し、欠けている雛形だけ補う。
- 書き込み後、対象プラグインの `hooks/` を grep して `__PLACEHOLDER__` が残っていないか確認する。

→ ステップ3へ

#### 出力

- 対象プラグインに注入フック・テンプレート・references 雛形が入る

---

### ステップ3: 報告と引き継ぎ

#### 条件

- ステップ2完了

#### 処理内容

1. 対象プラグインに書き込んだファイルを報告する。
2. 残りの手順（すべてプラグイン所有、このスキルの責務外）をユーザーに伝える:
   - `references/` を実際の doc で埋める（1 リファレンス = 1 ユースケース）。`references/example/` を置き換える
   - 各 doc の path + description を `references/_index.yaml`（+ `_index.jp.yaml`）に記入
   - `references/_injection_rules.yaml` で編集パスパターンを紐付け
   - 必要なら `settings.json` の `env` に `{ENV_PREFIX}_INJECTION_TTL` を設定
   - 新規プラグインなら `plugin.json` / `marketplace.json` を（`plugin-creator` で）用意し、プラグインの `CLAUDE.md` に注入フックの存在を記載
3. 仕組みをプラグインごとに手編集しない — `ref-inject` テンプレートを変えて再適用する。

#### 補足

- 対象プラグインが動くプロジェクトに `PyYAML` と `Jinja2` が必要。
