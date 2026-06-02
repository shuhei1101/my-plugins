# Glossary

Project-specific terms for this marketplace repo. Always loaded, so the bar is high — only
terms that are current, non-obvious from their name, and recur.

Japanese mirror: `.claude/rules/glossary.jp.md`

> Authoring bar and format: `plugins/work/references/conversation/グロッサリー.md`.

---

## Rules system

| Term | Description |
|---|---|
| incidents | The always-loaded recurrence-prevention log of process mistakes. Two layers: an index (`.claude/rules/incidents.md`) of one-line summaries and detail files (`.claude/references/incidents/{slug}.md` + `.jp.md`). Records operation/judgment errors only — never code bugs. |
| glossary | The always-loaded project terminology file (`.claude/rules/glossary.md`). Kept concise because every entry costs context on every session. |
| JP ミラー (jp-mirror) | A `.jp.md` companion to a `.md` file (or `.jp.yaml` to `.yaml`). The English file is the source of truth and always-loaded; the JP mirror is human-reference only and is **not** auto-loaded. Convention: edit the source, then sync the mirror; place any warning comment after the closing `---` of YAML frontmatter, never before the opening one. |

## Plugin mechanism

| Term | Description |
|---|---|
| ref-inject | The reference auto-injection mechanism (the `ref-inject` plugin and the `*-kit` hooks it seeds). On a matching Write/Edit/Read, the hook injects `required` references **full-body** and `optional` ones as **path + description only**, throttled by a per-session two-tier TTL token (`patterns` + `references` namespaces) so the same body is not re-injected until the TTL elapses. |
