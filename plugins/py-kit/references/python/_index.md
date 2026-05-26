# py-kit Python References — Index

This directory contains Python standards references for py-kit skills.
Skills read this index first, then select specific files based on what the task requires.

---

## Files

| File | Contents | When to read |
|---|---|---|
| `python-core.md` | Naming conventions, comment rules, type hints, language rules | Every Python task — baseline standards |
| `python-architecture.md` | SOLID, DRY, layered architecture, DI, no hardcoding, Pydantic, project folder structure | Full projects, architecture review, refactoring |
| `python-scripts.md` | Simple script structure, bat launcher templates, FastAPI run.bat, tkinter GUI | Script writing, bat file creation, simple automation |
| `python-testing.md` | Logger specification, test policy | Adding tests, setting up logging, new project scaffold |
| `python-fastapi.md` | FastAPI endpoint design, dependency injection patterns, common middleware | FastAPI projects |
| `python-llm.md` | LLM client architecture, prompt management, token handling | Projects that call LLM APIs |

---

## Usage Guide

**py-script** (simple scripts): Read `python-core.md` and `python-scripts.md`

**py-project new**: Read `python-core.md`, `python-architecture.md`, `python-testing.md`; add `python-fastapi.md` if FastAPI

**py-project existing**: Read `python-core.md`, `python-architecture.md`; add others as needed for the specific task

**FastAPI task**: Read `python-core.md`, `python-architecture.md`, `python-fastapi.md`

**LLM task**: Read `python-core.md`, `python-llm.md`
