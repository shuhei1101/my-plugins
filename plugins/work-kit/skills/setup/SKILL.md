---
name: setup
description: |
  Copy work-kit prompt files into the current project's .claude/hooks/work-kit/prompts/ directory.
  Hook configuration is applied automatically via hooks.json on plugin install.
  Manual invocation only — use /work-kit:setup.
disable-model-invocation: true
allowed-tools: Bash
---

# work-kit:setup — Copy Prompt Files into Current Project

Copies the work-kit prompt files to `.claude/hooks/work-kit/prompts/`.
Hook configuration (hooks.json) is applied automatically on plugin install;
this skill only handles placing the prompt files.

Plugin prompts are at: `${CLAUDE_SKILL_DIR}/../../prompts/`

---

## Tasks

### Step 1: Prepare the installation directory

#### Condition

- Always — run this before anything else

#### Process

1. Create `.claude/hooks/work-kit/prompts/`:

```bash
mkdir -p .claude/hooks/work-kit/prompts
```

→ Proceed to Step 2

#### Output

- `.claude/hooks/work-kit/prompts/` directory exists

---

### Step 2: Copy prompt files

#### Condition

- Step 1 complete

#### Input

- Plugin prompts at `${CLAUDE_SKILL_DIR}/../../prompts/`

#### Process

1. Copy `user-prompt-submit.md` to `.claude/hooks/work-kit/prompts/`:

```bash
cp "${CLAUDE_SKILL_DIR}/../../prompts/user-prompt-submit.md" .claude/hooks/work-kit/prompts/
```

2. Copy `stop.md` to `.claude/hooks/work-kit/prompts/`:

```bash
cp "${CLAUDE_SKILL_DIR}/../../prompts/stop.md" .claude/hooks/work-kit/prompts/
```

→ Proceed to Step 3

#### Output

- `.claude/hooks/work-kit/prompts/user-prompt-submit.md` copied
- `.claude/hooks/work-kit/prompts/stop.md` copied

---

### Step 3: Verify installation

#### Condition

- All files copied

#### Process

1. Confirm all installed files exist
2. Report completion to the user

#### Notes

##### Checklist

- [ ] `.claude/hooks/work-kit/prompts/user-prompt-submit.md` — exists
- [ ] `.claude/hooks/work-kit/prompts/stop.md` — exists
