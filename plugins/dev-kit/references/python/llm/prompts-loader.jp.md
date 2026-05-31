<!-- This file is a Japanese mirror of prompts-loader.md. When updating the English original, update this file too. -->
# llm/prompts-loader — プロンプトのローダー実装

`prompts/index.yaml` を読み、部品ファイル群を Jinja2 でレンダリングして 1 つのプロンプトに組み立てる実装規約。
プロンプトの **書き方** は `llm/prompts-authoring.md` 参照。

---

## 配置

```
src/{pkg}/integrations/llm/prompts/
├── __init__.py
├── index_loader.py       # prompts/index.yaml の読み込みとキャッシュ
├── builder.py            # 部品結合 + Jinja2 レンダリング
└── types.py              # PromptPart / PromptSpec 等の DTO
```

ローダーは **`src/` 配下**（プロジェクトコード）に置き、プロンプト本体（`prompts/`）はルート直下に置く。

---

## プロジェクトルートの解決

ローダーは `prompts/` フォルダの場所を知る必要がある。
`shared/constants.py` の `PROJECT_ROOT` を使う:

```python
# src/{pkg}/integrations/llm/prompts/index_loader.py
from __future__ import annotations
from pathlib import Path
from {pkg}.shared.constants import PROJECT_ROOT

PROMPTS_DIR: Path = PROJECT_ROOT / "prompts"
```

---

## index_loader.py — index.yaml の読み込み

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

ポイント:
- `@cache` で 1 プロセス 1 回だけ読む（起動時の I/O を抑える）
- 戻り値は `TypedDict` で型付け（dict のまま扱う）
- ホットリロードしたい時は `load_index.cache_clear()` を呼べばよい

---

## builder.py — 部品結合 + Jinja2 レンダリング

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

### 例: 呼び出し側

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

## H2 グループラッパー（任意）

`prompts-authoring.md` の「グループ化」を実装する場合、`build_prompt` を拡張:

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

## 言語切替（mirror_of）

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

`build_prompt(..., lang="jp")` のときに `render_part(resolve_part_lang(rel, lang), ...)` を通せばよい。

---

## OpenAI / Anthropic の `system` ブロック分離

LLM プロバイダによっては system / user を別パラメータに渡す。
`build_prompt` を **role 別に分けて返すバージョン** も用意:

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

これにより Anthropic の `system=...` 引数と `messages=[...]` を綺麗に分けられ、
かつ system 全体を 1 つの `cache_control` ブロックに包めるようになる（`llm/cost-cache.md`）。

---

## 結合テスト

ローダーの結合テストでは **実 LLM は呼ばず、build_prompt の結果文字列だけ検証**:

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

これで「プロンプトファイルを編集すると組み立て結果が変わる」回帰を検出できる。

---

## やってはいけないこと

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

## 関連ファイル

- `llm/prompts-authoring.md` — 部品の書き方・分割・index.yaml の構造
- `llm/cost-cache.md` — `cache_control` / 「上から積む」設計の根拠
- `architecture/composition-root.md` — build_prompt を main.py で配線する流れ
- `shared/constants.md` — `PROJECT_ROOT` の定義
