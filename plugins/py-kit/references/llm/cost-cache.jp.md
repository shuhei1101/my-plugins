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

## プロンプトキャッシュ — 設計の前提（最重要）

**プロンプトキャッシュは「先頭から共通したぶん」だけ効く。** 中間や末尾だけ揃ってもヒットしない。

LLM への入力は **スタック** のように上から順に積まれていて、その**先頭プレフィックスがバイト単位で一致するぶんだけ** がキャッシュ対象になる。
たとえばシステムプロンプトが完全一致 → そこまではヒット、ユーザーメッセージで分岐 → そこ以降はミス、というふうに切れる。

### 設計ルール: 固定値は上、動的値は下

| 位置 | 内容 |
|---|---|
| **上（先頭）** | 不変のキャラ設定 / 役割定義 / 出力スキーマ / few-shot 例 — **キャッシュさせたい部分** |
| **中** | セッション単位で固定（会話の base context、ペルソナ） |
| **下（末尾）** | リクエストごとに変わる値（直近の会話履歴・ユーザー入力・時刻） |

逆順に積む（動的値を上に置く）と、たった 1 文字の差で**それ以降全部キャッシュミス**になり、コストが跳ね上がる。

### 具体的なやり方

- `system` メッセージは **不変ブロックを優先** して連結する。動的な指示は user メッセージ側に回す
- `messages` 配列も **古い履歴ほど上** に。要約 + 最新数件の場合は「要約 → 古い順履歴 → 最新ユーザー入力」
- few-shot 例はシステム or 最初の user/assistant ペアに置く（ランダム順禁止）
- **`{timestamp}` を system に埋め込まない** — 1 秒変わるたびにキャッシュが切れる

### キャッシュが切れる典型ミス

```python
# ❌ system プロンプトに動的値を入れる
system = f"You are an assistant. Current time: {now_iso()}"
# → 毎回違うのでキャッシュ完全ミス

# ❌ user 履歴の順序を入れ替える
messages = sorted(messages, key=lambda m: m["importance"])   # 並び順が変わる
# → 同じ会話でもキャッシュヒットしない

# ✅ 不変部分を上、動的部分を最下段に
system = STATIC_ROLE_AND_RULES
messages = [
    {"role": "system", "content": SUMMARY_OF_HISTORY},  # session で固定
    *recent_messages,                                    # 末尾だけ毎回変わる
    {"role": "user", "content": user_input},
]
```

---

## プロンプトキャッシュ（Anthropic）

Claude API は `cache_control` でプロンプト前半を明示的にキャッシュ。
**同じシステムプロンプトを多数回使う** ときに効く（読み出し時のコストが入力単価の 10% に下がる）:

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

# 使用量に cache_read_input_tokens / cache_creation_input_tokens が出る
logger.info("llm_call", extra={
    "cache_read_tokens": response.usage.cache_read_input_tokens,
    "cache_creation_tokens": response.usage.cache_creation_input_tokens,
})
```

**条件**:
- システムプロンプト >= 1024 トークン（Haiku は 2048）必要
- 5 分以内に再呼び出しでヒット（`ephemeral`）。長期は `cache_control: {"type": "ephemeral", "ttl": "1h"}` も可
- `cache_control` ブロックは system / messages / tools のいずれにも付けられる。**4 ブロックまで**
- ブロックの境界が「キャッシュの切れ目」。意図的に「ここまで固定」と分けるイメージ

---

## プロンプトキャッシュ（OpenAI）

OpenAI も **自動プロンプトキャッシュ** がある（gpt-4o / o1 以降）。
`>= 1024 トークン` のプロンプトを **同一プレフィックスで送ると 50% 値引きが自動適用** される。**コード変更不要**。
ログに `usage.prompt_tokens_details.cached_tokens` フィールドが出る。

```python
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},   # 同一テキストを送れば自動ヒット
        *messages,
    ],
)
logger.info("llm_call", extra={
    "cached_tokens": response.usage.prompt_tokens_details.cached_tokens,
})
```

**条件**:
- プロンプトの **先頭から最低 1024 トークン** が前回と一致
- 一致単位は 128 トークンごと（端数は切り捨て）
- 5〜10 分でキャッシュは失効（明示制御なし）

### 両者共通の運用ポイント

- **system プロンプトに動的値を埋め込まない**（上記「キャッシュが切れる典型ミス」）
- 1 セッションで何度も同じ system + 履歴 を送るユースケース（チャット / ストリーミング / バッチ抽出）でメリット大
- 1 回しか呼ばないユースケースでは効かない（むしろ Anthropic は cache creation の 25% プレミアムで割高）

---

## Anthropic キャッシュの追加挙動（短く）

実装中によく踏むハマりどころだけ:

- **積み順**: `tools → system → messages` の順で hash 化される。上位を変えると下位全部 invalidate される（tools 変更で全 invalid、system 変更で messages 全 invalid 等）
- **breakpoint の置き方**: `cache_control` は「**変わらない最後のブロック**」に置く。timestamp / 受信メッセージ等の変動ブロックに置くと毎回 cache miss + write になり逆に高い
- **automatic vs explicit**:
  - **automatic** (`request 直下に cache_control 1 個**): 最後の cacheable block に自動で breakpoint が乗る。会話履歴の伸長に追従するので **多ターン会話のデフォルト** に最適
  - **explicit** (ブロック単位に `cache_control`): 最大 4 つまで。tools / system / 過去履歴を別々のキャッシュにしたい時用
- **lookback は 20 ブロックまで**: explicit breakpoint の戻り検索は 20 個まで。長い会話で breakpoint が前回書込み位置から 20 ブロック以上離れると hit しない → 静的部分にもう 1 つ explicit breakpoint を置いて常に書込みが残るようにする
- **最小キャッシュサイズ**（これ未満は無効、エラーも出ない）:
  - Opus 4.5+ / Haiku 4.5: **4096 tokens**
  - Sonnet 4.x / Opus 4.x（4.5 未満）: **1024 tokens**
  - Haiku 3.5: 2048 tokens
  - 確認は `response.usage.cache_creation_input_tokens` と `cache_read_input_tokens` が両方 0 → cache されてない
- **5m vs 1h cache**:
  - **5m**: デフォルト、書込みは base input × 1.25。使うたびに無料で refresh
  - **1h**: 書込みは base input × 2.0。**5 分超 〜 1 時間以内**に再呼び出しがある場合だけ得
  - 混在する場合は **1h を 5m より上（先頭側）** に並べる（順序逆だと API エラー）
- **pre-warming**: `max_tokens: 0` でリクエストを投げると system / tools をキャッシュに書き込むだけして即返る。ユーザー流入前にウォームアップしたい時用

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
