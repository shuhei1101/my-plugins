# ref-inject over-built a generator script and a PreCompact hook

## What happened

While building the `ref-inject` plugin (PR156), AI added two mechanisms the user then removed:

1. A deterministic `scripts/generate.py` that copied templates, substituted placeholders, and
   registered the plugin in `marketplace.json`. The user removed it — they wanted Claude to
   **read the templates and write the files itself**, because that keeps the generation in
   conversation context and is adaptable per plugin.
2. A `PreCompact` hook (`refresh_on_compact.py`) that deleted the session token after `/compact`
   so references would re-inject immediately. The user removed it because the **TTL token
   already re-injects** once it expires, so a dedicated compact hook was wasted overhead.

## Why it matters

Both were extra machinery for behavior the simpler existing path already covered (Claude-driven
copy; TTL expiry). Each added a file to maintain for no net benefit.

## Lesson

- For per-plugin / per-file generation in this repo, prefer **Claude-driven copy + substitute**
  over a deterministic script — the work stays in context and stays adaptable.
- Do **not** add a dedicated hook for behavior an existing mechanism (here, the TTL token)
  already provides.
- Default to the leanest mechanism; add infrastructure only when the simple path demonstrably
  falls short.

## Related

- PR156: ref-inject created; generate.py and refresh_on_compact.py both added then removed
- Related theme: [[premature-cross-plugin-centralization]], [[session-kit-removed-after-premise-change]]
