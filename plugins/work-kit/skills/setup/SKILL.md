---
name: setup
description: |
  Copy work-kit hook scripts into the current project's .claude/hooks/work-kit/ directory.
  Hook configuration is applied automatically via hooks.json on plugin install.
  Manual invocation only — use /work-kit:setup.
disable-model-invocation: true
allowed-tools: Bash
---

# work-kit:setup — Copy Hook Scripts into Current Project

Copies the work-kit hook scripts to `.claude/hooks/work-kit/`.
Hook configuration (hooks.json) is applied automatically on plugin install;
this skill only handles placing the script files.

Plugin scripts are at: `${CLAUDE_SKILL_DIR}/../../scripts/`

---

## Tasks

### Step 1: Prepare the installation directory

#### Condition

- Always — run this before anything else

#### Process

1. Create `.claude/hooks/work-kit/`:

```bash
mkdir -p .claude/hooks/work-kit
```

→ Proceed to Step 2

#### Output

- `.claude/hooks/work-kit/` directory exists

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

### Step 3: Verify installation

#### Condition

- All files copied

#### Process

1. Confirm all installed files exist
2. Report completion to the user

#### Notes

##### Checklist

- [ ] `.claude/hooks/work-kit/user-prompt-submit.py` — exists
- [ ] `.claude/hooks/work-kit/stop.py` — exists
