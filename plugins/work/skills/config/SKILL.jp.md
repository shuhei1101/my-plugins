---
name: config
description: |
  /work:config が呼び出されたとき。
  またはユーザーが「設定を変えたい」「env を設定したい」「トグルを切り替えたい」「plugin config」「workspace config」と言ったとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:config — プラグイントグル設定

env トグル変数を `AskUserQuestion` を使って対話的に設定します。
1つの変数ごとに選択 → 値 → スコープ → 適用をループして進めます。
ユーザーが終了を選ぶまで続きます。

---

## 管理対象トグル

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `WORK_KIT_PR_ENFORCEMENT` | UserPromptSubmit work-start 強制注入 | 有効 |
| `WORK_KIT_STOP_REMINDER` | Stop TODO/QA リマインダー注入 | 有効 |
| `WORK_KIT_USE_WORKTREE` | work-start での worktree 作成 | 有効 |
| `WORK_KIT_MERGE_PROPOSAL` | Stop フックでの `/work-kit:merge` 提案 | 有効 |
| `WORK_KIT_MERGE_AUTO_HANDOFF` | merge Step 11 auto pr-handoff | 有効 |
| `NEXT_KIT_TS_CHECK` | PostToolUse tsc 型チェック | 有効 |
| `AITUBER_NOTIFY` | Stop notify-aituber 通知（ユーザー設定） | 有効 |
| `CLAUDE_KIT_INJECTION_DISABLE` | claude-kit の全参照注入を無効化（逆極性） | 有効（注入 ON） |
| `DEV_KIT_INJECTION_DISABLE` | dev-kit の全参照注入を無効化（逆極性） | 有効（注入 ON） |

**通常極性**：キー不在 = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

**逆極性**（`INJECTION_DISABLE` 系）：キー不在 = ON（注入有効）。truthy（`"true"` など）に設定 = OFF（注入無効）。ON に戻すにはキーを削除する。

---

## タスク

### ステップ 1: 現在の状態を読む

#### 条件

- 常に実行 — 最初に実行します

#### 処理

以下を実行します：

```bash
cat .claude/settings.json 2>/dev/null || echo '{}'
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

管理対象の各トグルについて、該当の settings.json の `env` ブロックを確認します：

**通常極性変数**（`INJECTION_DISABLE` 以外）:
- キー不在 → **ON**（デフォルト有効）
- 値が `("false", "0", "no", "off")` 内にある → **OFF**
- その他 → **ON**（明示的に設定）

**逆極性変数**（`CLAUDE_KIT_INJECTION_DISABLE`、`DEV_KIT_INJECTION_DISABLE`）:
- キー不在 → **ON**（注入有効）
- 値が `("true", "1", "yes", "on")` 内にある → **OFF**（注入無効）
- その他 → **ON**（注入有効）

状態テーブルをテキスト出力として表示します：

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| WORK_KIT_PR_ENFORCEMENT | ON | .claude/settings.json |
| ...（以下同様）| | |
```

→ ステップ 2 へ

---

### ステップ 2: 設定する env 変数を選択（ループ先頭）

#### 条件

- Step 1 完了（ループ時はここから再開）

#### 処理

**`AskUserQuestion` ツールを呼び出します** `multiSelect: false` で：

- question: `"設定する env 変数を選択（MERGE_PROPOSAL / MERGE_AUTO_HANDOFF / NEXT_KIT_TS_CHECK / AITUBER_NOTIFY / CLAUDE_KIT_INJECTION_DISABLE / DEV_KIT_INJECTION_DISABLE は「その他」に入力）"`
- header: `"env 変数"`
- options（各ラベルに現在の状態を含める）:
  1. `"[{state}] WORK_KIT_PR_ENFORCEMENT"` — description: `"UserPromptSubmit work-start 強制注入"`
  2. `"[{state}] WORK_KIT_STOP_REMINDER"` — description: `"Stop TODO/QA リマインダー注入"`
  3. `"[{state}] WORK_KIT_USE_WORKTREE"` — description: `"work-start での worktree 作成"`
  4. `"完了（設定を終了）"` — description: `"ループを終了して変更結果を表示"`

option 4（完了）が選ばれた場合 → Step 5（レポート）に飛びます
「その他」（自由入力）の場合 → 入力されたテキストを対象変数として使用; 進める前に 9 つの管理対象変数のいずれかであることを検証します
その他の場合 → 選択されたオプションの変数名を使用します

→ ステップ 3 へ

---

### ステップ 3: 値とスコープを選択

#### 条件

- Step 2 完了（変数が選択された）

#### 処理

**`AskUserQuestion` ツールを呼び出します** 1 回の呼び出しで 2 つの質問を含めて：

**質問 1 — 値**（選択した変数が逆極性かどうかで options を切り替える）:

- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- multiSelect: false

*通常極性変数*（`INJECTION_DISABLE` 以外）:
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除し、デフォルト有効に戻す"`
  2. `"OFF（"false" に設定）"` — description: `"この機能を無効化する"`

*逆極性変数*（`CLAUDE_KIT_INJECTION_DISABLE`、`DEV_KIT_INJECTION_DISABLE`）:
- options:
  1. `"デフォルトに戻す（キー削除 = 注入 ON）"` — description: `"env キーを削除し、注入有効に戻す"`
  2. `"無効にする（"true" に設定 = 注入 OFF）"` — description: `"参照注入を無効化する"`

**質問 2 — スコープ**:
- question: `"どの settings.json に書き込みますか？"`
- header: `"スコープ"`
- options:
  1. `"プロジェクト（.claude/settings.json）"` — description: `"このリポジトリのみに適用"`
  2. `"ユーザー（~/.claude/settings.json）"` — description: `"全プロジェクトに適用"`
- multiSelect: false

両方の答えを記録します。

→ ステップ 4 へ

---

### ステップ 4: 変更を適用

#### 条件

- Step 3 完了

#### 処理

1. スコープの答えからターゲットファイルを決定します：
   - プロジェクト → `.claude/settings.json`
   - ユーザー → `~/.claude/settings.json`
2. ターゲットファイルから JSON を読み込みます（不在の場合は `{}` を使用）
3. `env` オブジェクトが存在することを確認します
4. 変更を適用します：
   - *通常極性変数*:
     - 「デフォルトに戻す」 → `env.{VAR_NAME}` キーを削除します
     - 「OFF」 → `env.{VAR_NAME}` を `"false"` に設定します
   - *逆極性変数*（`CLAUDE_KIT_INJECTION_DISABLE`、`DEV_KIT_INJECTION_DISABLE`）:
     - 「デフォルトに戻す」 → `env.{VAR_NAME}` キーを削除します
     - 「無効にする」 → `env.{VAR_NAME}` を `"true"` に設定します
5. 2 スペースインデントで書き込みます

最終レポート用に変更を記録します（変数名、変更前の状態 → 変更後の状態、ファイル）。

→ ステップ 2 に戻る

---

### ステップ 5: レポート

#### 条件

- ユーザーが Step 2 で「完了」を選択

#### 処理

このセッション中に行われたすべての変更の概要を出力します：

```
## 変更完了

| env 変数 | 変更前 | 変更後 | 設定ファイル |
|---|---|---|---|
| WORK_KIT_STOP_REMINDER | ON | OFF | .claude/settings.json |
```

変更がない場合は「変更なし」と報告します。

→ 完了。

---

## 注釈

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- AITUBER_NOTIFY のデフォルトスコープは「ユーザー」だが、スコープはユーザーが毎回選択する
