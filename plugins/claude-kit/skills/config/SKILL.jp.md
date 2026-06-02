---
name: config
description: |
  /claude-kit:config が呼び出されたとき。
  またはユーザーが「設定を変えたい」「env を設定したい」「トグルを切り替えたい」「JP ミラーを無効にしたい」「注入言語を変えたい」と言ったとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original (SKILL.md), update this file too. -->

# claude-kit:config — プラグイントグル設定

env 変数をインタラクティブに設定するスキル。
「変数選択 → 値設定 → スコープ選択 → 適用」のループを繰り返し、ユーザーが終了を選択するまで続ける。

---

## 管理対象変数

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `${CLAUDE_KIT_JP_MIRROR}` | JP ミラー（`.jp.md`）の作成 | 有効 |
| `${CLAUDE_KIT_INJECTION_LANG}` | 注入リファレンスの言語（`en` / `jp`） | `en` |
| `${CLAUDE_KIT_INJECTION_TTL}` | 注入トークンの TTL（秒） | `3600` |

**JP_MIRROR 極性**: キー不在または `"true"` = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

**INJECTION_LANG**: キー不在または `"en"` = 英語注入（デフォルト）。`"jp"` に設定 = 日本語注入。デフォルトに戻すにはキーを削除する。

**INJECTION_TTL**: キー不在 = 3600秒（デフォルト）。任意の整数（秒）を文字列で設定可能。デフォルトに戻すにはキーを削除する。

**除外**: `${CLAUDE_KIT_INJECTION_DISABLE}`（逆極性のキルスイッチ）はこのスキルで管理しない。

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

**`${CLAUDE_KIT_JP_MIRROR}`**:
- キー不在または `"true"/"1"/"yes"/"on"` → **ON**（デフォルト有効）
- `"false"/"0"/"no"/"off"` → **OFF**

**`${CLAUDE_KIT_INJECTION_LANG}`**:
- キー不在または `"en"` → **en**（デフォルト）
- `"jp"` → **jp**
- それ以外 → 設定値をそのまま表示

**`${CLAUDE_KIT_INJECTION_TTL}`**:
- キー不在 → **3600（デフォルト）**
- 値あり → その値を表示

状態テーブルをテキストで表示:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| CLAUDE_KIT_JP_MIRROR | ON | (未設定) |
| CLAUDE_KIT_INJECTION_LANG | en | (未設定) |
| CLAUDE_KIT_INJECTION_TTL | 3600（デフォルト） | (未設定) |
```

→ ステップ 2 へ進む

---

### ステップ 2: 設定する変数を選択（ループ先頭）

#### 条件

- ステップ 1 完了（ループ時はここから再開）

#### 処理

番号付きリストをプレーンテキストで出力し、ターンを終了してユーザーの入力を待つ:

```
設定する変数の番号を入力してください（0 で終了）:

  1. [ON]   CLAUDE_KIT_JP_MIRROR — JP ミラー作成
  2. [en]   CLAUDE_KIT_INJECTION_LANG — 注入言語
  3. [3600] CLAUDE_KIT_INJECTION_TTL — 注入 TTL（秒）
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

`AskUserQuestion` ツールを **1 回のコールで 2 つの質問** を送信。質問 1 の選択肢は変数の種類によって異なる:

**`${CLAUDE_KIT_JP_MIRROR}`（通常極性）の場合**:

- question: `"CLAUDE_KIT_JP_MIRROR の値を設定"`
- header: `"値"`
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除して JP ミラー作成を有効に戻す"`
  2. `"OFF（\"false\" に設定）"` — description: `"JP ミラー（.jp.md）の作成を無効にする"`

**`${CLAUDE_KIT_INJECTION_LANG}`（言語選択）の場合**:

- question: `"CLAUDE_KIT_INJECTION_LANG の値を設定"`
- header: `"言語"`
- options:
  1. `"en（デフォルト — キー削除）"` — description: `"英語注入に戻す（env キーを削除）"`
  2. `"jp（日本語注入）"` — description: `"日本語版リファレンスを注入する"`

**`${CLAUDE_KIT_INJECTION_TTL}`（整数値）の場合**:

- question: `"CLAUDE_KIT_INJECTION_TTL の値を設定"`
- header: `"TTL"`
- options:
  1. `"デフォルトに戻す（キー削除 = 3600秒）"` — description: `"env キーを削除して 3600 秒に戻す"`
  2. `"カスタム値を入力"` — description: `"秒数を直接入力する（例: 7200）"`

カスタム値を選択した場合は、入力された値を整数として解釈する（AskUserQuestion の「Other」入力で受け付ける）。

**質問 2 — スコープ**（すべての変数共通）:
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
   - **`${CLAUDE_KIT_JP_MIRROR}`**:
     - "デフォルトに戻す" → `env.CLAUDE_KIT_JP_MIRROR` キーを削除
     - "OFF" → `env.CLAUDE_KIT_JP_MIRROR` を `"false"` に設定
   - **`${CLAUDE_KIT_INJECTION_LANG}`**:
     - "en（デフォルト）" → `env.CLAUDE_KIT_INJECTION_LANG` キーを削除
     - "jp" → `env.CLAUDE_KIT_INJECTION_LANG` を `"jp"` に設定
     - Other（カスタム値）→ `env.CLAUDE_KIT_INJECTION_LANG` をその値に設定
   - **`${CLAUDE_KIT_INJECTION_TTL}`**:
     - "デフォルトに戻す" → `env.CLAUDE_KIT_INJECTION_TTL` キーを削除
     - カスタム値 → `env.CLAUDE_KIT_INJECTION_TTL` を入力値の文字列に設定
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
| CLAUDE_KIT_JP_MIRROR | ON | OFF | .claude/settings.json |
```

変更がなかった場合は「変更なし」と表示する。

→ 完了。

---

## 注意事項

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- `${CLAUDE_KIT_INJECTION_DISABLE}` は逆極性のキルスイッチのため、このスキルでは管理しない（`plugin-config.md` 参照）
- TTL に数値以外の文字列を設定しないこと — 整数値のみ有効
