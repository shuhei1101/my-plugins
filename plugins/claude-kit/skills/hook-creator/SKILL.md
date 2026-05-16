---
name: hook-creator
description: |
  Create a prompt-injection hook — a hook that injects a text prompt into Claude's context at a specific event.
  Trigger when the user says "I want to give Claude instructions at a specific moment", "inject a prompt on hook",
  "create a hook that tells Claude to do X when Y happens", "hook でプロンプトを差し込みたい",
  "特定のタイミングで AI に指示を出したい", or invoked explicitly as `/claude-kit:hook-creator`.
---

# hook-creator — Prompt-Injection Hook Creator

Creates hooks that inject a text prompt into Claude's context when a specific event fires.
Unlike action hooks (which run external scripts to send notifications or run tests), these hooks
deliver instructions directly to Claude itself.

---

## Overview

Claude Code hooks fire automatically at specific points in a session.
There are two broad categories:

| Category | Purpose |
|---|---|
| Action hook | Run external processes — notifications, tests, etc. |
| **Prompt-injection hook** | Output text to stdout → injected into Claude's context (this skill's focus) |

How prompt injection works:
- `UserPromptSubmit` hook: stdout text → injected as `<system-reminder>` before Claude processes
- `Stop` hook: write text to stderr + exit(2) → Claude continues with that instruction
- `PreToolUse` hook: JSON `{"decision":"block","reason":"<prompt>"}` to stdout → block tool and inject instruction

---

## Tasks

### Step 1: Read the official hooks documentation

#### Condition

- Always — run first

#### Process

1. Fetch the official documentation:
   **https://code.claude.com/docs/en/hooks**

→ Proceed to Step 2

#### Output

- Hook event list, JSON schema, and return-value spec understood

---

### Step 2: Gather requirements

#### Condition

- Step 1 complete

#### Input

- User's description of what they want

#### Process

1. Confirm the following:

   | Question | Examples |
   |---|---|
   | **When should it fire?** | Every time the user submits a prompt / when Claude finishes / before a tool runs |
   | **What instruction should Claude receive?** | "Update TODO.md before finishing" / "Check lint before committing" |
   | **Where should the hook live?** | Plugin (`hooks/hooks.json`) / Project (`.claude/settings.json`) / User (`~/.claude/settings.json`) |

2. Infer the event name from the user's description and suggest it (see §References / Event mapping)

→ Proceed to Step 3

#### Output

- Event name, prompt content, and placement location confirmed

---

### Step 3: Choose the hook pattern

#### Condition

- Step 2 complete

#### Input

- Event name (from Step 2)

#### Process

1. Select the pattern matching the event (see §References / Hook patterns)
2. For `Stop` or `PreToolUse` block patterns: explain the `stop_hook_active` guard to the user

→ Proceed to Step 4

#### Output

- hooks.json snippet (draft)

---

### Step 4: Create the prompt file

#### Condition

- Step 3 complete

#### Input

- Prompt content (from Step 2)
- Placement location (from Step 2)

#### Process

1. Create the prompt file at the appropriate path:

   | Placement | Example path |
   |---|---|
   | Plugin | `plugins/{name}/hooks/prompts/{event-name}.md` |
   | Project | `.claude/hooks/{event-name}.md` |

2. Write the user's instruction text as-is into the file

→ Proceed to Step 5

#### Output

- Prompt file created

#### Notes

##### Important

- `Stop` hook prompts should be imperative commands: "Do X", "Verify Y before finishing"
- `UserPromptSubmit` hook prompts are treated as `<system-reminder>` — best for injecting context or standing instructions

---

### Step 5: Create or update hooks.json

#### Condition

- Step 4 complete

#### Input

- Event name, hook pattern, prompt file path

#### Process

1. Choose the file based on placement:

   | Placement | File | Shared |
   |---|---|---|
   | Plugin | `plugins/{name}/hooks/hooks.json` | ✅ Bundled with plugin |
   | Project (team) | `hooks` section in `.claude/settings.json` | ✅ Committed to git |
   | Project (local only) | `hooks` section in `.claude/settings.local.json` | ❌ Add to `.gitignore` |

2. Use the snippet from §References / Hook patterns

→ Proceed to Step 6

#### Output

- Hook entry added to `hooks.json` or `settings.json`

---

### Step 6: Report to the user

#### Condition

- Step 5 complete

#### Process

1. List all created/updated files
2. Tell the user how to verify the hook works:
   - Restart Claude Code so the hook is loaded
   - Trigger the target event and confirm `<system-reminder>` appears

#### Output

- File list and verification steps

#### Notes

##### Checklist

- [ ] Prompt file exists
- [ ] Hook entry added to hooks.json or settings.json
- [ ] Path variable matches placement (see §References / Path variables)

---

## References

### Event mapping

| User's description | Event name | When it fires |
|---|---|---|
| "every time the user submits" / "before Claude processes" | `UserPromptSubmit` | After user submits, before Claude processes |
| "when Claude finishes" / "after each response" / "on stop" | `Stop` | When Claude stops responding |
| "before a tool runs" / "before Bash" | `PreToolUse` | Before tool execution (can block) |
| "after a tool runs" / "after file edit" | `PostToolUse` | After tool execution |
| "at session start" | `SessionStart` | When the session starts |

### Path variables

| Variable | Where usable | Meaning |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | **Plugin hooks.json only** | Plugin installation root |
| `${CLAUDE_PROJECT_DIR}` | settings.json / settings.local.json | Project root |
| `${CLAUDE_PLUGIN_DATA}` | Plugin hooks.json only | Plugin persistent data directory |

> ⚠️ `${CLAUDE_PLUGIN_ROOT}` is only expanded when installed as a plugin.
> In project-level settings.json it does nothing — use `${CLAUDE_PROJECT_DIR}` instead.

---

### Hook patterns

#### [Plugin] UserPromptSubmit

Place in the plugin's `hooks/hooks.json`. `${CLAUDE_PLUGIN_ROOT}` is available.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else sys.exit(0)",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/user-prompt-submit.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [Project] UserPromptSubmit

Place in `.claude/settings.json` or `.claude/settings.local.json`.
Prompt file lives at `.claude/hooks/{name}.md`.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else sys.exit(0)",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/user-prompt-submit.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [Plugin] Stop — inject a prompt and make Claude continue working

The `stop_hook_active` guard prevents infinite loops.
Write the prompt text to stderr and exit with code 2 to signal "block and continue".

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); (sys.stderr.buffer.write(p.read_text('utf-8').encode('utf-8')),sys.exit(2)) if p.exists() else None",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [Project] Stop

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); (sys.stderr.buffer.write(p.read_text('utf-8').encode('utf-8')),sys.exit(2)) if p.exists() else None",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [Project] PreToolUse — block tool and inject prompt

Use `matcher` to target specific tools.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else sys.exit(0)",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.md"
            ]
          }
        ]
      }
    ]
  }
}
```
