# llm/prompts-loader — Prompt loader implementation

Implementation conventions for reading `prompts/index.yaml`, rendering the part files with Jinja2, and assembling them into a single prompt.
For **how to write** prompts, see `llm/prompts-authoring.md`.

---

## Placement

```
src/{pkg}/integrations/llm/prompts/
├── __init__.py
├── index_loader.py       # prompts/index.yaml の読み込みとキャッシュ
├── builder.py            # 部品結合 + Jinja2 レンダリング
└── types.py              # PromptPart / PromptSpec 等の DTO
```

Place the loader **under `src/`** (project code), and place the prompt body (`prompts/`) directly under the project root.

---

## Resolving the project root

The loader needs to know where the `prompts/` folder is.
Use `PROJECT_ROOT` from `shared/constants.py`:

```python
# src/{pkg}/integrations/llm/prompts/index_loader.py
from __future__ import annotations
from pathlib import Path
from {pkg}.shared.constants import PROJECT_ROOT

PROMPTS_DIR: Path = PROJECT_ROOT / "prompts"
```

---

## index_loader.py — reading index.yaml

```python
from __future__ import annotations
import yaml
from functools import cache
from pathlib import Path
from typing import TypedDict, Literal


class PartMeta(TypedDict, total=False):
    path: str
    kind: Literal["static", "dynamic"]
    role: Literal["system", "user", "assistant"]
    category: str
    group: str
    lang: str
    mirror_of: str


class LlmSpec(TypedDict):
    template_id: str
    includes: list[str]


class PromptIndex(TypedDict, total=False):
    parts: list[PartMeta]
    llms: dict[str, LlmSpec]
    display: dict[str, object]
    legacy_aliases: dict[str, dict[str, str]]


@cache
def load_index(prompts_dir: Path) -> PromptIndex:
    """prompts/index.yaml を 1 度だけ読んでキャッシュする。"""
    data = yaml.safe_load((prompts_dir / "index.yaml").read_text(encoding="utf-8"))
    return data or {}
```

Key points:
- Use `@cache` to read once per process (keeps startup I/O low)
- The return value is typed via `TypedDict` (treat as a dict)
- When you want hot-reload, just call `load_index.cache_clear()`

---

## builder.py — part concatenation + Jinja2 rendering

```python
from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from functools import cache
from {pkg}.integrations.llm.prompts.index_loader import load_index, PROMPTS_DIR


@cache
def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(PROMPTS_DIR),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        auto_reload=True,   # ファイル更新を検知して再読込
    )


def render_part(rel_path: str, **vars: object) -> str:
    """1 つの部品をレンダリング。

    *.md は静的に読み、*.j2 は Jinja2 で変数展開する。
    """
    if rel_path.endswith((".j2", ".jinja", ".jinja2")):
        return _env().get_template(rel_path).render(**vars)
    return (PROMPTS_DIR / rel_path).read_text(encoding="utf-8")


def build_prompt(llm_id: str, *, lang: str = "en", **vars: object) -> str:
    """index.yaml の llms[llm_id].includes を順に積んで 1 本のプロンプトを作る。

    - 静的部品（.md）は キャッシュ対象として上部に配置済み（authoring 規約に従う）
    - 動的部品（.j2）は **vars で変数を渡してレンダリング
    """
    idx = load_index(PROMPTS_DIR)
    spec = idx["llms"][llm_id]
    parts = [render_part(p, **vars) for p in spec["includes"]]
    return "\n\n".join(parts)
```

### Example: caller side

```python
# src/{pkg}/features/notify/service.py
from {pkg}.integrations.llm.prompts.builder import build_prompt
from {pkg}.integrations.llm.types import AsyncChatFn


async def send_notify(
    duration: int,
    project: str | None,
    *,
    chat: AsyncChatFn,
) -> str:
    system = build_prompt("notify_chat", duration=duration, project=project)
    return await chat([
        {"role": "system", "content": system},
        {"role": "user", "content": "(start)"},
    ])
```

---

## H2 group wrappers (optional)

When implementing the "Grouping" in `prompts-authoring.md`, extend `build_prompt`:

```python
def build_prompt_grouped(llm_id: str, *, lang: str = "en", **vars: object) -> str:
    """同じ category の部品連続を H2 ラッパーで囲んで結合する。"""
    idx = load_index(PROMPTS_DIR)
    spec = idx["llms"][llm_id]
    parts_meta = {p["path"]: p for p in idx.get("parts", [])}
    categories = (idx.get("display") or {}).get("categories") or {}

    out: list[str] = []
    current_category: str | None = None

    for rel in spec["includes"]:
        meta = parts_meta.get(rel, {})
        cat = meta.get("category")
        rendered = render_part(rel, **vars)

        if cat != current_category:
            # category が切り替わったら H2 を入れる
            current_category = cat
            cat_meta = categories.get(cat) if cat else None
            h2 = (cat_meta or {}).get(f"h2_{lang}") if isinstance(cat_meta, dict) else None
            if h2:
                out.append(f"## {h2}")

        out.append(rendered)

    return "\n\n".join(out)
```

---

## Language switching (mirror_of)

```python
def resolve_part_lang(rel_path: str, lang: str) -> str:
    """jp ミラーが存在し lang=jp なら .jp.{ext} に切り替える。"""
    if lang != "jp":
        return rel_path
    p = PROMPTS_DIR / rel_path
    stem, ext = p.stem, p.suffix
    jp_candidate = p.with_name(f"{stem}.jp{ext}")
    return str(jp_candidate.relative_to(PROMPTS_DIR)) if jp_candidate.exists() else rel_path
```

For `build_prompt(..., lang="jp")`, just pass through `render_part(resolve_part_lang(rel, lang), ...)`.

---

## Splitting OpenAI / Anthropic `system` blocks

Some LLM providers pass system / user as separate parameters.
Also provide a **role-separated version** of `build_prompt`:

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class PromptBundle:
    system: str
    user: str


def build_bundle(llm_id: str, *, lang: str = "en", **vars: object) -> PromptBundle:
    idx = load_index(PROMPTS_DIR)
    spec = idx["llms"][llm_id]
    parts_meta = {p["path"]: p for p in idx.get("parts", [])}

    sys_parts: list[str] = []
    usr_parts: list[str] = []
    for rel in spec["includes"]:
        text = render_part(rel, **vars)
        role = parts_meta.get(rel, {}).get("role", "system")
        (sys_parts if role == "system" else usr_parts).append(text)

    return PromptBundle(
        system="\n\n".join(sys_parts),
        user="\n\n".join(usr_parts),
    )
```

This cleanly separates Anthropic's `system=...` argument from `messages=[...]`,
and lets you wrap the entire system into a single `cache_control` block (`llm/cost-cache.md`).

---

## Integration testing

In integration tests of the loader, **do not call the real LLM — verify only the resulting string from build_prompt**:

```python
# tests/integrations/llm/test_prompts.py
def test_notify_chat_build() -> None:
    """notify_chat の includes が順に展開され、role が含まれる。"""
    text = build_prompt("notify_chat", duration=30, project="aituber")
    assert "Notify Role" in text
    assert "Duration: 30" in text


def test_strict_undefined_raises() -> None:
    """未定義変数があれば例外が出る。"""
    with pytest.raises(Exception):
        build_prompt("notify_chat")   # duration を渡さない
```

This catches regressions where "editing a prompt file changes the assembly result".

---

## Things you must not do

```python
# ❌ ローダー内で外部 API を叩く
def build_prompt(...):
    response = httpx.get(...)   # ローダーは pure な変換に限る

# ❌ Undefined を許す
Environment(undefined=Undefined)   # → StrictUndefined にする

# ❌ ファイルパスをハードコード
prompt = Path("prompts/modes/notify/static/role.md").read_text()
# → index.yaml の includes に書く

# ❌ プロンプトをグローバル変数で持って毎回再生成
PROMPT = build_prompt("notify_chat", duration=0)   # vars を変えると不整合
```

---

## Related files

- `llm/prompts-authoring.md` — how to write parts / split them / structure of index.yaml
- `llm/cost-cache.md` — rationale for `cache_control` / the "stack from top" design
- `architecture/composition-root.md` — flow of wiring build_prompt in main.py
- `shared/constants.md` — definition of `PROJECT_ROOT`
