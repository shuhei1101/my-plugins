---
name: claude-kit:config
description: |
  When /claude-kit:config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい", "JP ミラーを無効にしたい", "注入言語を変えたい".
---

# claude-kit:config — Plugin Toggle Configuration

Interactively configures env variables.
Loops through variable selection → value → scope → apply,
until the user chooses to finish.

---

## Managed Variables

| env var | Description | Default |
|---|---|---|
| `CLAUDE_KIT_JP_MIRROR` | Create JP mirror (`.jp.md`) files | ON |
| `CLAUDE_KIT_INJECTION_LANG` | Language for injected references (`en` / `jp`) | `en` |
| `CLAUDE_KIT_INJECTION_TTL` | Injection token TTL (seconds) | `3600` |

**JP_MIRROR polarity**: Key absent or `"true"` = ON (default). `"false"` = OFF. To return to default, delete the key.

**INJECTION_LANG**: Key absent or `"en"` = English injection (default). `"jp"` = Japanese injection. To return to default, delete the key.

**INJECTION_TTL**: Key absent = 3600 seconds (default). Any integer (seconds) as a string. To return to default, delete the key.

**Excluded**: `CLAUDE_KIT_INJECTION_DISABLE` (reversed-polarity kill switch) is not managed by this skill.

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

For each variable, check the `env` block of both settings files (project takes precedence):

**CLAUDE_KIT_JP_MIRROR**:
- Key absent or `"true"/"1"/"yes"/"on"` → **ON** (default)
- `"false"/"0"/"no"/"off"` → **OFF**

**CLAUDE_KIT_INJECTION_LANG**:
- Key absent or `"en"` → **en** (default)
- `"jp"` → **jp**
- Anything else → display the raw value

**CLAUDE_KIT_INJECTION_TTL**:
- Key absent → **3600 (default)**
- Value present → display the value

Display a state table as text output:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| CLAUDE_KIT_JP_MIRROR | ON | (未設定) |
| CLAUDE_KIT_INJECTION_LANG | en | (未設定) |
| CLAUDE_KIT_INJECTION_TTL | 3600（デフォルト） | (未設定) |
```

→ Proceed to Step 2

---

### Step 2: Select variable to configure （ループ先頭）

#### Condition

- Step 1 complete（ループ時はここから再開）

#### Process

Output a numbered list as plain text, then end the turn and wait for user input:

```
設定する変数の番号を入力してください（0 で終了）:

  1. [ON]   CLAUDE_KIT_JP_MIRROR — JP ミラー作成
  2. [en]   CLAUDE_KIT_INJECTION_LANG — 注入言語
  3. [3600] CLAUDE_KIT_INJECTION_TTL — 注入 TTL（秒）
  0. 完了（終了）
```

**Do not call `AskUserQuestion` here** — use plain numbered list to avoid the 4-option cap.

If the user inputs `0` or `q` → jump to Step 5.
Otherwise parse the number and look up the corresponding var name.

→ Proceed to Step 3

---

### Step 3: Select value and scope

#### Condition

- Step 2 complete (a variable was selected)

#### Process

Call `AskUserQuestion` with **2 questions in a single call**. Question 1 options differ by variable type:

**For `CLAUDE_KIT_JP_MIRROR` (normal polarity)**:

- question: `"CLAUDE_KIT_JP_MIRROR の値を設定"`
- header: `"値"`
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除して JP ミラー作成を有効に戻す"`
  2. `"OFF（\"false\" に設定）"` — description: `"JP ミラー（.jp.md）の作成を無効にする"`

**For `CLAUDE_KIT_INJECTION_LANG` (language selection)**:

- question: `"CLAUDE_KIT_INJECTION_LANG の値を設定"`
- header: `"言語"`
- options:
  1. `"en（デフォルト — キー削除）"` — description: `"英語注入に戻す（env キーを削除）"`
  2. `"jp（日本語注入）"` — description: `"日本語版リファレンスを注入する"`

**For `CLAUDE_KIT_INJECTION_TTL` (integer value)**:

- question: `"CLAUDE_KIT_INJECTION_TTL の値を設定"`
- header: `"TTL"`
- options:
  1. `"デフォルトに戻す（キー削除 = 3600秒）"` — description: `"env キーを削除して 3600 秒に戻す"`
  2. `"カスタム値を入力"` — description: `"秒数を直接入力する（例: 7200）"`

For the custom value option, accept the user's typed value via AskUserQuestion "Other" input and interpret it as an integer string.

**Question 2 — scope** (all variables):
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
   - **CLAUDE_KIT_JP_MIRROR**:
     - "デフォルトに戻す" → delete `env.CLAUDE_KIT_JP_MIRROR` key
     - "OFF" → set `env.CLAUDE_KIT_JP_MIRROR` to `"false"`
   - **CLAUDE_KIT_INJECTION_LANG**:
     - "en（デフォルト）" → delete `env.CLAUDE_KIT_INJECTION_LANG` key
     - "jp" → set `env.CLAUDE_KIT_INJECTION_LANG` to `"jp"`
     - Other (custom) → set `env.CLAUDE_KIT_INJECTION_LANG` to the entered value
   - **CLAUDE_KIT_INJECTION_TTL**:
     - "デフォルトに戻す" → delete `env.CLAUDE_KIT_INJECTION_TTL` key
     - Custom value → set `env.CLAUDE_KIT_INJECTION_TTL` to the entered value as a string
5. Write back with 2-space indent
6. Record the change (var name, old state → new state, file)

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
| CLAUDE_KIT_JP_MIRROR | ON | OFF | .claude/settings.json |
```

If no changes were made, report "変更なし".

→ Done.

---

## Notes

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- `CLAUDE_KIT_INJECTION_DISABLE` は逆極性のキルスイッチのため、このスキルでは管理しない（`plugin-config.md` 参照）
- TTL には整数値のみ設定すること
