# Markdown chosen for code-consumed config (PR140)

## What happened

While reorganizing `plugins/py-kit/references/index.yaml`, AI converted it to `index.md` / `index.jp.md` (Markdown tables) on the grounds that "users browse it directly, Markdown is more readable". The Python hook `inject_references.py` had to be rewritten with a regex Markdown-table parser to extract `path → description`.

User caught it on review: **"これ YAML にしとかなあかんでしょ / なんでマークダウンにした / Python の処理でさ注入できんやん"**. AI had to revert: `index.yaml` (English description) + `index.jp.yaml` (Japanese mirror) was restored, the regex parser was deleted, and `yaml.safe_load` direct iteration was restored.

## Root cause

The conversion conflated two needs:

- **Human browsing** of a reference list — Markdown tables look nicer
- **Machine parsing** by a hook to look up descriptions — YAML is reliable, Markdown is fragile

When a single file serves both, **YAML wins** because:

- `yaml.safe_load` is one line; regex over Markdown table rows is brittle (separator rows, escaped pipes, multi-line cells)
- YAML supports comments naturally; Markdown can't
- Humans reading YAML still get the path / description pairing clearly

Markdown is for **prose with formatting**, not for **structured data with hover-over reads**.

## Lesson

**If a file is parsed by code, keep it in a structured format (YAML / JSON / TOML).** Convert to Markdown only when the *sole* consumer is a human reader.

When the desire to "use Markdown for human readability" arises but the file is also code-consumed:

1. Keep the data in YAML
2. If a Markdown view is genuinely needed, generate it from the YAML (don't hand-maintain Markdown as the source of truth)
3. The original YAML stays as the single source of truth

## Related

- Reverted in PR140 (commit bfe3f74)
- Same principle applies to `injection_rules.yaml`, `prompts/index.yaml`, any catalog the hook reads
