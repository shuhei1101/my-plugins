---
name: setup
description: |
  Install work-kit hook scripts into the current project and configure .claude/settings.json.
  Manual invocation only — use /work-kit:setup to run.
disable-model-invocation: true
allowed-tools: Bash Read Write
---

# work-kit:setup — Install Hooks into Current Project

Copies the work-kit hook scripts to `.claude/hooks/work-kit/` and adds hook
configuration to `.claude/settings.json`.

After installation:
- `UserPromptSubmit`: injects PR task status into Claude's context on every prompt
- `Stop`: injects a reminder when unchecked tasks exist in the current PR

Plugin scripts are at: `${CLAUDE_SKILL_DIR}/../../scripts/`

---

## Tasks

### Step 1: Prepare the installation directory

#### Condition

- Always — run this before anything else

#### Input

- Current directory (project root)

#### Process

1. Confirm the current directory is a Git repository
2. Create `.claude/hooks/work-kit/`:

```bash
mkdir -p .claude/hooks/work-kit
```

→ Proceed to Step 2

#### Output

- `.claude/hooks/work-kit/` directory exists

#### Notes

##### Branching

- Not a Git repository → stop and ask the user

---

### Step 2: Copy hook scripts

#### Condition

- Step 1 complete

#### Input

- Plugin scripts at `${CLAUDE_SKILL_DIR}/../../scripts/`

#### Process

1. Copy `user-prompt-submit.py` to `.claude/hooks/work-kit/`:

```bash
cp "${CLAUDE_SKILL_DIR}/../../scripts/user-prompt-submit.py" .claude/hooks/work-kit/
```

2. Copy `stop.py` to `.claude/hooks/work-kit/`:

```bash
cp "${CLAUDE_SKILL_DIR}/../../scripts/stop.py" .claude/hooks/work-kit/
```

→ Proceed to Step 3

#### Output

- `.claude/hooks/work-kit/user-prompt-submit.py` copied
- `.claude/hooks/work-kit/stop.py` copied

---

### Step 3: Add hook configuration to settings.json

#### Condition

- Step 2 complete

#### Input

- `.claude/settings.json` (create from `{}` if it does not exist)

#### Process

1. Read `.claude/settings.json`
2. Merge the following into the existing `hooks` key (do not overwrite existing entries):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/work-kit/user-prompt-submit.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/work-kit/stop.py"
          }
        ]
      }
    ]
  }
}
```

3. Save `.claude/settings.json`

→ Proceed to Step 4

#### Output

- `.claude/settings.json` updated with work-kit hook configuration

#### Notes

##### Prohibitions

- Do not delete existing hook entries — merge only
- If `UserPromptSubmit` or `Stop` already exists, append to the array

---

### Step 4: Verify installation

#### Condition

- All files created and settings updated

#### Process

1. Confirm all installed files exist
2. Report completion to the user

#### Output

- Installation complete report

#### Notes

##### Checklist

- [ ] `.claude/hooks/work-kit/user-prompt-submit.py` — exists
- [ ] `.claude/hooks/work-kit/stop.py` — exists
- [ ] `.claude/settings.json` — contains `UserPromptSubmit` and `Stop` hook config

---

## References

### Hook behavior summary

| Hook event | When | Action |
|---|---|---|
| `UserPromptSubmit` | After user submits prompt, before Claude processes it | Injects PR task status into Claude's context |
| `Stop` | When Claude completes a response | Injects unchecked-task reminder into context |

### Correspondence table

| File path | Description |
|---|---|
| `.claude/hooks/work-kit/user-prompt-submit.py` | UserPromptSubmit hook script |
| `.claude/hooks/work-kit/stop.py` | Stop hook script |
| `.claude/settings.json` | Hook configuration (hooks key) |
| `docs/tasks/**/PR{N}.md` | PR task documents referenced by the hook scripts |
