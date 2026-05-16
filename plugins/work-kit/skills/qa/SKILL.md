---
name: qa
description: |
  Rules for recording and closing QA entries in .work/QA.md.
  Trigger when an unresolved question arises during spec or TODO writing,
  or when the user says "QAに書いて", "QAエントリ追加", "QAをクローズして".
allowed-tools: Read Write
---

# work-kit:qa — QA Entry Rules

Defines how to record unresolved questions in `.work/QA.md` and close them once decided.
Never leave `TBD` or `要検討` in spec documents — record everything here instead.

---

## Tasks

### Step 1: Add a QA entry

#### Condition

- An unresolved question arises while writing a spec or TODO.md
- About to write `TBD` or `要検討` in a spec (don't — record here instead)

#### Process

1. Append to the `## 進行中` section of `.work/QA.md`:

```markdown
### {YYYY-MM-DD} {question title}

**Background**: {why this decision is needed}

| Option | Description |
|---|---|
| A | {option A} |
| B | {option B} |

**Recommended**: {A or B + 1–2 line reasoning}

**Apply decision to**: {relevant specs/ document}
```

2. In the spec body, write only "under review in QA.md" — put details in the QA entry

→ Done (to close a QA entry, proceed to Step 2)

#### Notes

##### Prohibitions

- Never omit the recommended approach ("decide later" or "user's call" is not allowed)
- Never leave TBD / 要検討 markers in spec documents

---

### Step 2: Close a QA entry

#### Condition

- The user has made a decision on an open question

#### Process

1. Reflect the decision in the document listed under `**Apply decision to**`
2. Remove the entry completely from `## 進行中` in `.work/QA.md`
3. Append a summary to `## 解決済み`:

```markdown
### {YYYY-MM-DD} {question title} → {decision in one line}
```

4. Update any TODO.md files that referenced this QA entry

#### Notes

##### Prohibitions

- Do not update `## 解決済み` before reflecting the decision in the spec
- Do not leave the entry in `## 進行中` after moving it to `## 解決済み`
