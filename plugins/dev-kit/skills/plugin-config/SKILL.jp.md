---
name: dev-kit:plugin-config
description: |
  /dev-kit:plugin-config が呼び出されたとき。
  またはユーザーが「設定を変えたい」「env を設定したい」「トグルを切り替えたい」「言語を有効にしたい」「TypeScript チェックを無効にしたい」「Markdown チェックを無効にしたい」と言ったとき。
---
<!-- This file is a Japanese mirror. When updating the English original (SKILL.md), update this file too. -->

# dev-kit:plugin-config — プラグイントグル設定

env トグル変数をインタラクティブに設定するスキル。
「変数選択 → 値設定 → スコープ選択 → 適用」のループを繰り返し、ユーザーが終了を選択するまで続ける。

---

## 管理対象トグル

### 言語 opt-in トグル（デフォルト OFF — truthy で有効化）

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `DEV_KIT_PYTHON` | Python 参照注入（`*.py` 等を編集時） | 無効 |
| `DEV_KIT_HTML` | HTML/CSS/JS 参照注入（`*.html`/`*.css`/`*.js` 編集時） | 無効 |
| `DEV_KIT_NEXT` | Next.js 参照注入（`*.ts`/`*.tsx` 等を編集時） | 無効 |
| `DEV_KIT_MARKDOWN` | Markdown 参照注入（`*.md` 編集時） | 無効 |

**Opt-in 極性**: キー不在 = OFF（デフォルト無効）。truthy（`"true"` など）に設定 = ON。OFF に戻すにはキーを削除する。

### 機能トグル（デフォルト ON）

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `DEV_KIT_NEXT_TS_CHECK` | PostToolUse `tsc --noEmit`（`*.ts`/`*.tsx` 編集後） | 有効 |
| `DEV_KIT_MARKDOWN_CHECK` | Markdown frontmatter チェック（`*.md` 書き込み後） | 有効 |

**通常極性**: キー不在 = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

---

## タスク

### ステップ 1: 現在の状態を読み取る

#### 条件

- 常に実行 — 最初に行う

#### 処理

以下を実行:

```bash
cat .claude/settings.json 2>/dev/null || echo '{}'
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

両ファイルの `env` ブロックを確認し（プロジェクト設定が優先）:

**Opt-in 極性**（`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`）:
- キー不在 → **OFF**（デフォルト無効）
- 値が `("true", "1", "yes", "on")` → **ON**
- それ以外 → **OFF**

**通常極性**（`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`）:
- キー不在 → **ON**（デフォルト有効）
- 値が `("false", "0", "no", "off")` → **OFF**
- それ以外 → **ON**

状態テーブルをテキストで表示:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| DEV_KIT_PYTHON | OFF | (未設定) |
| DEV_KIT_HTML | OFF | (未設定) |
| DEV_KIT_NEXT | OFF | (未設定) |
| DEV_KIT_MARKDOWN | OFF | (未設定) |
| DEV_KIT_NEXT_TS_CHECK | ON | (未設定) |
| DEV_KIT_MARKDOWN_CHECK | ON | (未設定) |
```

→ ステップ 2 へ進む

---

### ステップ 2: 設定する env 変数を選択（ループ先頭）

#### 条件

- ステップ 1 完了（ループ時はここから再開）

#### 処理

番号付きリストをプレーンテキストで出力し、ターンを終了してユーザーの入力を待つ:

```
設定する変数の番号を入力してください（0 で終了）:

  1. [OFF] DEV_KIT_PYTHON — Python 参照注入
  2. [OFF] DEV_KIT_HTML — HTML/CSS/JS 参照注入
  3. [OFF] DEV_KIT_NEXT — Next.js 参照注入
  4. [OFF] DEV_KIT_MARKDOWN — Markdown 参照注入
  5. [ON]  DEV_KIT_NEXT_TS_CHECK — TypeScript 型チェック
  6. [ON]  DEV_KIT_MARKDOWN_CHECK — Markdown frontmatter チェック
  0. 完了（終了）
```

**`AskUserQuestion` は使わない** — 4 選択肢上限を避けるためプレーンテキストリストを使用する。

ユーザーが `0` または `q` を入力 → ステップ 5 へジャンプ。
それ以外は番号を解析し、対応する変数名を取得する。

→ ステップ 3 へ進む

---

### ステップ 3: 値とスコープを選択

#### 条件

- ステップ 2 完了（変数が選択された）

#### 処理

`AskUserQuestion` ツールを **1 回のコールで 2 つの質問** を送信:

**質問 1 — 値**（極性によって選択肢が異なる）:

*Opt-in 極性変数*（`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`）:
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- options:
  1. `"有効にする（\"true\" に設定）"` — description: `"この言語の参照注入を有効化する"`
  2. `"デフォルトに戻す（キー削除 = OFF）"` — description: `"env キーを削除してデフォルト無効に戻す"`

*通常極性変数*（`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`）:
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除してデフォルト有効に戻す"`
  2. `"OFF（\"false\" に設定）"` — description: `"この機能を無効化する"`

**質問 2 — スコープ**:
- question: `"どの settings.json に書き込みますか？"`
- header: `"スコープ"`
- options:
  1. `"プロジェクト（.claude/settings.json）"` — description: `"このリポジトリのみに適用"`
  2. `"ユーザー（~/.claude/settings.json）"` — description: `"全プロジェクトに適用"`
- multiSelect: false

両方の回答を記録する。

→ ステップ 4 へ進む

---

### ステップ 4: 変更を適用

#### 条件

- ステップ 3 完了

#### 処理

1. スコープの回答からターゲットファイルを決定:
   - プロジェクト → `.claude/settings.json`
   - ユーザー → `~/.claude/settings.json`
2. ターゲットファイルから JSON を読み込む（存在しない場合は `{}` を使用）
3. `env` オブジェクトが存在することを確認
4. 変更を適用:
   - *Opt-in 極性変数*（`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`）:
     - "有効にする" → `env.{VAR_NAME}` を `"true"` に設定
     - "デフォルトに戻す" → `env.{VAR_NAME}` キーを削除
   - *通常極性変数*（`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`）:
     - "デフォルトに戻す" → `env.{VAR_NAME}` キーを削除
     - "OFF" → `env.{VAR_NAME}` を `"false"` に設定
5. 2 スペースインデントで書き戻す
6. 変更を記録する（変数名、変更前の状態 → 変更後の状態、ファイル）

→ ステップ 2 へループ

---

### ステップ 5: レポート

#### 条件

- ステップ 2 でユーザーが `0` または `q` を入力

#### 処理

このセッション中に行ったすべての変更のサマリーを出力:

```
## 変更完了

| env 変数 | 変更前 | 変更後 | 設定ファイル |
|---|---|---|---|
| DEV_KIT_NEXT_TS_CHECK | ON | OFF | .claude/settings.json |
```

変更がなかった場合は「変更なし」と表示する。

→ 完了。

---

## 注意事項

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- `DEV_KIT_INJECTION_DISABLE` は逆極性のキルスイッチのため、このスキルでは管理しない（`plugin-config.md` 参照）
