# llm/prompts-authoring — How to write and assemble prompt files

Do not **embed prompts inside code**. Move them into files, **split them into fine-grained pieces**, and assemble them via index.yaml.
The loader implementation is in a separate file (`llm/prompts-loader.md`).

---

## Placement: `prompts/` directly under the project root

```
{project_root}/
├── pyproject.toml
├── prompts/                       # ← プロンプトファイルは src/ の外に置く
│   ├── index.yaml                 # 部品メタデータと組み立て定義の SoT
│   ├── characters/                # キャラごとの不変設定（任意）
│   ├── shared/                    # 横断的な部品（履歴・出力スキーマ・few-shot）
│   ├── modes/                     # ユースケースごとの部品
│   └── settings.yaml.sample       # 環境別パラメータ（任意）
├── src/{pkg}/
│   └── integrations/llm/prompts/  # ローダー実装（YAML 読み込み + Jinja2 + 部品結合）
└── tests/
```

### Why directly under the root

- **Prompts are "configuration + literary content" rather than "code"**, so place them outside the source tree
- Streamers and non-engineers can edit them (without being aware of `src/` in the IDE)
- You can choose whether to bundle them during packaging (controlled individually via `include`)
- Place the loader under `src/{pkg}/integrations/llm/prompts/` and reference `prompts/` relatively from the project root / via `Path`

---

## Part granularity: split per H3 section

The principle is **1 file = 1 H3 section**. Reasons:
- An LLM prompt is an assemblage of many small blocks — "role", "policy", "output format", "input examples", "constraints", ...
- Packing them into a large `.md` makes **which LLM needs which block** invisible
- Small modifications (swapping just one block) make impacts on other LLMs invisible
- Same philosophy as hook injection — **do not put unused information into the context**

### Standard file structure

```markdown
### Notify Role

You are the AITuber, speaking a brief monologue right after finishing a task.
This is a notification voice for the completion of work...
```

- The top of the file starts with **`### {title}`** (H3). The title is **the file body itself is the SoT**
- The body is passed to the LLM as-is, so the Markdown format should be "within what the LLM can read"
- Aim for a few to about 30 lines per file. Consider splitting if it gets longer

---

## Static vs Dynamic: `.md` and `.j2`

| Extension | Purpose | Caching |
|---|---|---|
| `*.md` | Static part. No variables | Eligible for prompt cache |
| `*.j2` | Jinja2 template. Embed via `{{var}}` | Varies per request → not eligible for cache |

```
prompts/modes/notify/
├── static/                          # キャッシュさせたい固定部分
│   ├── role.md                      # 役割定義（不変）
│   ├── policy_chat.md               # 方針（不変）
│   └── output_csv_format.md         # 出力フォーマット（不変）
└── dynamic/                         # リクエストごとに変わる部分
    └── situation.j2                 # 現在の状況（duration、project 等）
```

### Placement principle (alignment with prompt cache)

Express in directory structure the rule **"static values on top, dynamic values on the bottom"** described in `llm/cost-cache.md`:

- When assembling, stack in the order **`static/` → `dynamic/`**
- This makes the entire `static/` a shared prefix, so the prompt cache works
- Placing `dynamic/` templates at the tail keeps the top part cache-hit even if variables change

---

## SoT management with `index.yaml`

Consolidate the location, type, and classification of all parts in `prompts/index.yaml`.
**Hardcoding is forbidden** — do not keep a path list like `STATIC_PARTS = [...]` on the Python side.

### Minimal sample

```yaml
# prompts/index.yaml

# ----- 部品一覧 -----
parts:
  - path: modes/notify/static/role.md
    kind: static
    role: system
    category: role
  - path: modes/notify/static/policy_chat.md
    kind: static
    role: system
    category: policy
  - path: modes/notify/static/output_csv_format.md
    kind: static
    role: system
    category: output_format
  - path: modes/notify/dynamic/situation.j2
    kind: dynamic
    role: user
    category: situation

# ----- LLM ごとの組み立て定義 -----
llms:
  notify_chat:
    template_id: notify_chat
    includes:
      - modes/notify/static/role.md
      - modes/notify/static/policy_chat.md
      - modes/notify/static/output_csv_format.md
      - modes/notify/dynamic/situation.j2
```

### What to write

| Key | Content |
|---|---|
| `parts[]` | `path` of every part + meta (`kind`, `role`, `category`, optionally `group` / `mirror_of`, etc.) |
| `llms[]` | The `includes` list of parts used by each LLM call (the order is the stacking order) |
| `display` | Multilingual labels for UI display names (mode names / category names) (optional) |
| `legacy_aliases` | Mapping of old paths → new IDs (backward compatibility for renames, optional) |

### Order = stacking order = cache boundary

In `includes`, **the top is the head**, the bottom is the tail.
**Static toward the top, dynamic toward the bottom** so the upper part is cache-hit.

---

## Grouping (H2 wrappers)

When you want to group multiple parts under one H2 section (e.g. arrange
personality / speaking_style / preferences under "## Character Profile"):

```yaml
display:
  categories:
    character:
      h2_jp: キャラクター設定
      h2_en: Character Profile
    output_format:
      h2_jp: 出力
      h2_en: Output

parts:
  - path: characters/akane/static/personality.md
    category: character
  - path: characters/akane/static/speaking_style.md
    category: character
```

The loader wraps consecutive parts of the same category into something like `## Character Profile\n\n### personality...\n### speaking_style...`.
Detailed assembly logic is on the `llm/prompts-loader.md` side.

---

## Part i18n / mirrors

When you want the same part in both Japanese and English, use **filename suffixes**:

```
prompts/shared/response_generation/dynamic/
├── character_info.j2          # 英語版
└── character_info.jp.j2       # 日本語版
```

List both in `index.yaml`'s parts and make the pairing explicit with the `mirror_of` key:

```yaml
parts:
  - path: shared/response_generation/dynamic/character_info.j2
    lang: en
  - path: shared/response_generation/dynamic/character_info.jp.j2
    lang: jp
    mirror_of: shared/response_generation/dynamic/character_info.j2
```

The loader switches via the `lang` parameter.

---

## Make "assembly" easy to change

Final prompt = concatenation of parts. **Make the concatenation logic changeable via external config**:

- A/B test by swapping `llms.{id}.includes`
- Adding a part → just append to `parts[]` and to that LLM's `includes[]`
- Hardcoded `STATIC_INSTRUCTIONS = "..."` is forbidden (**adding a new part becomes double work**)

---

## Things you must not do

```python
# ❌ Python コード内に長いプロンプトを直書き
SYSTEM = """あなたは...
（100 行）"""

# ❌ システムプロンプトに動的値を混入（キャッシュが切れる）
system = f"You are an assistant. Now: {now()}"

# ❌ includes リストを Python 側で組む
SYSTEM_PARTS = ["role", "policy", "output_format"]   # → index.yaml に書く

# ❌ 同じプロンプト本文をコピペで複数 LLM にハードコード
TASK_A_PROMPT = "..."
TASK_B_PROMPT = "..."   # 同じ部品を共有するなら parts + includes で
```

---

## Related files

- `llm/prompts-loader.md` — implementation that reads index.yaml and concatenates parts
- `llm/cost-cache.md` — design thinking around the prompt cache
- `dev-kit:yaml` — general operational conventions for `index.yaml` (outside dev-kit Python)
