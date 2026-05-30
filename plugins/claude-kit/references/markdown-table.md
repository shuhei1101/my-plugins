# Markdown Table Conventions

Japanese mirror: `references/markdown-table.jp.md`

---

## Repeated cell values

When consecutive rows share the same value in a column, write the value **only in the first row** and leave the cell blank in subsequent rows.

**Example — file + change summary:**

| File | Changes |
|---|---|
| `foo.md` | Added section A |
|  | Fixed typo in section B |
| `bar.md` | Removed deprecated note |

**Anti-pattern — do not repeat:**

| File | Changes |
|---|---|
| `foo.md` | Added section A |
| `foo.md` | Fixed typo in section B |

Apply this rule to any column whose value spans multiple rows: file names, component names, categories, etc.
