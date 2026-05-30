# Plugin Config Skill Guide

How to add a **config skill** to a Claude Code plugin — an interactive skill that lets users
toggle the plugin's env-variable-controlled features without manually editing `settings.json`.

Japanese mirror: `references/plugin-config.jp.md`

Reference implementation: `plugins/work/skills/plugin-config/SKILL.md` (the `work:plugin-config` skill).

---

## Why every plugin needs a config skill

Plugins expose opt-in / opt-out behaviors through environment variables (see `environment.md`).
Without a config skill, users must hand-edit JSON — easy to get wrong, hard to discover.

A config skill:
- Shows the current state of every toggle at a glance
- Lets users flip values with `AskUserQuestion` (no JSON editing)
- Handles scope (project vs user) transparently
- Encodes the "no-key = default-on" contract so users never accidentally leave a stale `"true"` value

---

## When to add a config skill

Add a config skill when the plugin has **one or more env toggles** the user is expected to change.
A plugin with only developer-facing internals (e.g. `*_INJECTION_TTL`) does not need one.

Minimum threshold: at least one user-facing ON/OFF toggle in the plugin's `CLAUDE.md`
`## Environment Variables` section.

---

## Managed toggle convention

All user-facing toggles follow the same contract:

| State | Representation |
|---|---|
| ON (default) | Key **absent** from the `env` block |
| OFF | `env.{KEY}` set to `"false"` |
| Explicit ON | `env.{KEY}` set to `"true"` (equivalent to absent; avoid unless clarity is needed) |

**Returning to default**: delete the key (`"デフォルトに戻す"` option) — do **not** set it to `"true"`.

Exception: `{PREFIX}_INJECTION_DISABLE` uses reversed polarity (truthy = off). Exclude it from
config-skill management; handle it separately via manual settings.json editing.

---

## Skill structure — the 5-step AskUserQuestion loop

```
Step 1: Read current state        → display state table
Step 2: Select env var (loop head) → AskUserQuestion (var selection + 完了 option)
Step 3: Select value + scope      → AskUserQuestion (2 questions in one call)
Step 4: Apply change              → edit settings.json; record change; loop to Step 2
Step 5: Report                    → summary table of all changes
```

### Step 1 — Read current state

```bash
cat .claude/settings.json 2>/dev/null || echo '{}'
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

For each toggle: absent → **ON**, `"false"/"0"/"no"/"off"` → **OFF**, anything else → **ON**.

Output a state table as text before calling `AskUserQuestion`:

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| FOO_BAR | ON | .claude/settings.json |
| FOO_BAZ | OFF | ~/.claude/settings.json |
```

### Step 2 — Select env var (loop head)

Output a numbered list of all managed toggles as plain text, then end the turn and wait for
the user to type a number (or `0` / `q` to finish):

```
設定する変数の番号を入力してください（0 で終了）:

  1. [{state}] {VAR_NAME_1} — {機能の説明}
  2. [{state}] {VAR_NAME_2} — {機能の説明}
  3. [{state}] {VAR_NAME_3} — {機能の説明}
  …
  0. 完了（終了）
```

**Do not call `AskUserQuestion` here** — a plain numbered list lets you show all toggles without
the 4-option cap.

If the user types `0` or `q` → jump to Step 5.
Otherwise parse the number, look up the corresponding var name, → proceed to Step 3.

### Step 3 — Select value and scope

Call `AskUserQuestion` with **2 questions in a single call**:

```yaml
# Question 1 — value
question: "{VAR_NAME} の値を設定"
header:   "値"
options:
  - label: "デフォルトに戻す（キー削除 = ON）"   description: "env キーを削除してデフォルト有効に戻す"
  - label: "OFF（\"false\" に設定）"            description: "この機能を無効化する"

# Question 2 — scope
question: "どの settings.json に書き込みますか？"
header:   "スコープ"
options:
  - label: "プロジェクト（.claude/settings.json）"    description: "このリポジトリのみに適用"
  - label: "ユーザー（~/.claude/settings.json）"     description: "全プロジェクトに適用"
```

### Step 4 — Apply change

1. Determine target file from scope answer
2. Read existing JSON (use `{}` if absent)
3. Ensure `env` object exists
4. Apply: "デフォルトに戻す" → delete key; "OFF" → `env.{KEY} = "false"`
5. Write back with 2-space indent
6. Record change (var, old state → new state, file) → loop to Step 2

### Step 5 — Report

```
## 変更完了

| env 変数 | 変更前 | 変更後 | 設定ファイル |
|---|---|---|---|
| FOO_BAR | ON | OFF | .claude/settings.json |
```

If no changes → "変更なし".

---

## Minimal SKILL.md template

```markdown
---
name: plugin-config
description: |
  When /{plugin-name}:plugin-config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい".
---

# {plugin-name}:plugin-config — Plugin Toggle Configuration

Interactively configures env toggle variables via `AskUserQuestion`.

---

## Managed Toggles

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `{PREFIX}_FOO` | {機能の説明} | 有効 |

**Rule**: キー不在 = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

---

## Tasks

### Step 1: Read current state
…
### Step 2: Select env var to configure （ループ先頭）
…
### Step 3: Select value and scope
…
### Step 4: Apply change
…
### Step 5: Report
…
```

---

## Checklist before shipping

- [ ] `## Environment Variables` in the plugin's `CLAUDE.md` lists every managed toggle
- [ ] Each toggle follows the absent = ON / `"false"` = OFF contract
- [ ] `{PREFIX}_INJECTION_DISABLE` (reversed polarity) is **excluded** from the config skill
- [ ] SKILL.md `description` frontmatter triggers on natural-language phrases like "設定を変えたい"
- [ ] Version bump + changelog entry for the plugin
