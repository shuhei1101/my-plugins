# llm/prompts — Prompt file management

Don't embed long prompts in Python string literals — **manage them as separate files**.

---

## Layout

```
src/{pkg}/
└── integrations/
    └── llm/
        ├── openai_client.py
        └── prompts/
            ├── extract_event_system.md
            ├── extract_event_user.md.j2
            ├── summarize_system.md
            └── translate_system.md.j2
```

- `.md`: static prompts (no parameters)
- `.md.j2`: Jinja2 templates (variables embedded)

A `prompts/` folder can also live per feature:

```
features/extract/
├── service.py
├── types.py
└── prompts/
    └── extract.md.j2
```

"Shared prompts used by multiple features" go in `integrations/llm/prompts/`;
"feature-specific" ones in `features/{feature}/prompts/`.

---

## Loader utility

```python
# src/{pkg}/integrations/llm/prompt_loader.py
from __future__ import annotations
from pathlib import Path
from functools import cache
from jinja2 import Environment, FileSystemLoader, StrictUndefined

_PROMPTS_DIR = Path(__file__).parent / "prompts"


@cache
def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(_PROMPTS_DIR),
        undefined=StrictUndefined,   # 未定義変数でエラー
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_prompt(name: str, **vars: object) -> str:
    """{prompts}/<name> をレンダリングする。

    `.md` は静的に読み込み、`.md.j2` は Jinja2 で変数展開。
    """
    if name.endswith(".j2"):
        return _env().get_template(name).render(**vars)
    return (_PROMPTS_DIR / name).read_text(encoding="utf-8")
```

---

## Static prompts

```markdown
<!-- src/{pkg}/integrations/llm/prompts/extract_event_system.md -->
あなたはニュース記事からイベント情報を抽出する専門家です。

抽出ルール:
- 開催日が明記されていない場合は null とする
- 場所は最も具体的な表記を採用する
- カテゴリは事前定義された 4 種類から選ぶ

JSON で返答してください。
```

```python
system_text = render_prompt("extract_event_system.md")
```

---

## Jinja2 templates

```jinja
{# src/{pkg}/integrations/llm/prompts/extract_event_user.md.j2 #}
以下の記事から{{ field_name }}を抽出してください。

# 記事

{{ article }}

# 制約

- 最大 {{ max_items }} 件
{% if examples %}
# 例

{% for ex in examples %}
- {{ ex }}
{% endfor %}
{% endif %}
```

```python
user_text = render_prompt(
    "extract_event_user.md.j2",
    field_name="イベント情報",
    article="...",
    max_items=5,
    examples=["コンサート", "展覧会"],
)
```

`StrictUndefined` is configured, so any undefined variable raises a runtime error (typo prevention).

---

## Use from service functions

```python
# src/{pkg}/features/extract/service.py
from {pkg}.integrations.llm.prompt_loader import render_prompt


async def extract_event(article: str, *, client: instructor.AsyncInstructor) -> ExtractedEvent:
    system = render_prompt("extract_event_system.md")
    user = render_prompt(
        "extract_event_user.md.j2",
        article=article,
        field_name="イベント情報",
        max_items=5,
    )

    return await client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=ExtractedEvent,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_retries=3,
    )
```

---

## Prompt versioning

A prompt change changes behavior. **Keep a history** — two approaches:

### Approach 1: Version in the filename

```
prompts/
├── extract_event_system.v1.md
├── extract_event_system.v2.md   # 現役
└── extract_event_system.latest.md -> v2.md   # シンボリックリンク or alias
```

Useful for A/B tests and regression checks.

### Approach 2: One file + track with Git history

Track file changes through `git log`. Simple.
Annotate dates or versions with PR-number comments:

```markdown
<!-- PR123: location 必須から任意に変更（記事に欠落することが多いため） -->
あなたはニュース記事から...
```

For new projects, **Approach 2** is recommended (keeps complexity down).

---

## Unit testing prompts

A snapshot test that verifies the render output of a prompt file:

```python
# tests/integrations/llm/test_prompts.py
from {pkg}.integrations.llm.prompt_loader import render_prompt


def test_extract_event_user_renders() -> None:
    text = render_prompt(
        "extract_event_user.md.j2",
        article="サンプル記事",
        field_name="イベント情報",
        max_items=3,
    )
    assert "サンプル記事" in text
    assert "最大 3 件" in text


def test_extract_event_system_static() -> None:
    text = render_prompt("extract_event_system.md")
    assert "抽出ルール" in text
```

Doesn't actually call the LLM (testing policy: unit tests not required, but
**verifying prompt render results** is useful as part of integration tests).

---

## What not to do

```python
# ❌ Python コード内に長いプロンプトを埋め込む
SYSTEM = """あなたは...
（100 行）"""
# → prompts/*.md に切り出す

# ❌ f-string で変数を埋め込む（エスケープ事故）
prompt = f"記事: {article}"
# article に "{name}" などが含まれると Jinja より弱い検証で事故る
# → Jinja2 でエスケープ制御

# ❌ Undefined を許す（誤字に気付けない）
Environment(undefined=Undefined)
# → StrictUndefined にする
```

---

## Related files

- `llm/providers.md` — Pass the assembled messages to the LLM
- `llm/instructor.md` — Specify response_model for structured output
- `llm/cost-cache.md` — Prompt caching
