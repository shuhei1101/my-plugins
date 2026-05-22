# Incident: Skill Reading Other Skills Causes Token Bloat

**Date**: 2026-05-23
**PR**: PR68 (conversation-to-claude-improve)

## What Happened

`conversation-to-claude` had a Step 0 that read four creator skills (`skill-creator`, `rule-creator`, `hook-creator`, `claude-creator`) before making proposals. This was intended to give Claude accurate judgment criteria.

However, each Claude Code skill has a ~2500 token limit, so reading 4 skills consumed ~10,000 tokens on every invocation — before any actual work was done.

## Root Cause

The assumption was that Claude needed to read full skills to understand how to propose accurately. In reality, only a small subset of each skill (the "when to use" criteria) was needed.

## Fix

Removed Step 0 entirely. Extracted the essential judgment criteria from all creator skills and embedded them directly into `conversation-to-claude`'s own References section (`§ Artifact type knowledge`). The skill is now self-contained.

## Prevention Rule

**Never design a skill that reads other skills at startup.** If judgment criteria from another skill are needed, extract only the relevant decision rules and embed them inline. Skills should be self-contained.
