---
name: config
description: |
  When /dev-kit:config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい", "言語を有効にしたい", "TypeScript チェックを無効にしたい", "Markdown チェックを無効にしたい".
---

# dev-kit:config — Plugin Toggle Configuration

Interactively configures env toggle variables.
Loops through one-variable-at-a-time selection → value → scope → apply,
until the user chooses to finish.

---

## Managed Toggles

### Language opt-in toggles（デフォルト OFF — truthy で有効化）

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `DEV_KIT_PYTHON` | Python 参照注入（`*.py` 等を編集時） | 無効 |
| `DEV_KIT_HTML` | HTML/CSS/JS 参照注入（`*.html`/`*.css`/`*.js` 編集時） | 無効 |
| `DEV_KIT_NEXT` | Next.js 参照注入（`*.ts`/`*.tsx` 等を編集時） | 無効 |
| `DEV_KIT_MARKDOWN` | Markdown 参照注入（`*.md` 編集時） | 無効 |

**Opt-in polarity**: キー不在 = OFF（デフォルト無効）。truthy（`"true"` など）に設定 = ON。OFF に戻すにはキーを削除する。

### Feature toggles（デフォルト ON）

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `DEV_KIT_NEXT_TS_CHECK` | PostToolUse `tsc --noEmit`（`*.ts`/`*.tsx` 編集後） | 有効 |
| `DEV_KIT_MARKDOWN_CHECK` | Markdown frontmatter チェック（`*.md` 書き込み後） | 有効 |

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

For each managed toggle, check the `env` block of both settings files (project takes precedence):

**Opt-in polarity** (`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`):
- Key absent → **OFF**（デフォルト無効）
- Value in `("true", "1", "yes", "on")` → **ON**
- Otherwise → **OFF**

**Normal polarity** (`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`):
- Key absent → **ON**（デフォルト有効）
- Value in `("false", "0", "no", "off")` → **OFF**
- Otherwise → **ON**

Display a state table as text output:

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

→ Proceed to Step 2

---

### Step 2: Select env var to configure （ループ先頭）

#### Condition

- Step 1 complete（ループ時はここから再開）

#### Process

Output a numbered list as plain text, then end the turn and wait for user input:

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

**Do not call `AskUserQuestion` here** — use plain numbered list to avoid the 4-option cap.

If the user inputs `0` or `q` → jump to Step 5.
Otherwise parse the number and look up the corresponding var name.

→ Proceed to Step 3

---

### Step 3: Select value and scope

#### Condition

- Step 2 complete (a var was selected)

#### Process

Call `AskUserQuestion` tool with **2 questions in a single call**:

**Question 1 — 値** (options differ by polarity):

*Opt-in polarity vars* (`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`):
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- options:
  1. `"有効にする（\"true\" に設定）"` — description: `"この言語の参照注入を有効化する"`
  2. `"デフォルトに戻す（キー削除 = OFF）"` — description: `"env キーを削除してデフォルト無効に戻す"`

*Normal polarity vars* (`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`):
- question: `"{VAR_NAME} の値を設定"`
- header: `"値"`
- options:
  1. `"デフォルトに戻す（キー削除 = ON）"` — description: `"env キーを削除してデフォルト有効に戻す"`
  2. `"OFF（\"false\" に設定）"` — description: `"この機能を無効化する"`

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
   - *Opt-in polarity vars* (`DEV_KIT_PYTHON`, `DEV_KIT_HTML`, `DEV_KIT_NEXT`, `DEV_KIT_MARKDOWN`):
     - "有効にする" → set `env.{VAR_NAME}` to `"true"`
     - "デフォルトに戻す" → delete `env.{VAR_NAME}` key
   - *Normal polarity vars* (`DEV_KIT_NEXT_TS_CHECK`, `DEV_KIT_MARKDOWN_CHECK`):
     - "デフォルトに戻す" → delete `env.{VAR_NAME}` key
     - "OFF" → set `env.{VAR_NAME}` to `"false"`
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
| DEV_KIT_NEXT_TS_CHECK | ON | OFF | .claude/settings.json |
```

If no changes were made, report "変更なし".

→ Done.

---

## Notes

- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- `DEV_KIT_INJECTION_DISABLE` は逆極性のキルスイッチのため、このスキルでは管理しない（`plugin-config.md` 参照）
