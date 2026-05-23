---
name: plugin-creator
description: |
  Create a new Claude Code plugin with proper versioning (changelogs/ folder).
  Trigger when the user says "新しいプラグインを作りたい", "プラグインを作って", "create a plugin", "make a new plugin", or "plugin-creator して".
---

# plugin-creator — New Plugin Scaffold

Creates a plugin with the standard directory structure, including the `changelogs/` versioning folder.

---

## References

- Plugin structure and version rules: `references/plugin-structure.md` in this plugin
- Official plugin docs: https://code.claude.com/docs/ja/plugins

---

## Tasks

### Step 1: Gather plugin information

#### Condition

- Always — run first

#### Process

Ask the user for:

1. **Plugin name** — kebab-case (e.g. `code-reviewer`, `my-tool`)
2. **Description** — one-line summary of what the plugin does
3. **Skills to include** — name and purpose of each skill (at least one)
4. **Other components** — agents, hooks, MCP servers? (optional)

#### Output

- Plugin name, description, skill list, component list confirmed

---

### Step 2: Generate directory structure

#### Condition

- Step 1 complete

#### Process

1. Read `references/plugin-structure.md` in this plugin for the canonical layout
2. Create the following (adjust for components chosen in Step 1):

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
└── changelogs/
    └── v1.0.0.md
```

3. If agents / hooks / MCP were requested, create those dirs and stub files too

#### Output

- Directory structure created under `plugins/<plugin-name>/`

---

### Step 3: Write plugin.json

#### Condition

- Step 2 complete

#### Process

Create `plugins/<plugin-name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

#### Output

- `plugin.json` written

---

### Step 4: Write SKILL.md for each skill

#### Condition

- Step 3 complete

#### Process

For each skill from Step 1, create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.

Use the step-based structure:
- Frontmatter: `name`, `description` (auto-trigger conditions)
- Sections: Overview → Tasks (each task: Condition / Process / Output)

Keep it concise — each step should be actionable without reading other files.

#### Output

- `SKILL.md` created for each skill

---

### Step 5: Write initial changelog

#### Condition

- Step 4 complete

#### Process

Create `plugins/<plugin-name>/changelogs/v1.0.0.md`:

```markdown
# v1.0.0 — {YYYY-MM-DD}

## 変更内容

- 初回リリース
- {追加したスキル名} スキルを追加

## 構造の変更

初回リリースのため、ディレクトリ構造全体が新規作成。

```
plugins/<plugin-name>/
├── .claude-plugin/plugin.json
├── skills/<skill-name>/SKILL.md
└── changelogs/v1.0.0.md
```
```

#### Notes

The "構造の変更" section is the most important part of the changelog.
When this plugin's structure changes in the future, other projects that depend on it can read this section to understand what they need to update on their end.

#### Output

- `changelogs/v1.0.0.md` written

---

### Step 6: Register in marketplace.json

#### Condition

- Step 5 complete

#### Process

1. Read `.claude-plugin/marketplace.json` in the repository root
2. Add a new entry to the `plugins` array:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

3. Save the file

#### Output

- `.claude-plugin/marketplace.json` updated

---

### Step 7: Report and next steps

#### Process

Report what was created:

- Directory structure summary
- File list with paths
- How to test locally:

```bash
# ローカルテスト
claude --plugin-dir ./plugins/<plugin-name>
/<skill-name>
```

- Remind the user to bump `plugin.json` and add a new `changelogs/v{X.Y.Z}.md` whenever the plugin is updated in the future
