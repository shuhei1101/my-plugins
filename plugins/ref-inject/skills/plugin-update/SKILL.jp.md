---
name: plugin-update
description: |
  ref-inject が適用済みのプラグイン（hooks/scripts/inject_references.py の存在で判定）を検査し、
  注入の仕組みファイルを現行の ref-inject テンプレートに揃える。references/ の内容（ユーザー作成の
  doc・_index.yaml・_injection_rules.yaml）は一切変更しない — hooks/ 配下の仕組みファイルだけを更新する。
  手動起動のみ — /ref-inject:plugin-update を使う。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# ref-inject:plugin-update — コンシューマープラグインの注入の仕組みを更新

**全 ref-inject コンシューマー**の注入フックファイルを、現行の ref-inject テンプレートに揃える。
`/ref-inject:apply` が初回導入を行うのに対し、`plugin-update` はテンプレート変更が生じたときに仕組みを最新化し続ける。

`references/` の内容（ユーザー作成の doc・`_index.yaml`・`_injection_rules.yaml`）は
**一切変更しない** — 更新対象は `hooks/` 配下の仕組みファイルのみ。

---

## "コンシューマー" の定義

プラグインが `hooks/scripts/inject_references.py` を持つ場合、そのプラグインは ref-inject コンシューマーとみなす。
このファイルは `/ref-inject:apply` が残す正規のマーカー。

---

## このスキルが更新する仕組みファイル

| ファイル | 処理 |
|---|---|
| `hooks/scripts/inject_references.py` | 現行テンプレート（プレースホルダ置換済み）で上書き |
| `hooks/scripts/_common.py` | 現行テンプレートで上書き |
| `hooks/templates/injection.md.j2` | 現行テンプレートで上書き |
| `hooks/templates/injection.jp.md.j2` | 現行テンプレートで上書き |
| `hooks/hooks.json` | `PreToolUse(Edit\|Write\|MultiEdit\|Read)` エントリをマージ、他のフックはそのまま |

---

## 作業内容

### ステップ1: コンシューマープラグインを列挙

#### 条件

- 常に — 最初に実行

#### 処理内容

1. 以下を実行する:
   ```bash
   find . -path '*/hooks/scripts/inject_references.py' \
     -not -path '*/ref-inject/templates/*' \
     -not -path '*/.git/*'
   ```
2. 各結果は `{plugin_root}/hooks/scripts/inject_references.py` の位置にある。
   それぞれのマッチから `{plugin_root}`（例: `plugins/claude-kit`）を導出する。
3. コンシューマーが見つからない場合 → 「ref-inject コンシューマーが見つかりません。」と報告して終了。

→ ステップ2へ

#### 出力

- コンシューマープラグインのルート一覧が確定（例: `plugins/claude-kit`、`plugins/dev-kit`）

---

### ステップ2: 各コンシューマーのプレースホルダ値を導出

#### 条件

- ステップ1完了

#### 処理内容

各コンシューマーのプラグインルート（`{plugin_root}`）について、**ディレクトリ名**（`{name}` = パスの最後のセグメント）からプレースホルダ値を導出する:

| プレースホルダ | 導出方法 | 例（`claude-kit`） |
|---|---|---|
| `__PLUGIN_NAME__` | `name` | `claude-kit` |
| `__ENV_PREFIX__` | `name` を大文字化し英数以外の連続を `_` に | `CLAUDE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `claude-kit-references-injection` |
| `__DEFAULT_TTL__` | コンシューマーの既存 `.py` の最初の TTL 行から取得; なければ `3600` | `3600` |

→ ステップ3へ

#### 出力

- 各コンシューマーのプレースホルダマップが確定

---

### ステップ3: 仕組みファイルを比較して報告

#### 条件

- ステップ2完了

#### 処理内容

各コンシューマープラグインについて:

1. `${CLAUDE_PLUGIN_ROOT}/templates/hooks/` から4つのテンプレートファイルを読む:
   - `scripts/inject_references.py`
   - `scripts/_common.py`
   - `templates/injection.md.j2`
   - `templates/injection.jp.md.j2`

2. `inject_references.py` は4つのプレースホルダをコンシューマーの導出値で置換する。
   他の3ファイルはプレースホルダなし — そのまま比較する。

3. コンシューマーの現行バージョンの同4ファイルを読む。

4. 比較する。差分があるファイルを **要更新** としてメモする。

5. `hooks.json` について: テンプレートの `hooks.json` とコンシューマーの `hooks.json` を読む。
   コンシューマーの `PreToolUse(Edit|Write|MultiEdit|Read)` エントリがテンプレートのエントリと
   一致するか確認する。異なれば **要マージ** としてメモする。

6. コンシューマーごとに調査結果をまとめる:
   - **最新**: 差分なし
   - **要更新**: 差分があるファイルの一覧

→ ステップ4へ

#### 出力

- コンシューマーごとの差分サマリーをユーザーに表示

---

### ステップ4: 更新を適用（ユーザー確認あり）

#### 条件

- ステップ3完了
- 更新が必要なファイルを持つコンシューマーが1つ以上ある

#### 処理内容

1. ステップ4 のコンシューマーごとのサマリーを表示する。
2. ユーザーに確認する: 「全コンシューマーの仕組みファイルを更新しますか？（yes / スキップするプラグインを指定）」
3. ユーザーが承認した各コンシューマーについて:

   a. 4つのフックスクリプトとテンプレートを**上書き**する（該当箇所はプレースホルダを置換）。

   b. **`hooks.json` をマージ**: ファイル全体を上書きしない — `PreToolUse(Edit|Write|MultiEdit|Read)` エントリを見つけてテンプレートのエントリに差し替える。コンシューマーの `hooks.json` にある他のエントリはそのまま保持する。

4. 各コンシューマーへの書き込み後、`{plugin_root}/hooks/` を grep して残存する `__PLACEHOLDER__` トークンがないか確認し、あれば報告する。

→ ステップ5へ

#### 注意

##### 禁止事項

- `references/` の内容（doc・`_index.yaml`・`_injection_rules.yaml`・`CLAUDE.md`）を上書きしない
- `hooks.json` を全体置換しない — PreToolUse エントリは必ずインプレースでマージする

---

### ステップ5: 完了報告

#### 条件

- ステップ4完了

#### 処理内容

1. コンシューマーごとに更新したファイルを一覧表示する。
2. `git diff` を表示する（大きい場合は省略）。
3. コンシューマーのファイルに変更がなかった場合は「Already up to date」と報告する。
4. コミットメッセージ案を提示する:
   - `chore: sync ref-inject injection hook to v{N}`
   - `{N}` は `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` から取得
5. **このスキルはコミットしない** — コミットはユーザーの責務。

→ 完了

#### 注意

##### 禁止事項

- 自動コミット
