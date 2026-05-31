---
name: plugin-config
description: |
  /work:plugin-config が呼び出されたとき。
  またはユーザーが「設定を変えたい」「env を設定したい」「トグルを切り替えたい」「plugin config」「workspace config」と言ったとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:plugin-config — プラグイントグル設定

env トグル変数をインタラクティブに設定するスキル。
「変数選択 → 値設定 → スコープ選択 → 適用」のループを繰り返し、ユーザーが終了を選択するまで続ける。

---

## 管理対象トグル

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `WORK_BRANCH_ENFORCEMENT` | UserPromptSubmit work-start 強制注入 | 有効 |
| `WORK_STOP_REMINDER` | Stop TODO/QA リマインダー注入 | 有効 |
| `WORK_USE_WORKTREE` | work-start での worktree 作成 | 有効 |
| `WORK_MERGE_PROPOSAL` | Stop フックでの `/work:merge` 提案 | 有効 |
| `WORK_MERGE_AUTO_HANDOFF` | merge Step 11 auto branch-reserve | 有効 |
| `WORK_COMMIT_TYPE` | コミットメッセージのタイププレフィックス付与 | 有効 |
| `AITUBER_NOTIFY` | Stop notify-aituber 通知（ユーザー設定） | 有効 |

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

管理対象の各トグルについて、該当の settings.json の `env` ブロックを確認:

- キー不在 → **ON**（デフォルト有効）
- 値が `("false", "0", "no", "off")` → **OFF**
- それ以外 → **ON**（明示設定）

状態テーブルをテキストで表示:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| WORK_BRANCH_ENFORCEMENT | ON | .claude/settings.json |
| ...（以下同様）| | |
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

  1. [{state}] WORK_BRANCH_ENFORCEMENT — UserPromptSubmit work-start 強制注入
  2. [{state}] WORK_STOP_REMINDER — Stop TODO/QA リマインダー注入
  3. [{state}] WORK_USE_WORKTREE — work-start での worktree 作成
  4. [{state}] WORK_MERGE_PROPOSAL — Stop フックでの merge 提案
  5. [{state}] WORK_MERGE_AUTO_HANDOFF — merge Step 11 auto pr-handoff
  6. [{state}] WORK_COMMIT_TYPE — コミットメッセージのタイププレフィックス付与
  7. [{state}] AITUBER_NOTIFY — Stop notify-aituber 通知
  0. 完了（終了）
```

**`AskUserQuestion` は使わない** — 4 選択肢上限を避けるためプレーンテキストリストを使用する。

ユーザーが `0` または `q` を入力 → ステップ 5（レポート）へジャンプ。
それ以外は番号を解析し、対応する変数名を取得する。

→ ステップ 3 へ進む

---

### ステップ 3: 値とスコープを選択

#### 条件

- ステップ 2 完了（変数が選択された）

#### 処理

`AskUserQuestion` ツールを **1 回のコールで 2 つの質問** を送信:

**質問 1 — 値**:
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- multiSelect: false
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除し、デフォルト有効に戻す"`
  2. `"OFF（"false" に設定）"` — description: `"この機能を無効化する"`

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
   - "デフォルトに戻す" → `env.{VAR_NAME}` キーを削除
   - "OFF" → `env.{VAR_NAME}` を `"false"` に設定
5. 2 スペースインデントで書き戻す

最終レポート用に変更を記録する（変数名、変更前の状態 → 変更後の状態、ファイル）。

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
| WORK_STOP_REMINDER | ON | OFF | .claude/settings.json |
```

変更がなかった場合は「変更なし」と表示する。

→ 完了。

---

## 注意事項

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- AITUBER_NOTIFY のデフォルトスコープは「ユーザー」だが、スコープはユーザーが毎回選択する
- dev-kit の env トグル（`DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT` / `DEV_KIT_MARKDOWN` / `DEV_KIT_NEXT_TS_CHECK`）は `/dev-kit:plugin-config` で設定する
- `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` は逆極性のキルスイッチのためこのスキルでは管理しない（`plugin-config.md` 参照）
