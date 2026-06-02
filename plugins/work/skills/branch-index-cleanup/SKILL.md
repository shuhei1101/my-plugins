---
name: work:branch-index-cleanup
description: |
  Audit git branches against index.yaml / index.archive.yaml and clean up unregistered ones.
  Classifies each unregistered branch as A (delete), B (archive + delete), or C (keep, add to index).
  Trigger when the user says "ブランチを整理して", "未登録ブランチを片付けて", "branch-index-cleanup して",
  or invoked explicitly as `/work:branch-index-cleanup`.
disable-model-invocation: true
---

# work:branch-index-cleanup — Audit & Clean Up Unregistered Branches

Compares local git branches with `index.yaml` / `index.archive.yaml` and interactively classifies
each unregistered branch. Then executes delete / archive / index-add per classification.

---

## Tasks

### Step 1: Collect unregistered branches

#### Condition

- Always — run first

#### Process

1. Get all local branches:

```bash
git branch --format='%(refname:short)'
```

2. Read registered branch identifiers from both index files (each entry has either an `id` and/or a
   `title` matching `{type}/{title}`):

```bash
python -c "
import yaml
branches = set()
for path in ['.work/tasks/index.yaml', '.work/tasks/index.archive.yaml']:
    try:
        data = yaml.safe_load(open(path))
        for entry in (data.get('branches') or []):
            if entry.get('branch'): branches.add(str(entry['branch']))
    except: pass
print('BRANCHES:', ' '.join(sorted(branches)))
"
```

3. For each branch (excluding `master` / `main`), check whether it is registered:
   - **New format**: branch is `{type}/{title}` → match against `titles`
   - **Legacy format**: branch is `PR{N}/{type}/{title}` → extract `{N}` and match against `ids`
   - Branches that match neither are treated as unregistered
4. Build the list of **unregistered branches**

→ Proceed to Step 2

#### Output

- List of unregistered branch names

---

### Step 2: Classify each branch

#### Condition

- Step 1 complete — at least one unregistered branch found

#### Process

1. Display the unregistered branch list in a table:

   | Branch | Inferred ID | Inferred Title | Classification |
   |---|---|---|---|
   | feat/some-feature | (none) | feat/some-feature | ? |
   | PR42/feat/legacy   | 42     | feat/legacy        | ? |
   | ... | | | |

2. For each branch, auto-infer:
   - `id` — only present when the branch name carries a legacy `PR{N}/` prefix
   - `title` — full branch name (new format) or the `{type}/{title}` portion (legacy format)
   - `type` — type portion (feat/fix/refactor/docs/chore/test), default `chore` if absent

3. Ask the user to assign A / B / C to each branch:

   > 各ブランチを以下のいずれかに分類してください:
   > - **A** — 完了済み・不要（削除のみ）
   > - **B** — 完了済み・記録したい（archive に追記 → 削除）
   > - **C** — 作業継続（index.yaml に追記）

4. If the user wants to modify inferred metadata for B/C branches, accept corrections before proceeding

→ Proceed to Step 3

#### Output

- Classification map: `{ branch: { class: A|B|C, id, title, type, summary? } }`

---

### Step 3: Execute per classification

#### Condition

- Step 2 complete — user has confirmed all classifications

#### Process

Execute in order: B → C → A

**Class B — archive + delete**:

For each B branch:
1. Append entry to `.work/tasks/index.archive.yaml`:

```bash
python -c "
import yaml, sys
path = '.work/tasks/index.archive.yaml'
try:
    data = yaml.safe_load(open(path)) or {}
except: data = {}
branches = data.get('branches') or []
branches.append({
    'branch': sys.argv[1],
    'title': sys.argv[2],
    'type': sys.argv[3],
    'summary': sys.argv[4] if sys.argv[4] else '',
    'task': sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] else '',
    'completed': True,
})
data['branches'] = branches
yaml.dump(data, open(path, 'w'), allow_unicode=True, default_flow_style=False)
" {branch} {title} {type} "{summary}" {task_dir}
```

2. Delete the branch:

```bash
git branch -d {branch}   # use -D if not merged
```

**Class C — add to index.yaml**:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
  --branch "{branch}" \
  --title "{title}" \
  --type {type} \
  --summary "{summary}" \
  --task "{task_dir}"
```

**Class A — delete only**:

```bash
git branch -d {branch}   # use -D if not merged
```

→ Proceed to Step 4

#### Notes

- If `git branch -d` fails (not fully merged), warn the user and ask whether to force-delete (`-D`)
- `${CLAUDE_PLUGIN_ROOT}` is the shell variable pointing to the plugin root path

---

### Step 4: Report results

#### Condition

- Step 3 complete

#### Process

Print a summary table:

| 分類 | 件数 | ブランチ |
|---|---|---|
| A（削除） | N | branch1, branch2 |
| B（archive → 削除） | N | branch3 |
| C（index 追記） | N | branch4 |

Confirm the final state:

```bash
git branch --format='%(refname:short)' | grep -v master | grep -v main
```

→ Done.

---

### Step 5: Nothing to do (all branches registered)

#### Condition

- Step 1 found zero unregistered branches

#### Process

Report:

> すべてのブランチが index.yaml / index.archive.yaml に登録済みです。整理は不要です。
