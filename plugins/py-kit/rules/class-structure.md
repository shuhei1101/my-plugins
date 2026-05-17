---
description: >
  Template for the class-structure rule. Deploy to .claude/rules/class-structure.md in the project.
  Triggers when abstract classes, Protocols, or their concrete implementations are modified,
  and prompts a check for ripple effects across the class hierarchy.
---

# py-kit rule template: class-structure
# Copy to: {project}/.claude/rules/class-structure.md
# Adjust the paths: section to match your project's source layout.

---
paths:
  - "src/**/domain/**/*.py"
  - "src/**/infrastructure/**/*.py"
  - "src/**/*able.py"
  - "src/**/i_*.py"
  - "src/**/base_*.py"
---

# Class Structure Linkage

When any file matching this rule's paths is modified:

## Check before committing

1. **Identify the class role** — is the changed file a Protocol, ABC, or concrete implementation?

2. **If a Protocol or ABC changed:**
   - List all classes that implement or inherit from it
   - For each: verify the class still satisfies the contract (method signatures, return types, raised exceptions)
   - For each: check if behavior assumptions in callers remain valid

3. **If a concrete implementation changed:**
   - Check the parent Protocol / ABC — does the change violate the Liskov Substitution Principle?
   - Check sibling implementations — do they need a parallel change?

4. **If a method signature changed:**
   - Search for all call sites (`Grep` for the method name across `src/` and `tests/`)
   - Update call sites and type annotations

## Pattern

```
Protocol / ABC (domain/repositories/ or domain/services/)
    └── ConcreteA (infrastructure/)
    └── ConcreteB (infrastructure/)
```

When any node in this tree changes, verify the whole tree.
