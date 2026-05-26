<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python コア規約 — py-kit（日本語ミラー）

> このファイルは `python-core.md` の日本語ミラーです。Claude Code には読み込まれません。

全 Python タスクで必ず読むベースライン規約。

---

## 命名規則

| 対象 | 規約 | 例 |
|---|---|---|
| モジュール / ファイル | `snake_case` | `user_repository.py` |
| クラス | `PascalCase` | `UserRepository` |
| 関数 / メソッド | `snake_case` | `find_by_id()` |
| 変数 | `snake_case` | `user_id` |
| 定数 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| プライベート | 先頭に `_` | `_internal_cache` |
| Protocol / インターフェース | `{Name}able`（推奨）・`I{Name}`・`Base{Name}` — プロジェクト内で1パターンに統一 | `Convertable`・`IConverter`・`BaseConverter` |
| 実装クラスファイル | `{実装名}_{name}.py` | `ffmpeg_converter.py` |

---

## コメントルール

**なぜ**を書く。**何をするか**は書かない（コードを読めばわかる）。

- 良い例：`# CP932 で bat ファイルをパースする — 日本語 UTF-8 バイトがリードバイトとして誤認され後続文字が消える`
- 悪い例：`# setup_logger を呼ぶ`

1行の短いコメントのみ。複数段落・シグネチャを言い換えるだけの docstring は禁止。

例外：スクリプトのモジュールレベル docstring（`python-scripts.md` 参照）。

---

## 型ヒント

関数の引数・戻り値・クラスフィールドの全箇所に付ける。裸の `Any` は禁止。

```python
from typing import Literal, Optional, Protocol, TypeVar
from collections.abc import Sequence

def process(items: Sequence[str], mode: Literal["fast", "slow"]) -> list[str]: ...
```

構造的インターフェースには `Protocol` を使う（新規コードでは `ABC` より推奨）：

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...
```

共有デフォルト実装が必要な場合のみ `ABC` を使う。

---

## 言語ルール

- **英語のみ**：全 `print()` およびロガー出力（bat ファイルが CP932 で日本語を文字化けさせるため）
- **日本語可**：コードコメント・`.env.sample` のコメント・GUI 表示文字列
