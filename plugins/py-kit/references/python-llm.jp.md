<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python LLM クライアント規約 — py-kit（日本語ミラー）

> このファイルは `python-llm.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-llm.md` にも反映してください。

LLM API（Claude・OpenAI・Gemini・ローカル OSS モデル等）を呼ぶプロジェクトの
アーキテクチャ規約。`python-core.md` と `python-architecture.md` と合わせて読む。

LLM は外部サービスなので同じ DDD レイヤールールに従う：`domain/` に Protocol・
`infrastructure/` に具体実装・composition root で配線。

---

## 1. アーキテクチャ概要

```
domain/
├── repositories/
│   └── llm_client.py            # LlmClient Protocol（「何」）
└── services/
    └── llms/                    # タスク特化型 LLM Protocol（「なぜ」）
        ├── response_generation_llm.py
        ├── classification_llm.py
        └── summarization_llm.py

infrastructure/
└── llm/
    ├── providers/               # ベンダーアダプター（「どう」）
    │   ├── base.py              # 全ベンダー共通の LlmProvider Protocol
    │   ├── claude_provider.py
    │   ├── openai_provider.py
    │   └── gemini_provider.py
    ├── instructor_clients/      # 構造化出力ラッパー（Pydantic 紐付け）
    │   ├── response_generation_claude_client.py
    │   └── classification_openai_client.py
    ├── prompts/                 # プロンプトテンプレート（.md ファイル・起動時ロード）
    │   ├── response_generation.md
    │   └── classification.md
    └── exceptions.py            # LLM 固有例外クラス
```

### 1.1 三層抽象

| レイヤー | 目的 | 例 |
|---|---|---|
| タスク特化型 LLM（`domain/services/llms/`） | ドメインの視点：「コメントを分類したい」 | `ClassificationLlm.classify(comment: str) -> CommentCategory` |
| ベンダープロバイダ（`infrastructure/llm/providers/`） | ベンダーのチャット API への共通アダプター | `ClaudeProvider.invoke(request: LlmRequest) -> str` |
| ワイヤー SDK | ベンダーの Python SDK | `anthropic.Anthropic`・`openai.OpenAI` |

3層の理由：ドメインはビジネス動詞（`classify`・`summarize`・`generate_response`）で話す — 「Claude にこのメッセージを送る」ではない。プロバイダ層はベンダー差異（認証・リクエスト形式・例外型）を共通の `LlmProvider` インターフェースで隠す。1タスクだけ Claude → OpenAI に切り替えるのは `main.py` の配線変更で済む。

---

## 2. `LlmClient` Protocol

全 LLM 呼び出しに共通する最小 Protocol — ドメインが「テキストを返すモデルが欲しい」だけのときに使う：

```python
# domain/repositories/llm_client.py
from typing import Protocol

class LlmClient(Protocol):
    async def complete(
        self,
        prompt: str,
        *,
        max_tokens: int,
        temperature: float = 0.0,
    ) -> str: ...

    async def complete_structured[T: BaseModel](
        self,
        prompt: str,
        *,
        schema: type[T],
        max_tokens: int,
        temperature: float = 0.0,
    ) -> T: ...
```

この最小インターフェースで足りるタスクは `LlmClient` を注入する。独自入出力形を持つタスクは固有の Protocol を定義（§ 4）して注入する。

---

## 3. ベンダープロバイダ層

### 3.1 共通リクエスト型

共有リクエスト型を持つことで、各タスク特化型クライアントがすべてのベンダーに同じ語彙で話せる：

```python
# infrastructure/llm/providers/base.py
from typing import Protocol
from pydantic import BaseModel

class LlmMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LlmRequest(BaseModel):
    model: str
    messages: list[LlmMessage]
    max_tokens: int
    temperature: float = 0.0
    response_format: dict | None = None  # ベンダー固有の構造化出力ヒント


class LlmProvider(Protocol):
    async def invoke(self, request: LlmRequest) -> str: ...
    async def invoke_with_retry(
        self,
        request: LlmRequest,
        *,
        max_retries: int = 3,
    ) -> str: ...
```

### 3.2 具体プロバイダ例 — Claude

```python
# infrastructure/llm/providers/claude_provider.py
import anthropic
from anthropic import APIStatusError, RateLimitError

from {pkg}.infrastructure.llm.providers.base import LlmRequest
from {pkg}.infrastructure.llm.exceptions import (
    LlmRateLimitError,
    LlmServerError,
    LlmBadRequestError,
)
from {pkg}.logger import get_logger

logger = get_logger(__name__)


class ClaudeProvider:
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def invoke(self, request: LlmRequest) -> str:
        try:
            response = await self._client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                system=self._extract_system(request),
                messages=self._to_anthropic_messages(request),
            )
            logger.debug(
                "claude usage: input=%d output=%d cache_read=%d cache_creation=%d",
                response.usage.input_tokens,
                response.usage.output_tokens,
                getattr(response.usage, "cache_read_input_tokens", 0),
                getattr(response.usage, "cache_creation_input_tokens", 0),
            )
            return response.content[0].text

        except RateLimitError as e:
            raise LlmRateLimitError(str(e)) from e
        except APIStatusError as e:
            if 400 <= e.status_code < 500:
                raise LlmBadRequestError(str(e)) from e
            raise LlmServerError(str(e)) from e

    async def invoke_with_retry(self, request: LlmRequest, *, max_retries: int = 3) -> str:
        attempt = 0
        delay = 1.0
        while True:
            try:
                return await self.invoke(request)
            except (LlmRateLimitError, LlmServerError) as e:
                attempt += 1
                if attempt > max_retries:
                    raise
                logger.warning("retrying after %s (attempt %d/%d): %s", delay, attempt, max_retries, e)
                await asyncio.sleep(delay)
                delay *= 2  # 指数バックオフ
```

### 3.3 プロバイダルール

| ルール | 理由 |
|---|---|
| ベンダー例外を必ずドメイン例外でラップ（`LlmRateLimitError`・`LlmServerError` 等） | 呼び出し元コードが `except anthropic.APIStatusError` を絶対書かない |
| トークン使用量を常に DEBUG ログ（`input`・`output`・`cache_read`・`cache_creation`） | コスト分析・キャッシュ効果測定 |
| `max_tokens` は常に明示設定 | ベンダーのデフォルトは予測不能・変わる |
| `temperature=0.0` がデフォルト — 高い値は意識的に選ぶ | 再現性 |
| `invoke_with_retry` は opt-in；`invoke` 生で独自リトライ実装も可 | 一部タスクはリトライ不可（冪等性懸念） |

---

## 4. タスク特化型 LLM クライアント

タスク特化型クライアントはドメインが依存する Protocol を定義する。典型的に **Instructor**（またはベンダー native 構造化出力）で Pydantic スキーマを LLM 呼び出しに紐付ける。

### 4.1 ドメインでのタスク Protocol

```python
# domain/services/llms/classification_llm.py
from typing import Protocol
from {pkg}.domain.value_objects.comment_category import CommentCategory

class ClassificationLlm(Protocol):
    async def classify(self, comment_text: str) -> CommentCategory: ...
```

### 4.2 具体実装 — Instructor + Claude

```python
# infrastructure/llm/instructor_clients/classification_claude_client.py
import instructor
import anthropic
from pydantic import BaseModel, Field

from {pkg}.domain.value_objects.comment_category import CommentCategory
from {pkg}.infrastructure.llm.prompts import load_prompt
from {pkg}.logger import get_logger

logger = get_logger(__name__)


class _ClassificationResult(BaseModel):
    """Instructor が強制するスキーマ。"""
    category: Literal["spam", "question", "praise", "criticism", "other"]
    confidence: float = Field(..., ge=0.0, le=1.0)


_SYSTEM_PROMPT = load_prompt("classification")  # prompts/classification.md


class ClassificationClaudeClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = instructor.from_anthropic(anthropic.AsyncAnthropic(api_key=api_key))
        self._model = model

    async def classify(self, comment_text: str) -> CommentCategory:
        logger.debug("classifying comment: %d chars", len(comment_text))
        result = await self._client.messages.create(
            model=self._model,
            max_tokens=256,
            response_model=_ClassificationResult,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": comment_text},
            ],
        )
        return CommentCategory(value=result.category, confidence=result.confidence)
```

### 4.3 なぜ Instructor（推奨）

Instructor（または LangChain の `with_structured_output`）の利点：

- 生文字列パースではなく型付き Pydantic オブジェクト
- ベンダー形式へのスキーマ自動変換
- パース失敗時の自動リトライ
- ベンダー間で同じコード形

Instructor なしでは、ベンダー毎の JSON-schema 配管・コードフェンスの正規表現パース・出力不正時のリトライ自作ロジック — 全部バグの温床。

### 4.4 出力スキーマルール

| ルール | 理由 |
|---|---|
| 出力スキーマは Pydantic `BaseModel` | Instructor が要求；境界バリデーション |
| 範囲値にはフィールドバリデーション（`Field(..., ge=0, le=1)`） | LLM は範囲外値を静かに返す |
| 閉集合カテゴリには `Literal[...]` | LLM は同義語を返す（"praise" vs "compliment"） |
| 1タスク = 1スキーマ；無関係なタスクで再利用しない | 統一スキーマは神オブジェクト化する |
| 境界を越える前にドメイン値オブジェクトでラップ | スキーマは内部；ドメインコードは値オブジェクトを受ける |

---

## 5. プロンプト管理

### 5.1 プロンプトはコードではなくファイルに住む

```
infrastructure/llm/prompts/
├── classification.md
├── response_generation.md
├── summarization.md
└── ...
```

### 5.2 ローダー

```python
# infrastructure/llm/prompts/__init__.py
from functools import cache
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent


@cache
def load_prompt(name: str) -> str:
    """プロンプトテンプレートを名前でロード。初回読み込み後キャッシュ。"""
    path = _PROMPTS_DIR / f"{name}.md"
    return path.read_text(encoding="utf-8")
```

### 5.3 テンプレート化

変数置換には `string.Template` か Jinja2 を使う — ファイル内容に f-string を使わない（変数欠落のコンパイル時チェックなし）。

```python
# infrastructure/llm/prompts/response_generation.md
You are responding to: ${user_name}.
The context is: ${context}.
```

```python
from string import Template

template = Template(load_prompt("response_generation"))
prompt = template.substitute(user_name=user.name, context=ctx)
```

複雑なプロンプト（ループ・条件分岐）は Jinja2：

```python
from jinja2 import Template
template = Template(load_prompt("complex_prompt"))
prompt = template.render(history=messages, user=user)
```

### 5.4 プロンプトバージョニング

本番のプロンプトを変更するとき：

1. 先頭に PR 番号と理由のコメントを追加
2. 前バージョンを最低1リリースサイクル分はインラインで（コメントアウトで）残す
3. 出力構造が変わるなら Pydantic スキーマもバンプ

```markdown
<!-- PR142: トーン指示を厳格化。出力がより簡潔に。 -->
You are a concise assistant.
...

<!-- PR130（旧）:
You are a helpful assistant.
...
-->
```

### 5.5 system vs user ロール

| 内容 | ロール |
|---|---|
| ペルソナ・タスク説明・出力形式・例 | `system` |
| モデルに反応してほしい実際の入力 | `user` |
| マルチターンダイアログの過去ターン | `user` / `assistant` 交互 |

動的なユーザーデータを絶対 `system` ロールに入れない — プロンプトキャッシュ経由で他ターンに漏れる可能性。

---

## 6. トークン・コスト・キャッシュ管理

### 6.1 `max_tokens` は常に設定

ベンダーデフォルトは差があり、出力を静かにキャップする可能性がある。常に設定。

```python
# ✅ 良い — 明示
LlmRequest(model="claude-sonnet-4-6", messages=[...], max_tokens=1024)

# ❌ 悪い — 静かなデフォルト
client.messages.create(model="claude-sonnet-4-6", messages=[...])
```

期待出力サイズ + 30% ヘッドルームで `max_tokens` を選ぶ。

### 6.2 トークン使用量をログ

各プロバイダ実装がトークン使用量を DEBUG でログ — コール再実行なしのコスト分析が可能。

```python
logger.debug(
    "claude usage: input=%d output=%d cache_read=%d cache_creation=%d",
    r.usage.input_tokens, r.usage.output_tokens,
    getattr(r.usage, "cache_read_input_tokens", 0),
    getattr(r.usage, "cache_creation_input_tokens", 0),
)
```

定期ジョブがこれらを集約して日次コストレポートに。

### 6.3 プロンプトキャッシュ

≥1024 トークンの静的システムプロンプトは `cache_control` で入力コスト削減：

```python
# Claude — Anthropic 固有
response = await client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": user_input}],
)
```

最初の呼び出しがキャッシュ書き込み（追加課金）；以降は無料読み出し。キャッシュ TTL は約5分 — リトライ・バッチがその窓内に収まるよう設計。

### 6.4 バルク操作には Batch API

10件以上の独立した呼び出しで即時応答が不要なら、batch API（Anthropic Batch API・OpenAI Batch API）。約50%安く・24時間ターンアラウンド。

```python
# 投げっぱなしバックグラウンドジョブとして許容
batch = await client.messages.batches.create(requests=[...])
# batch.id をポーリング・後で結果取得
```

レイテンシ重視（チャット UI）はバッチではなくストリーミング。

### 6.5 ユーザー向け出力にはストリーミング

```python
async with client.messages.stream(
    model=request.model,
    max_tokens=request.max_tokens,
    messages=self._to_anthropic_messages(request),
) as stream:
    async for text in stream.text_stream:
        yield text
```

チャット UI で体感レイテンシ改善。構造化出力（Instructor）にはストリーミング不可 — 完全応答を待つ。

---

## 7. プロバイダ選択とマルチモデル構成

AITuber パターンから着想：タスク毎に異なるベンダー・モデルを使う。

### 7.1 タスク毎モデル設定

```python
# config.py
class LlmModelsConfig(BaseModel):
    classification: str = "claude-haiku-4-5-20251001"      # 高速・安価
    response_generation: str = "claude-sonnet-4-6"          # 品質重視
    summarization: str = "claude-sonnet-4-6"
    embedding: str = "voyage-3"                              # 別ベンダー

class Settings(BaseModel):
    anthropic_api_key: SecretStr
    voyage_api_key: SecretStr
    llm_models: LlmModelsConfig = Field(default_factory=LlmModelsConfig)
```

### 7.2 composition root での配線

```python
# main.py
claude = ClaudeProvider(settings.anthropic_api_key.get_secret_value())
voyage = VoyageProvider(settings.voyage_api_key.get_secret_value())

classification_llm = ClassificationClaudeClient(
    api_key=settings.anthropic_api_key.get_secret_value(),
    model=settings.llm_models.classification,
)
response_llm = ResponseGenerationClaudeClient(
    api_key=settings.anthropic_api_key.get_secret_value(),
    model=settings.llm_models.response_generation,
)
embedding_llm = EmbeddingClient(provider=voyage)
```

ドメインは使っているベンダーを知らない；タスク特化型 Protocol にだけ依存。response_generation タスクを OpenAI に切り替えるのは config + 配線変更だけ — ドメイン変更なし。

### 7.3 プロバイダ間フォールバック（任意）

高可用性シナリオ向け：

```python
class FallbackProvider:
    """Provider Decorator：primary 失敗時に secondary へフォールバック。"""

    def __init__(self, primary: LlmProvider, secondary: LlmProvider) -> None:
        self._primary = primary
        self._secondary = secondary

    async def invoke(self, request: LlmRequest) -> str:
        try:
            return await self._primary.invoke(request)
        except LlmServerError as e:
            logger.warning("primary LLM failed, falling back: %s", e)
            return await self._secondary.invoke(request)
```

これは Decorator（`python-architecture.md § 6.4`）；配線ステップで合成する。

---

## 8. エラー処理

### 8.1 LLM 例外階層

```python
# infrastructure/llm/exceptions.py
class LlmError(Exception): ...

class LlmRateLimitError(LlmError): ...       # リトライ可
class LlmServerError(LlmError): ...           # リトライ可
class LlmBadRequestError(LlmError): ...       # リトライ不可 — プロンプト修正
class LlmAuthenticationError(LlmError): ...   # リトライ不可 — キー修正
class LlmTimeoutError(LlmError): ...           # リトライ可
class LlmContentFilterError(LlmError): ...    # リトライ不可 — コンテンツポリシー
```

### 8.2 リトライ可・不可

| 例外 | リトライ | アクション |
|---|---|---|
| `LlmRateLimitError` | ✅ Yes | 指数バックオフ・Retry-After ヘッダー尊重 |
| `LlmServerError`（5xx） | ✅ Yes | 指数バックオフ・最大3回 |
| `LlmTimeoutError` | ✅ Yes | バックオフ・最大2回 |
| `LlmBadRequestError`（4xx） | ❌ No | 上位へ伝播；プロンプト・リクエストが間違っている |
| `LlmAuthenticationError` | ❌ No | 上位へ伝播；config 修正 |
| `LlmContentFilterError` | ❌ No | 上位へ伝播；入力がベンダーポリシー違反 |

### 8.3 ユースケース境界で LLM 例外をラップ

ユースケースが LLM 例外をドメイン例外に翻訳：

```python
# application/use_cases/classify_comment.py
class ClassifyCommentUseCase:
    def __init__(self, llm: ClassificationLlm) -> None:
        self._llm = llm

    async def execute(self, comment_text: str) -> CommentCategory:
        try:
            return await self._llm.classify(comment_text)
        except LlmContentFilterError:
            return CommentCategory.skipped("content_policy")
        except LlmError as e:
            raise ClassificationUnavailableError("LLM failure") from e
```

HTTP 層は `anthropic.APIStatusError` を絶対見ない — ドメイン例外のみ。

---

## 9. LLM コードのテスト

LLM 呼び出しは非決定論的。実 API ではなく**フェイク LLM**（缶詰応答を返す）に対してテスト。

```python
# tests/mocks/fake_classification_llm.py
from {pkg}.domain.value_objects.comment_category import CommentCategory
from {pkg}.domain.services.llms.classification_llm import ClassificationLlm

class FakeClassificationLlm:
    def __init__(self, response_map: dict[str, CommentCategory]) -> None:
        self._response_map = response_map

    async def classify(self, comment_text: str) -> CommentCategory:
        return self._response_map.get(comment_text, CommentCategory.other())
```

```python
# tests/application/use_cases/test_classify_comment.py
def test_returns_skipped_when_content_filter_triggers():
    llm = FakeClassificationLlm({...})
    # ...
```

実モデルが本当に必要な統合テスト（稀 — `vcrpy` 等での record-and-replay スナップショットテストを推奨）は env var でガードし、CI で毎回トークン消費しない。

---

## 10. Definition of Done — LLM チェックリスト

LLM を触る変更：

- [ ] ドメインがタスク特化型 Protocol（`domain/services/llms/`）を持つ — 汎用 `LlmClient` ではない
- [ ] 具体クライアントが `infrastructure/llm/instructor_clients/`（Pydantic 紐付け）か `infrastructure/llm/providers/`（生テキスト）に住む
- [ ] プロンプトが `infrastructure/llm/prompts/` の `.md` ファイル・コード内ではない
- [ ] 構造化出力の Pydantic スキーマが `Field` 制約と閉集合 `Literal` を使う（§ 4.4）
- [ ] `max_tokens` 明示設定（§ 6.1）
- [ ] トークン使用量を DEBUG ログ（§ 6.2）
- [ ] プロバイダがベンダー例外をドメイン例外でラップ（§ 8.1）
- [ ] ユースケースが LLM 例外をドメイン例外でラップ（§ 8.3）
- [ ] テストがフェイク LLM 使用・実 API ではない（§ 9）
- [ ] プロンプトが静的・大きいならプロンプトキャッシュ適用（§ 6.3）
- [ ] タスク毎モデルが `Settings.llm_models.{task}` で設定可能（§ 7.1）
