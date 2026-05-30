# Jinja2 Template Authoring — Known Pitfalls with trim_blocks and lstrip_blocks

Japanese mirror: `references/hook/jinja2/authoring.jp.md`

The injection hook renders `.j2` templates with both `trim_blocks=True` and `lstrip_blocks=True`
enabled. These settings eliminate boilerplate whitespace in the output, but they also introduce
subtle Markdown-rendering traps that are easy to stumble into.

---

## Engine settings (non-configurable)

```python
Environment(
    trim_blocks=True,    # strips the newline immediately after a closing block tag %}
    lstrip_blocks=True,  # strips leading whitespace on lines that contain only a block tag
)
```

Both are always on. Every pitfall below flows from these two settings.

---

## Pitfall 1 — Block tag directly above `---` produces a setext heading

### What happens

```jinja2
{% if optional %}
---          ← danger: this "---" attaches to the line above after trim_blocks removes the newline
```

`trim_blocks` removes the newline after `%}`, so the rendered output looks like:

```
[whatever the if-block produces]
---
```

If the if-block produces a non-empty line just before `---`, Markdown parsers interpret
`---` as a setext-heading underline for that line, corrupting the heading hierarchy.

### Fix — add a blank line after the block tag

```jinja2
{% if optional %}

---          ← safe: a blank line separates the block tag from the horizontal rule
```

---

## Pitfall 2 — `{{ expr }}` inside an ATX heading (`## …`)

### What happens

```jinja2
## {{ ref.path }} — {{ ref.description }}
```

Some Markdown renderers (including Claude Code's preview) convert the line into a heading, then
try to render the inline `{{ … }}` as a code span — producing broken output.

### Fix — append `<!-- -->`

```jinja2
## {{ ref.path }} — {{ ref.description }}<!-- -->
```

The empty HTML comment forces parsers to treat the line as a paragraph-level element rather than
a pure ATX heading, suppressing the setext / heading misinterpretation while leaving the rendered
text intact.

---

## Pitfall 3 — Block tag directly above content in a conditional block

### What happens

```jinja2
{% if not jp_mirror %}
> Warning text    ← rendered immediately after the if-tag line with no blank line
{% endif %}
```

With `trim_blocks`, the newline after `{% if not jp_mirror %}` is stripped, causing the
blockquote to appear with no leading blank line. This can confuse renderers that require a
blank line before block-level elements.

### Fix — blank line immediately after the opening tag

```jinja2
{% if not jp_mirror %}

> Warning text
{% endif %}
```

---

## Pitfall 4 — Indented block tags lose their indentation

### What happens

With `lstrip_blocks=True`, any line that starts only with whitespace followed by `{%` has
that leading whitespace stripped. An indented `{% for %}` loop intended to produce indented
output will not produce indented output.

### Fix — place the required indentation outside the block tag

If the output genuinely needs indentation, emit it as a literal string on the content lines, not
by indenting the block tag itself:

```jinja2
{% for item in items %}
    - {{ item }}     ← indentation here is on the content line, not the block tag
{% endfor %}
```

---

## Quick reference — Do / Don't

| Situation | Don't | Do |
|---|---|---|
| Horizontal rule after `if`/`for` block | `{% if x %}\n---` | `{% if x %}\n\n---` |
| `{{ expr }}` in ATX heading | `## {{ path }}` | `## {{ path }}<!-- -->` |
| Blank line required before block element | `{% if x %}\n> text` | `{% if x %}\n\n> text` |
| Indented output | indent the `{%` tag | indent the content lines |
