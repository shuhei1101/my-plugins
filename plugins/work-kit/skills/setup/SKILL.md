---
name: setup
description: |
  Initialize the work-kit document structure (tasks dir, index.yaml, qa.md) in the current project.
  Manual invocation only — use /work-kit:setup.
disable-model-invocation: true
allowed-tools: Bash Read Write
---

# work-kit:setup — Initialize Document Structure

Creates the task management folder, PR index (`index.yaml`), and QA documents
in the current project. Run once when adopting work-kit in a new project.

---

## Tasks

### Step 1: Confirm the tasks directory location

#### Condition

- Always — run first

#### Process

1. Ask the user for the tasks directory path (default: `docs/tasks/`)
2. If the path already exists, confirm before proceeding

→ Proceed to Step 2

#### Output

- Tasks directory path is confirmed

---

### Step 2: Create the directory and files

#### Condition

- Step 1 complete

#### Process

1. Create the tasks directory
2. Create `{tasks_dir}/index.yaml`:

```yaml
prs: []
```

3. Create `{tasks_dir}/qa.md`:

```markdown
# QA — Open Questions

## In Progress

<!-- Record unresolved design and implementation questions here -->
```

4. Create `{tasks_dir}/qa_history.md`:

```markdown
# QA History — Resolved

<!-- Move resolved items here from qa.md -->
```

→ Proceed to Step 3

#### Output

- `{tasks_dir}/index.yaml` created
- `{tasks_dir}/qa.md` created
- `{tasks_dir}/qa_history.md` created

---

### Step 3: Verify and report

#### Process

1. Confirm all files exist
2. Report completion to the user

#### Notes

##### Checklist

- [ ] `{tasks_dir}/index.yaml` — exists
- [ ] `{tasks_dir}/qa.md` — exists
- [ ] `{tasks_dir}/qa_history.md` — exists
