# py-kit References — Index

This file is the entry point for all py-kit Python references. py-kit skills
(`py-kit:py-script`, `py-kit:py-project`) read this first in Step 1, then load
the specific reference files that match the task.

Place this file inside `plugins/py-kit/references/` so that any read under that
directory carries the index into the conversation context.

---

## When to Read What

Pick the references that match the task. Always start with `python-core.md`.

| Task | Read |
|---|---|
| Any Python work (baseline — always required) | `python-core.md` |
| Designing or scaffolding a project / refactoring / quality review | `python-architecture.md` |
| Writing a simple single-file script (no `pyproject.toml`, no tests) | `python-core.md` + `python-scripts.md` |
| Generating bat launchers / FastAPI run.bat / tkinter GUI | `python-scripts.md` |
| Setting up `logger.py` / pytest skeleton / mocks | `python-testing.md` |
| Implementing FastAPI endpoints / routers / middleware | `python-fastapi.md` |
| Wrapping an LLM API (Claude / OpenAI) / Instructor / prompt files | `python-llm.md` |

---

## Quick "I'm building..." Map

| Building... | Read in order |
|---|---|
| A one-off Python script | `python-core.md` → `python-scripts.md` |
| A new layered project (no FastAPI, no LLM) | `python-core.md` → `python-architecture.md` → `python-testing.md` |
| A new FastAPI service | `python-core.md` → `python-architecture.md` → `python-fastapi.md` → `python-testing.md` |
| A new LLM-powered service | `python-core.md` → `python-architecture.md` → `python-llm.md` → `python-testing.md` |
| Reviewing an existing project | `python-core.md` → `python-architecture.md` → (specific file based on what changed) |

---

## File List

| File | One-liner |
|---|---|
| `python-core.md` | Naming, comment rules, type hints, language rules — the always-required baseline |
| `python-architecture.md` | SOLID, DRY, design patterns (Strategy / Template Method / Factory / Decorator), DI, Pydantic boundaries, layered architecture, project folder structure (pure DDD) |
| `python-scripts.md` | Single-file script structure, argparse patterns, bat launcher templates (Windows), FastAPI run.bat, tkinter GUI |
| `python-testing.md` | Logger specification, test policy, pytest conventions, mock organization |
| `python-fastapi.md` | DDD-aligned project layout, router patterns, dependency injection, middleware, lifespan |
| `python-llm.md` | LLM client Protocol abstraction, provider pattern, task-specific LLMs, structured output (Pydantic + Instructor), prompt files, token / cost management, error handling |

Each file has a JP mirror (`*.jp.md`) with the same structure.

---

## Reading Protocol for Skills

1. Read this `CLAUDE.md` first — identify which references apply
2. Read **all applicable** reference files **in full** before generating code
3. Do not skim sections — every section has rules that apply to the kind of code being written
4. If a rule conflicts with the user's explicit instruction, ask before deviating
