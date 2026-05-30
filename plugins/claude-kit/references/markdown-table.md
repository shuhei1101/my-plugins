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

---

## Number column

Always add a `#` column as the **leftmost column** of every table.

**Example:**

| # | File | Changes |
|---|---|---|
| 1 | `foo.md` | Added section A |
|  |  | Fixed typo in section B |
| 2 | `bar.md` | Removed deprecated note |

**Anti-pattern — omitting the number column:**

| File | Changes |
|---|---|
| `foo.md` | Added section A |
| `bar.md` | Removed deprecated note |

The `#` column makes rows easy to reference in conversation ("row 3") and helps orient readers in long tables.
