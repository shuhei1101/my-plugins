# AskUserQuestion Usage Guide

When and how to call the `AskUserQuestion` tool from within skills.

Japanese mirror: `references/common/askuserquestion.jp.md`

---

## When to use

Only call `AskUserQuestion` when a skill definition or the user **explicitly instructs** its use.

For all other mid-task questions or confirmation prompts, write the question as **plain text and
end the turn** — do not call `AskUserQuestion`.

**Why**: `AskUserQuestion` does not trigger the Stop hook. Calling it outside a skill bypasses
the stop-hook notification system.

---

## Question count

| Item | Constraint |
|---|---|
| Minimum | 1 question |
| Maximum | 4 questions per call |

---

## Options constraints

| Item | Constraint |
|---|---|
| Minimum | 2 options |
| Maximum | 4 options |
| "Other" | Appended automatically by the UI — never add it manually |

---

## Fields

### `question`

The complete question, ending with a question mark.

### `header`

Short label displayed as a chip/tag. **Max 12 characters.** Examples: `"Auth method"`, `"Library"`, `"Approach"`.

### `options[].label`

Display text the user sees and selects (1–5 words). If recommending a specific option, put it
first and append `"(Recommended)"` to the label.

### `options[].description`

Explains the option — trade-offs, implications, or what happens if chosen.

### `multiSelect`

When `true`: the user can select multiple options. Use when choices are **not mutually exclusive**.
Phrase the question accordingly (e.g. "Which features do you want to enable?").

**Constraint**: `preview` is only supported for single-select questions (`multiSelect: false`).

---

## Preview field

Use `options[].preview` for visual comparisons: ASCII mockups, code snippets, diagram
variations, or configuration examples. Do **not** use for simple preference questions where
labels and descriptions suffice.

```yaml
options:
  - label: "Class structure"
    description: "Better for stateful processing."
    preview: |
      ```python
      class Processor:
          def __init__(self, cfg):
              self.cfg = cfg

          def run(self):
              ...
      ```
  - label: "Function structure"
    description: "Better for simple pipelines."
    preview: |
      ```python
      def process(cfg):
          ...
      ```
```

When any option has a `preview`, the UI switches to a side-by-side layout (option list on the
left, preview on the right). Content is rendered as Markdown in a monospace box; multi-line text
with newlines is supported.

---

## Anti-patterns

| # | Anti-pattern | Correct approach |
|---|---|---|
| 1 | More than 4 options | Split into multiple questions or use a numbered list in plain text |
| 2 | Adding "Other" manually | Omit — the UI appends it automatically |
| 3 | Using `preview` with `multiSelect: true` | Only use `preview` with single-select questions |
| 4 | Calling `AskUserQuestion` outside a skill | Write the question as plain text and end the turn |
