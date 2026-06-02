---
name: ref-inject:plugin-config
description: |
  When /ref-inject:plugin-config is invoked.
  Or when the user says "ref-inject の設定を変えたい", "注入を無効にしたい".
---

# ref-inject:plugin-config — Plugin Toggle Configuration

Interactively configures env toggle variables for the ref-inject plugin.

> **Note**: ref-inject currently has no user-facing env toggles of its own.
> Consumer plugins (`dev-kit`, `claude-kit`) expose their own toggles via their respective
> `plugin-config` skills. This skill is a placeholder for future toggles.

---

## Managed Toggles

Currently no managed toggles.

---

## Tasks

### Step 1: Report current state

#### Condition

- Always — run first

#### Process

Inform the user:

```
ref-inject には現在ユーザー向けのトグルがありません。

注入動作を制御する場合は、各消費プラグインの plugin-config を使用してください:
  - /claude-kit:plugin-config — claude-kit の注入設定（JP ミラー / 言語 / TTL）
  - /dev-kit:plugin-config   — dev-kit の言語 opt-in および TypeScript チェック
```

→ Done.

---

## Notes

- ref-inject のキルスイッチ（`${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}`）は逆極性のため、各プラグインの plugin-config では管理しない — `settings.json` を直接編集すること
