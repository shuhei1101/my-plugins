# Markdown Table Conventions

Japanese mirror: `references/markdown/markdown-table.jp.md`

---

## Number column

Always add a `#` column as the **leftmost column** of every table.
The `#` column is **always filled** — every row has a sequential number, no exceptions.

**Example:**

| # | File | Changes |
|---|---|---|
| 1 | `foo.md` | Added section A |
| 2 |  | Fixed typo in section B |
| 3 | `bar.md` | Removed deprecated note |

**Anti-pattern — omitting the number column:**

| File | Changes |
|---|---|
| `foo.md` | Added section A |
| `bar.md` | Removed deprecated note |

The `#` column makes rows easy to reference in conversation ("row 3") and helps orient readers in long tables.

---

## Repeated cell values

When consecutive rows share the same value in a column, write the value **only in the first row** and leave the cell blank in subsequent rows.

**Example:**

| # | File | Changes |
|---|---|---|
| 1 | `foo.md` | Added section A |
| 2 |  | Fixed typo in section B |
| 3 | `bar.md` | Removed deprecated note |

**Anti-pattern — do not repeat:**

| # | File | Changes |
|---|---|---|
| 1 | `foo.md` | Added section A |
| 2 | `foo.md` | Fixed typo in section B |
| 3 | `bar.md` | Removed deprecated note |

Apply this rule to any column whose value spans multiple rows: file names, component names, categories, etc.
The `#` column is exempt — it always has a sequential number.
