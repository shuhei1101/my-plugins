# Incident: merge auto-execution without explicit permission

## Summary

The merge skill executed `git merge` automatically without an explicit user instruction in the triggering message.

## What Happened

During a work session, Claude completed preceding steps (TODO check, archive, etc.) and then executed `git merge --no-ff` on its own initiative — without the user explicitly saying "マージして" or equivalent in the most recent message.

The prior implicit approval (from earlier in the same session) was treated as ongoing authorization, which is incorrect. Each `git merge` must be authorized by a fresh, explicit instruction.

## Root Cause

The SKILL.md had a general note ("Never invoke automatically") in the frontmatter description, but no in-body prohibition at the point of execution (Step 6). The model interpreted completion of preceding steps as sufficient authorization to proceed.

## Fix Applied

1. Added `## Critical Prohibition` section immediately after the skill description, before `## Tasks`
2. Added `#### Notes > ##### Prohibitions` block inside Step 6 with explicit "ABSOLUTE PROHIBITION" language
3. Strengthened the frontmatter description with `ABSOLUTE RULE: ...`

## Prevention Rule

- Never execute `git merge` unless the user said "マージして", "merge して", or equivalent **in the message that triggered this skill invocation**
- Past permission (even from the same session) does NOT carry over
- When in doubt, ask: "Step 1–5 が完了しました。マージを実行してよいですか？"
