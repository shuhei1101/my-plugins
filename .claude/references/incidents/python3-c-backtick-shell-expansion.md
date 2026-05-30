# python3 -c Backtick Shell Expansion

**Date**: 2026-05-30
**Category**: command-error

## What Happened

When passing Python code to `python3 -c "..."` via a Bash command that contained backtick-quoted strings (e.g., Markdown code spans like `` `plugins/work/` ``), Bash treated the backticks as command substitutions and expanded them, corrupting the Python string content:

```bash
python3 -c "
content = '''
| `plugins/work/` | 編集 | ...
'''
"
```

The backtick content was shell-expanded (attempted as a command), and the resulting variables were empty strings, leaving the file with blank cells in the table.

## How to Avoid

Use a single-quoted heredoc delimiter (`PYEOF`) so Bash does not expand anything inside the heredoc body:

```bash
python3 << 'PYEOF'
content = """
| `plugins/work/` | 編集 | ...
"""
PYEOF
```

With `<< 'PYEOF'` (single-quoted), Bash treats the entire block as a literal string — no variable expansion, no command substitution, no backslash processing.

## Context

This issue occurs when Python code contains backtick characters (common in Markdown table content). The `python3 -c "..."` form passes the code through Bash string parsing, which interprets backticks as command substitutions even inside double quotes. The heredoc form with a quoted delimiter bypasses this entirely.
