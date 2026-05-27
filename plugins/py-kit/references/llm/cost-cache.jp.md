<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# llm/cost-cache — トークン管理とコスト最適化

> このファイルは `cost-cache.md` の日本語ミラーです。

LLM API のコストを抑える定石。

---

## まず計測

最適化前にトークン使用量をログ出力する（`llm/providers.md` の例参照）:

```python
logger.info("llm_call", extra={
    "provider": "openai",
    "model": "gpt-4o-mini",
    "input_tokens": usage.prompt_tokens,
    "output_tokens": usage.completion_tokens,
})
```

JSON Lines を集計して `input_tokens × 入力単価 + output_tokens × 出力単価` で日次コストを出す。

---

## `max_tokens` で出力を制限

```python
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=req,
    max_tokens=512,    # 出力上限
)
```

無制限だと「冗長な前置きで上限まで使い切る」事象が起きる。**用途に応じて適切に絞る**:

| 用途 | max_tokens 目安 |
|---|---|
| Yes/No 判定 | 50 |
| 短い分類タグ | 100 |
| 1 段落の要約 | 300 |
| 構造化抽出（Pydantic） | 800-1024 |
| 長い文章生成 | 2048+ |

---

## プロンプトキャッシュ（Anthropic）

Claude API は `cache_control` でプロンプト前半をキャッシュできる。
**同じシステムプロンプトを多数回使う** ときに効く（90% 値引き）:

```python
response = await client.messages.create(
    model="claude-haiku-4-5-20251001",
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},   # 5 分キャッシュ
        },
    ],
    messages=[{"role": "user", "content": user_text}],
    max_tokens=1024,
)

# 使用量に cache_read_input_tokens が出る
logger.info("llm_call", extra={
    "cache_read_tokens": response.usage.cache_read_input_tokens,
    "cache_creation_tokens": response.usage.cache_creation_input_tokens,
})
```

**条件**:
- システムプロンプト >= 1024 トークン（Haiku は 2048）必要
- 5 分以内に再呼び出しでヒット
- システム + ユーザーメッセージの一部もキャッシュできる

---

## プロンプトキャッシュ（OpenAI）

OpenAI も自動プロンプトキャッシュがある（gpt-4o 以降）。`>= 1024 トークン` のプロンプトを
同一プレフィックスで送ると 50% 値引きが自動適用される。**コード変更不要**。
ログに `cached_tokens` フィールドが出る。

---

## モデル選定

| 用途 | 推奨モデル |
|---|---|
| 単純分類 / Yes-No / タグ付け | `gpt-4o-mini` / `claude-haiku-4-5` |
| 構造化抽出 / 中程度の推論 | `gpt-4o` / `claude-sonnet-4-6` |
| 複雑な推論 / 長文 / コード生成 | `claude-opus-4-7` / `o3` |

**最小モデルで通せないか試す → 必要なら上げる**。最初から最大モデルは贅沢。

---

## Batch API

OpenAI / Anthropic とも Batch API がある。**非同期で 24h 以内に処理**、**50% 値引き**。

- リアルタイム不要な大量処理（夜間バッチで分類・抽出など）に最適
- レスポンスは S3 / Files API 経由でまとめて取得

```python
# OpenAI Batch
batch_input = [
    {
        "custom_id": "req-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {"model": "gpt-4o-mini", "messages": [...]},
    },
    ...
]
# JSONL ファイルにして Files API でアップロード、Batches API で submit
```

詳細は各社ドキュメント。コードは標準化されているので「夜間バッチ」と決まったら採用検討。

---

## ストリーミング（コスト軽減ではないが UX 改善）

```python
async for chunk in chat_stream(req):
    print(chunk, end="", flush=True)
```

ユーザー体感の改善。最初のトークンまでの時間を短縮できる（TTFT）。
コストは変わらない（むしろメタデータでわずかに増える）。

---

## 履歴の刈り取り

会話履歴をそのまま積み続けると指数的にトークンが膨らむ。
**直近 N 件 + 古い履歴は要約** が定石:

```python
async def trimmed_messages(history: list[Message], summary: str) -> list[Message]:
    """要約 + 直近 10 件だけ残す。"""
    recent = history[-10:]
    return [
        {"role": "system", "content": f"会話の要約: {summary}"},
        *recent,
    ]
```

要約自体も LLM で（小さなモデルで）。

---

## やってはいけないこと

```python
# ❌ max_tokens 無制限
# 一発のリクエストで無駄に多くの出力をされる

# ❌ プロンプトキャッシュなしで巨大システムを毎回送る
# 同じプロンプトを 1000 回送ると 90% 損する

# ❌ 単純タスクに巨大モデル
# Yes/No 判定に Opus は過剰

# ❌ レスポンスをログに垂れ流す（コスト追跡できない）
# token 数を必ず構造化ログに残す
```

---

## 関連ファイル

- `llm/providers.md` — トークン使用量ログの実装
- `llm/exceptions-retry.md` — rate-limit と並んでコストに影響
- `shared/logger.md` — 構造化ログでコスト集計
