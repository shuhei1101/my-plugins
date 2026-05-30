# Jinja2 Template Authoring — Markdown Output

Authoring rules for Jinja2 templates that **emit Markdown** (e.g. `hooks/templates/injection.md.j2`).
Most rendering bugs come from the interaction between Jinja2 whitespace stripping and Markdown
block-element spacing. The patterns below are the ones that have actually broken templates in
this repo — encode them as habits.

Japanese mirror: `references/hook/jinja2/templates.jp.md`

---

## Environment assumed by these rules

These rules assume the Jinja2 environment is configured as:

```python
Environment(
    trim_blocks=True,       # strip the first newline AFTER {% %}
    lstrip_blocks=True,     # strip leading whitespace BEFORE {% %}
    undefined=StrictUndefined,
    autoescape=False,
)
```

This is the configuration used by `claude-kit` / `dev-kit` injection hooks. If you author
templates for the same hook framework, you inherit this configuration — the rules apply.

`trim_blocks` is the source of nearly all of the bugs below. If you change it, the rules change.

---

## Rule 1 — `{% %}` block tags consume the next newline

With `trim_blocks=True`, the newline **immediately after** a `{% ... %}` tag is stripped.
That means writing one blank line after `{% endif %}` produces **zero** blank lines in the output.

### Anti-pattern

```jinja
{% if note %}
> {{ note }}
{% endif %}
## Next heading
```

Renders to:

```markdown
> note text
## Next heading
```

The blockquote and the `##` heading collide on adjacent lines. Most Markdown renderers will still
parse the heading, but visual spacing is broken and some renderers will fold them together.

### Fix — put the blank line INSIDE the block

```jinja
{% if note %}
> {{ note }}

{% endif %}
## Next heading
```

The blank line is part of the block's content, so it survives. After `trim_blocks` eats the newline
after `{% endif %}`, you are left with exactly one blank line separating the blockquote and the
heading — which is what Markdown needs.

**Rule of thumb**: any Markdown block element that needs a blank line around it (heading, list,
blockquote, code fence, table) must have that blank line **inside** the enclosing Jinja2 block,
not after `{% endif %}` / `{% endfor %}`.

---

## Rule 2 — Consecutive block tags drop ALL the newlines between them

`{% endfor %}{% endif %}{% if other %}` (one tag per line) chains through `trim_blocks` and the
intermediate blank lines vanish. If the next visible character is `---`, it binds to the
**last line of the previous content** and becomes a setext-style level-2 heading.

### Anti-pattern

```jinja
{% if required %}
{% for ref in required %}
- {{ ref.name }}
{% endfor %}
{% endif %}
{% if optional %}
---

## Optional references
```

Renders to:

```markdown
- last_ref_name
---

## Optional references
```

`last_ref_name\n---` is a Markdown **setext heading** (the dashes underline the previous line).
The last bullet of the list silently becomes a heading and the `---` separator disappears from
the output.

### Fix — put the leading blank line INSIDE the optional block

```jinja
{% if required %}
{% for ref in required %}
- {{ ref.name }}
{% endfor %}
{% endif %}
{% if optional %}

---

## Optional references
```

The blank line at the top of the `{% if optional %}` body survives `trim_blocks`, so the output
has `blank line + ---` and Markdown sees an `<hr>` instead of a heading underline.

**Rule of thumb**: when `{% endif %}{% if X %}` is followed by `---`, the blank line BEFORE `---`
must be inside the inner `{% if X %}` block.

---

## Rule 3 — `}}` in a heading confuses Handlebars-style parsers

A line like

```jinja
## {{ ref.path }} — {{ ref.description }}
```

renders to clean Markdown, but the literal `}}` at the end of the heading can be misread by
**downstream tooling** that uses Handlebars / Mustache / Jinja2-like syntax (IDE previews, chat
clients, doc generators). Some of those tools chew the rest of the buffer trying to find a matching
`{{`, and the following content silently disappears.

### Fix — terminate the line with `<!-- -->`

```jinja
## {{ ref.path }} — {{ ref.description }}<!-- -->
```

The HTML comment is invisible in rendered Markdown but breaks the `}}` from whatever literal text
follows, so Handlebars-style parsers stop scanning at the comment.

**Apply this to any heading or paragraph line that ENDS with a Jinja2 expression** (`}}`).
Lines where `}}` is followed by literal text (e.g. `{{ name }} — description`) are safe because
the literal text already breaks the parse chain.

---

## General authoring guidance

1. **End every template with a single trailing newline.** Files without a final newline cause the
   last block to merge into whatever the renderer appends next.
2. **Prefer Markdown's normal blank-line rhythm over `{%- ... -%}`.** The leading/trailing-dash
   variants give you fine control over whitespace stripping, but they compose badly with
   `trim_blocks` / `lstrip_blocks` and produce templates that are hard to reason about.
   Reserve them for the rare case where standard formatting cannot achieve the required spacing.
3. **Test the rendered output, not just the template syntax.** A template that parses cleanly can
   still produce unparseable Markdown. Render with a representative payload and view it as
   Markdown — preferably in the same renderer the consumer uses.
4. **Keep one Jinja2 control tag per line.** Stacking `{% endif %}{% endfor %}` on a single line
   makes Rule 2 harder to spot and produces unpredictable whitespace.

---

## Quick checklist

When you edit a `.md.j2` template, walk through:

- [ ] Every `{% endif %}` / `{% endfor %}` that precedes a Markdown block element — is the
      required blank line **inside** the block?
- [ ] Every `{% endif %}{% if X %}` chain where `---` follows — is the blank line **inside** the
      inner `{% if X %}`?
- [ ] Every heading or paragraph line ending in `}}` — does it end with `<!-- -->`?
- [ ] Does the file end with exactly one trailing newline?
- [ ] Did you render the template with a representative payload and view the output?
