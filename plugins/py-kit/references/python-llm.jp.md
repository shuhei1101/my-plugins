<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python LLM クライアント規約 — py-kit（日本語ミラー）

> このファイルは `python-llm.md` の日本語ミラーです。Claude Code には読み込まれません。

LLM API（Claude・OpenAI など）を呼ぶプロジェクトのアーキテクチャ規約。
`python-core.md` と `python-architecture.md` と合わせて読む。

---

## アーキテクチャ原則

LLM を外部サービスとして扱う。全 LLM API 呼び出しはドメイン層に定義した Protocol インターフェースを通し、具体実装はインフラ層に置く。

```python
# domain/repositories/llm_client.py
class LlmClient(Protocol):
    async def complete(self, prompt: str, *, max_tokens: int = 1024) -> str: ...
    async def complete_structured(self, prompt: str, schema: type[T]) -> T: ...

# infrastructure/llm/claude_client.py
class ClaudeClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    async def complete(self, prompt: str, *, max_tokens: int = 1024) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
```

---

## 構造化出力

構造化 LLM 出力には Pydantic モデルを使う。スキーマ強制には Instructor を推奨。

```python
from instructor import from_anthropic
import anthropic
from pydantic import BaseModel

class IssueList(BaseModel):
    issues: list[str]
    priority: Literal["high", "medium", "low"]

client = from_anthropic(anthropic.Anthropic())
result: IssueList = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    response_model=IssueList,
    messages=[{"role": "user", "content": prompt}],
)
```

---

## プロンプト管理

- プロンプトテンプレートは `.md` ファイルとして `{package_name}/prompts/` に保存する
- 起動時に `Path(__file__).parent / "prompts" / "{name}.md"` でロードする
- 関数ボディ内にプロンプトのテキストをハードコードしない
- 変数置換には `str.format(**kwargs)` または `string.Template` を使う

---

## トークンとコスト管理

- `max_tokens` は常に明示的に設定する — デフォルト値に頼らない
- 全 API 呼び出しのトークン使用量（入力・出力）を DEBUG レベルでログに記録する
- 1024 トークンを超える静的なシステムプロンプトにはプロンプトキャッシュ（`cache_control`）を適用する
- 独立した呼び出しが10件超の場合はバッチ API を使う

---

## エラーハンドリング

```python
from anthropic import RateLimitError, APIStatusError

try:
    result = await llm_client.complete(prompt)
except RateLimitError:
    # 指数バックオフ、最大3回リトライ
    ...
except APIStatusError as e:
    logger.error("LLM API error %s: %s", e.status_code, e.message)
    raise
```

LLM エラーはアプリケーション層に届く前にドメイン例外にラップする。
