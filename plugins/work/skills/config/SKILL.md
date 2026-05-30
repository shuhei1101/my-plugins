---
name: config
description: |
  When /work:config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい", "plugin config", or "workspace config".
---

# work:config — Plugin Toggle Configuration

Interactively configures env toggle variables.
Loops through one-variable-at-a-time selection → value → scope → apply,
until the user chooses to finish.

---

## Managed Toggles

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `WORK_PR_ENFORCEMENT` | UserPromptSubmit work-start 強制注入 | 有効 |
| `WORK_STOP_REMINDER` | Stop TODO/QA リマインダー注入 | 有効 |
| `WORK_USE_WORKTREE` | work-start での worktree 作成 | 有効 |
| `WORK_MERGE_PROPOSAL` | Stop フックでの `/work:merge` 提案 | 有効 |
| `WORK_MERGE_AUTO_HANDOFF` | merge Step 11 auto branch-reserve | 有効 |
| `AITUBER_NOTIFY` | Stop notify-aituber 通知（ユーザー設定） | 有効 |

**Normal polarity**: キー不在 = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

---

## Tasks

### Step 1: Read current state

#### Condition

- Always — run first

#### Process

Run:

```bash
cat .claude/settings.json 2>/dev/null || echo '{}'
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

For each managed toggle, check the `env` block of the relevant settings file:

- Key absent → **ON**（デフォルト有効）
- Value in `("false", "0", "no", "off")` → **OFF**
- Otherwise → **ON**（明示設定）

Display a state table as text output:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| WORK_PR_ENFORCEMENT | ON | .claude/settings.json |
| ...（以下同様）| | |
```

→ Proceed to Step 2

---

### Step 2: Select env var to configure （ループ先頭）

#### Condition

- Step 1 complete（ループ時はここから再開）

#### Process

Output a numbered list as plain text, then end the turn and wait for user input:

```
設定する変数の番号を入力してください（0 で終了）:

  1. [{state}] WORK_PR_ENFORCEMENT — UserPromptSubmit work-start 強制注入
  2. [{state}] WORK_STOP_REMINDER — Stop TODO/QA リマインダー注入
  3. [{state}] WORK_USE_WORKTREE — work-start での worktree 作成
  4. [{state}] WORK_MERGE_PROPOSAL — Stop フックでの merge 提案
  5. [{state}] WORK_MERGE_AUTO_HANDOFF — merge Step 11 auto pr-handoff
  6. [{state}] AITUBER_NOTIFY — Stop notify-aituber 通知
  0. 完了（終了）
```

**Do not call `AskUserQuestion` here** — use plain numbered list to avoid the 4-option cap.

If the user inputs `0` or `q` → jump to Step 5 (report).
Otherwise parse the number and look up the corresponding var name.

→ Proceed to Step 3

---

### Step 3: Select value and scope

#### Condition

- Step 2 complete (a var was selected)

#### Process

**Call `AskUserQuestion` tool** with 2 questions in a single call:

**Question 1 — 値**:
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- multiSelect: false
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除し、デフォルト有効に戻す"`
  2. `"OFF（"false" に設定）"` — description: `"この機能を無効化する"`

**Question 2 — スコープ**:
- question: `"どの settings.json に書き込みますか？"`
- header: `"スコープ"`
- options:
  1. `"プロジェクト（.claude/settings.json）"` — description: `"このリポジトリのみに適用"`
  2. `"ユーザー（~/.claude/settings.json）"` — description: `"全プロジェクトに適用"`
- multiSelect: false

Record both answers.

→ Proceed to Step 4

---

### Step 4: Apply change

#### Condition

- Step 3 complete

#### Process

1. Determine target file from scope answer:
   - プロジェクト → `.claude/settings.json`
   - ユーザー → `~/.claude/settings.json`
2. Read JSON from target file (use `{}` if absent)
3. Ensure `env` object exists
4. Apply change:
   - "デフォルトに戻す" → delete `env.{VAR_NAME}` key
   - "OFF" → set `env.{VAR_NAME}` to `"false"`
5. Write back with 2-space indent

Record the change (var name, old state → new state, file) for the final report.

→ Loop to Step 2

---

### Step 5: Report

#### Condition

- User input `0` or `q` in Step 2

#### Process

Output a summary of all changes made during this session:

```
## 変更完了

| env 変数 | 変更前 | 変更後 | 設定ファイル |
|---|---|---|---|
| WORK_STOP_REMINDER | ON | OFF | .claude/settings.json |
```

If no changes were made, report "変更なし".

→ Done.

---

## Notes

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- AITUBER_NOTIFY のデフォルトスコープは「ユーザー」だが、スコープはユーザーが毎回選択する
- dev-kit の env トグル（`DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT` / `DEV_KIT_MARKDOWN` / `DEV_KIT_NEXT_TS_CHECK`）は `/dev-kit:config` で設定する
- `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` は逆極性のキルスイッチのためこのスキルでは管理しない（`plugin-config.md` 参照）
