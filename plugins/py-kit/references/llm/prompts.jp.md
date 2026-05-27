<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# llm/prompts — プロンプトファイル管理

> このファイルは `prompts.md` の日本語ミラーです。

長いプロンプトは Python 文字列リテラルに埋め込まず、**別ファイルとして管理**する。

---

## 配置

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

- `.md`: 静的プロンプト（パラメータなし）
- `.md.j2`: Jinja2 テンプレート（変数を埋め込む）

`prompts/` フォルダは feature ごとに置いてもよい:

```
features/extract/
├── service.py
├── types.py
└── prompts/
    └── extract.md.j2
```

「複数 feature で使う共通プロンプト」は `integrations/llm/prompts/`、
「特定 feature 専用」は `features/{feature}/prompts/`。

---

## 読み込みユーティリティ

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

## 静的プロンプト

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

## Jinja2 テンプレート

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

`StrictUndefined` を設定しているので、未定義変数があれば実行時エラーになる（誤字防止）。

---

## サービス関数からの利用

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

## プロンプトのバージョン管理

プロンプトの変更で挙動が変わる。**履歴を残す** ために 2 通り:

### 方法 1: ファイル名にバージョン

```
prompts/
├── extract_event_system.v1.md
├── extract_event_system.v2.md   # 現役
└── extract_event_system.latest.md -> v2.md   # シンボリックリンク or alias
```

A/B テストや回帰確認に使いやすい。

### 方法 2: 1 ファイル + Git 履歴で追う

Git の `git log` でファイル変更履歴を見る。シンプル。
日付やバージョンは PR 番号コメントで補完:

```markdown
<!-- PR123: location 必須から任意に変更（記事に欠落することが多いため） -->
あなたはニュース記事から...
```

新規プロジェクトでは **方法 2** を推奨（複雑度を抑える）。

---

## プロンプトの単体テスト

プロンプトファイルのレンダリング結果を確認するスナップショットテスト:

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

実際の LLM コールはしない（テスト方針: 単体テスト不要だが、プロンプトの **render 結果検証**
だけは結合テストの一部として有用）。

---

## やってはいけないこと

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

## 関連ファイル

- `llm/providers.md` — 出来上がったメッセージを LLM に渡す
- `llm/instructor.md` — 構造化出力で response_model 指定
- `llm/cost-cache.md` — プロンプトキャッシュ
