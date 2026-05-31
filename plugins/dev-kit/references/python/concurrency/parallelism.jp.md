<!-- This file is a Japanese mirror of parallelism.md. When updating the English original, update this file too. -->
# concurrency/parallelism — 並列処理

threading / multiprocessing / subinterpreter の使い分け。

---

## GIL と前提

| 処理タイプ | GIL の影響 | 推奨 |
|---|---|---|
| **IO バウンド**（HTTP / ファイル / DB / sleep） | ほぼ無視できる | `asyncio` または `threading` |
| **CPU バウンド**（計算 / 画像処理 / 圧縮） | 1 プロセス内では並列にならない | `multiprocessing` or `subinterpreters` |

Python 3.13+ では `--disable-gil` ビルドで GIL を外せるが、依存ライブラリの対応が
追いつくまでは GIL 前提で設計する。

---

## 早見表

| やりたいこと | API | 備考 |
|---|---|---|
| 多数の HTTP 並列 | `asyncio` + httpx.AsyncClient | `concurrency/async.md` 参照 |
| 多数の同期 IO 並列（古い lib） | `concurrent.futures.ThreadPoolExecutor` | GIL は IO 待ちで解放される |
| 重い計算を CPU コア数だけ並列 | `concurrent.futures.ProcessPoolExecutor` | 引数 / 戻り値が pickle 可能であること |
| 既存 sync 関数を async から並列 | `asyncio.to_thread` | 軽量 |
| 数値計算を高速化 | NumPy / numba / cython | 真の並列が必要なら multiprocessing と組み合わせ |

---

## ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_sync(url: str) -> str:
    """同期 HTTP 取得（古い lib 想定）。"""
    import urllib.request
    return urllib.request.urlopen(url).read().decode()

def fetch_many(urls: list[str], *, max_workers: int = 10) -> list[str]:
    """N 並列で取得。"""
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(fetch_sync, urls))
```

async から呼ぶ場合は `asyncio.to_thread` で 1 関数ずつ:

```python
import asyncio

async def fetch_many_async(urls: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(asyncio.to_thread(fetch_sync, url)) for url in urls]
    return [t.result() for t in tasks]
```

---

## ProcessPoolExecutor

CPU バウンド処理を物理コアで並列実行する:

```python
from concurrent.futures import ProcessPoolExecutor
import os

def heavy_calc(n: int) -> int:
    """重い計算（純 Python）。"""
    total = 0
    for i in range(n):
        total += i * i
    return total

def parallel_calc(values: list[int]) -> list[int]:
    """CPU コア数だけ並列に走らせる。"""
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        return list(ex.map(heavy_calc, values))
```

**制約**:
- 引数 / 戻り値が `pickle` 可能であること（関数 / DTO / 基本型なら OK、ラムダや Closure は不可）
- プロセス起動コストがあるので、1 タスクが十分重くないと逆効果（目安: 100ms 以上）
- `if __name__ == "__main__":` ガードを忘れずに（Windows / macOS で必須）

```python
if __name__ == "__main__":
    results = parallel_calc([10**6, 10**7, 10**8])
```

---

## subprocess（外部コマンド実行）

```python
import subprocess

def run_ffmpeg(input_path: Path, output_path: Path) -> None:
    """ffmpeg を呼んで変換する。"""
    result = subprocess.run(
        ["ffmpeg", "-i", str(input_path), str(output_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    # result.stdout / result.stderr が使える
```

async 文脈なら `asyncio.create_subprocess_exec`:

```python
import asyncio

async def run_ffmpeg_async(input_path: Path, output_path: Path) -> None:
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-i", str(input_path), str(output_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {stderr.decode()}")
```

---

## subinterpreters（PEP 734、Python 3.13+）

3.13 で `interpreters` 標準モジュールが入り、プロセスより軽量な分離環境で並列実行できる。
ただし API は実験的、ライブラリ対応も限定的。**新規プロジェクトでは様子見**を推奨。
本当に必要になってから検討。

---

## 共有状態

- スレッド間: `threading.Lock`、`queue.Queue`、`threading.Event`
- プロセス間: `multiprocessing.Queue`、`multiprocessing.Manager`、`multiprocessing.shared_memory`

ただし、共有状態を持つほどバグも増えるので **避ける**。Producer / Consumer モデルでキューに流すのが基本。

---

## まとめ判断フロー

```
やりたい処理は CPU バウンド？
├── No (IO) → asyncio が第一候補。古い lib なら ThreadPool
└── Yes
    ├── 1 タスク 100ms 未満 → 並列化しない、または numpy/numba 等で内部高速化
    └── 1 タスク 100ms 以上 → ProcessPoolExecutor
```

---

## やってはいけないこと

```python
# ❌ asyncio で重い計算を直書き（イベントループが固まる）
async def bad() -> int:
    return sum(i*i for i in range(10**8))   # CPU バウンドを await なしで

# ✅ to_thread か ProcessPoolExecutor へ
async def good() -> int:
    return await asyncio.to_thread(heavy_calc, 10**8)

# ❌ ProcessPoolExecutor にラムダ / closure を渡す
ex.map(lambda x: x*2, values)   # pickle できない

# ❌ multiprocessing でグローバル変数を共有しようとする
counter = 0
def worker(): counter += 1   # 別プロセスの counter は別物
```

---

## 関連ファイル

- `concurrency/async.md` — IO バウンドの本命
- `performance/cheatsheet.md` — ボトルネック特定の手順
