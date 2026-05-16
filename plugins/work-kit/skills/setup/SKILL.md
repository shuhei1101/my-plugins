---
name: setup
description: |
  Initialize the work-kit document structure in the current project by running the setup script.
  Creates docs/tasks/, docs/specs/, and docs/QA.md from templates.
  Manual invocation only — use /work-kit:setup.
disable-model-invocation: true
allowed-tools: Bash
---

# work-kit:setup — Initialize Document Structure

Expands the plugin's template into the project's docs directory.
The Python script handles file creation; Claude does not create files directly.

Expanded structure:
```
{docs_dir}/
├── tasks/      # Task / PR folders (created dynamically by work-start)
├── specs/      # Specification documents (empty initially)
└── QA.md       # Open questions
```

---

## Tasks

### Step 1: Confirm the docs directory path

#### Condition

- Always — run first

#### Process

1. Ask the user for the docs directory path (default: `docs`)

→ Proceed to Step 2

#### Output

- Docs directory path confirmed

---

### Step 2: Run the setup script

#### Condition

- Step 1 complete

#### Process

1. Run:

```bash
python "${CLAUDE_SKILL_DIR}/../../scripts/setup.py" {docs_dir}
```

→ Proceed to Step 3

#### Output

- Template expanded to `{docs_dir}`

---

### Step 3: Verify and report

#### Process

1. Confirm script output shows no errors
2. Report completion to the user

#### Notes

##### Checklist

- [ ] `{docs_dir}/tasks/` — exists
- [ ] `{docs_dir}/specs/` — exists
- [ ] `{docs_dir}/QA.md` — exists
