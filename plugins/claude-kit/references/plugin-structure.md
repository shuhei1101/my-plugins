# Plugin Structure Reference

## Standard Directory Layout

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md         # Skill definition (English, auto-loaded)
│       └── SKILL.jp.md      # Japanese translation (reference only)
├── agents/
│   └── <agent-name>.md      # Agent definitions (optional)
├── hooks/
│   └── hooks.json           # Hook configuration (optional)
├── references/              # Shared reference docs (optional)
│   └── <topic>.md
├── .mcp.json                # MCP server config (optional)
└── changelogs/              # Version history (required by plugin-kit)
    ├── v1.0.0.md            # Initial release
    └── v1.1.0.md            # Subsequent versions
```

## plugin.json Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Plugin identifier (kebab-case). Used as skill namespace. |
| `description` | Yes | Plugin description |
| `version` | Yes | Semantic versioning (e.g. `1.0.0`) |
| `author` | No | Author info |

## marketplace.json Entry

Add to `.claude-plugin/marketplace.json` → `plugins` array:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

## Version Bump Rules

| Change type | Bump |
|---|---|
| Bug fix / minor correction | PATCH (`1.x.y` → `1.x.y+1`) |
| New skill or behavior change | MINOR (`1.x.0` → `1.x+1.0`) |
| Complete redesign | MAJOR (`1.0.0` → `2.0.0`) |

## Changelog File Format

File: `changelogs/v{X.Y.Z}.md`

```markdown
# v{X.Y.Z} — {YYYY-MM-DD}

## 変更内容

- {変更点}

## 構造の変更

{ディレクトリ構造や設定ファイルの変更があれば記載。なければ省略。}
```

The "構造の変更" section is critical — it lets other projects that depend on this plugin know what structural updates they need to apply.
