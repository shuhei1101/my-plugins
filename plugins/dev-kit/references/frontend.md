# Frontend — dev-kit Shared Reference

Frontend-shared conventions (HTML, CSS, JavaScript / TypeScript on the client side).

---

## Mandatory rules

### Always use the `frontend-design` skill when designing UI

For **any** frontend visual/UX work — components, pages, full applications, layout decisions,
typography, color choices, animations — invoke the `frontend-design` skill **without exception**.

The skill enforces:

- A clear conceptual / aesthetic direction (not generic AI defaults)
- Distinctive typography and color choices
- Intentional motion and spatial composition
- Production-grade implementation matched to the aesthetic vision

Do not write frontend UI code by ad-hoc taste — route every UI design decision through this skill,
even for small components, so the output stays cohesive and avoids "AI slop" aesthetics.

Skill ID: `frontend-design:frontend-design` (from the official Claude plugins marketplace).

---

> **TODO**: Additional frontend topics to be added in future PRs.
>
> Planned topics:
> - Frontend project structure conventions
> - Component design principles (composition, props, state boundaries)
> - Accessibility (a11y) baseline
> - Frontend testing approach
> - Build / bundler conventions
