<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# concurrency/async — asyncio 規約

> このファイルは `async.md` の日本語ミラーです。

Python 3.12+ の asyncio 機能を前提に書く。

---

## 並行実行: `asyncio.TaskGroup`

複数の async 関数を並列に走らせるなら `TaskGroup` を使う（`asyncio.gather` は **使わない**）。

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[dict]:
    """複数 URL を並列取得して結果リストを返す。"""
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]

    return [t.result() for t in tasks]
```

TaskGroup の利点（vs `gather`）:
- どれか 1 つが例外を出したら他もキャンセルされる
- 例外は `ExceptionGroup` でまとまる（複数同時失敗を扱える）
- `with` ブロックを抜けた時点で全タスク完了が保証される

---

## タイムアウト: `asyncio.timeout`

```python
async def fetch_with_timeout(url: str) -> dict:
    """30 秒でタイムアウトする HTTP fetch。"""
    async with asyncio.timeout(30):
        return await fetch(url)
```

`async with asyncio.timeout(N)` ブロック内で発生した async 処理が N 秒超えたら `TimeoutError` を投げる。
`asyncio.wait_for` は古い API なので新規コードでは使わない。

---

## キャンセル

タスクキャンセルは `task.cancel()`:

```python
task = asyncio.create_task(long_running())
await asyncio.sleep(5)
task.cancel()

try:
    await task
except asyncio.CancelledError:
    pass
```

**`CancelledError` は再 raise する** のが原則。キャンセル伝播を止めない:

```python
async def my_op() -> None:
    try:
        await long_running()
    except asyncio.CancelledError:
        # クリーンアップ
        await cleanup()
        raise   # ← 必ず raise
```

---

## sync / async 境界

### sync → async（ブロッキング処理を async から呼ぶ）

```python
import asyncio
import time

def blocking_io() -> str:
    """同期ブロッキング処理（例: requests / open / time.sleep）。"""
    time.sleep(1)
    return "done"


async def async_caller() -> str:
    """別スレッドで実行して await できる形にする。"""
    return await asyncio.to_thread(blocking_io)
```

`asyncio.to_thread` は CPU 時間が短い IO バウンド処理に使う。
CPU バウンドなら `concurrency/parallelism.md` を参照。

### async → sync（async 関数を sync コードから呼ぶ）

```python
import asyncio

async def my_async_op() -> str: ...

# top-level script で
result = asyncio.run(my_async_op())
```

`asyncio.run` は **エントリポイントで 1 度だけ**。
ネストして呼ぶと `RuntimeError` になる（Jupyter 等は `nest_asyncio` で回避するが、通常コードでは避ける）。

---

## async コンテキストマネージャ

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator


@asynccontextmanager
async def open_session(url: str) -> AsyncIterator[Session]:
    """セッションを開き、終了時に必ず close する。"""
    session = await Session.connect(url)
    try:
        yield session
    finally:
        await session.close()


# 使い方
async def use_it() -> None:
    async with open_session("ws://example.com") as session:
        await session.send("hello")
```

`__aenter__` / `__aexit__` を持つクラスを書く方法もあるが、**関数 + `@asynccontextmanager`** の方が軽量。

---

## async generator

```python
from typing import AsyncIterator


async def stream_messages(client: SomeClient) -> AsyncIterator[str]:
    """サーバからのメッセージを yield する。"""
    async for raw in client.subscribe():
        yield raw.decode("utf-8")


# 使い方
async for msg in stream_messages(client):
    print(msg)
```

LLM のストリーミング応答も同じパターン:

```python
async def chat_stream(req: ChatRequest) -> AsyncIterator[str]:
    """LLM レスポンスを 1 トークンずつ yield する。"""
    async for chunk in _client.chat_stream(req):
        yield chunk.content
```

---

## Queue を使った Producer / Consumer

```python
async def producer(queue: asyncio.Queue[str]) -> None:
    for i in range(10):
        await queue.put(f"item-{i}")
        await asyncio.sleep(0.1)
    await queue.put(None)   # 終了センチネル


async def consumer(queue: asyncio.Queue[str]) -> None:
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"got {item}")


async def main() -> None:
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue))
        tg.create_task(consumer(queue))
```

`runtime/` で WebSocket メッセージのバッファリング等に使う。

---

## Lock / Semaphore

```python
# 排他
lock = asyncio.Lock()

async def critical_section() -> None:
    async with lock:
        # 同時に 1 つしか入れない
        ...


# 同時実行数を制限
sem = asyncio.Semaphore(3)

async def limited_fetch(url: str) -> dict:
    async with sem:
        return await fetch(url)   # 最大 3 並列
```

---

## やってはいけないこと

```python
# ❌ asyncio.gather（TaskGroup に置き換える）
results = await asyncio.gather(*tasks)

# ❌ asyncio.wait_for（asyncio.timeout に置き換える）
result = await asyncio.wait_for(coro, timeout=10)

# ❌ async 関数を await せずに呼ぶ（コルーチンオブジェクトを捨てる）
async_op()   # 結果が走らない、警告も出る

# ❌ CancelledError を握りつぶす
try:
    await op()
except asyncio.CancelledError:
    pass   # ← raise しないとキャンセル伝播が止まる

# ❌ sync ブロッキングを async 関数内で素で呼ぶ（イベントループを止める）
async def bad() -> None:
    time.sleep(1)   # NG。asyncio.sleep か asyncio.to_thread
```

---

## 関連ファイル

- `concurrency/parallelism.md` — CPU バウンド処理
- `architecture/composition-root.md` — async 起動の典型
- `core/type-hints.md` — Awaitable / AsyncIterator の型
