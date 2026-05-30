<!-- This file is a Japanese mirror of comments.md. When updating the English original, update this file too. -->
# コメントルール

> このファイルは `comments.md` の日本語ミラーです。

dev-kit Next の `frontend/conventions/comments.md` と同じ思想で Python に適用する。

---

## 言語

コメントは **日本語** で書く:
- 関数 / 型 / DTO の説明（docstring）
- 引数・フィールドの説明（重要なもの）
- ブロックコメント（処理セクションのラベル）
- セクションマーカー
- 変更履歴コメント（PR 番号 + 意図）

識別子（変数名・関数名・型名）は英語のまま。

---

## 必須 / 推奨マトリクス

| 対象 | コメント要否 | 形式 |
|---|---|---|
| `__init__.py` で export する関数 / 型 | ✅ 必須 | 1 行 docstring |
| public な関数（`_` 始まりでない） | ✅ 必須 | 1 行 docstring（重要度に応じて複数行） |
| 内部関数（`_` 始まり） | ⚠️ 推奨 | docstring 任意、複雑なら必須 |
| Pydantic / dataclass の**設計上重要な**フィールド | ✅ 必須 | `Field(description=...)` または `# ` インラインコメント |
| 普通のフィールド（自明なもの） | ❌ 不要 | — |
| 関連 statement ブロック | ⚠️ 推奨 | `# ` 単行ラベル |
| **複数ステップを持つ関数の各ステップ**（レイヤー不問） | ✅ 必須 | `# ` 各ステップの意図（ブロックマーカーだけにしない） |
| **条件分岐**（レイヤー不問） | ✅ 必須 | `# ` 分岐ごとのラベル（条件の意味 + 何をするか） |
| 自明な 1 行 | ❌ 不要 | — |
| ログ出力のみの行（`logger.*`） | ❌ 不要 | — |
| 変更履歴（PR 番号 + 意図） | ✅ 許可 | `# PR{N}: {何を変えたか/なぜ}` |
| TODO / FIXME | ✅ 許可 | issue 番号必須（`# TODO(#123): ...`） |

AI と共同で書く前提なので、**多めに書く**。将来 AI が読むときに人間と同じ恩恵を受ける。

---

## パターン 1: 関数 docstring

公開関数 / 型には 1 行 docstring を必ず書く。

```python
def create_user(input: CreateUserInput, *, save: SaveUser) -> User:
    """ユーザーを新規作成し、永続化する。"""
    ...

def find_user_by_id(id: UserId, *, find: FindUser) -> User | None:
    """ユーザーを ID で検索する。見つからなければ None。"""
    ...
```

複数行が必要なら 1 行目に要約、空行、詳細:

```python
def calculate_score(user: User, items: list[Item]) -> int:
    """ユーザーの累計スコアを計算する。

    プレミアム会員は基本点 +20%、購入回数が 10 を超えた items は対象外。
    """
    ...
```

`@param` / `@returns` / `@type` のような JSDoc 型アノテーションは書かない。
型は signature が持つ。**目的だけ書く**。

---

## パターン 2: 設計上重要なフィールドの説明

「設計上重要」の判断基準（dev-kit Next と同じ）:
- 外部キー / ID 参照
- ステータス系 enum / Literal
- 業務的に意味のあるフラグ（公開 / アーカイブ / 削除等）
- 楽観ロックカラム
- 監査カラム（作成者・更新者・タイムスタンプ）
- 業務的に複雑な意味を持つフィールド

### Pydantic の場合

```python
from pydantic import BaseModel, Field
from typing import Literal

class CreateUserInput(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=0, le=150)
    is_public: bool = Field(
        default=False,
        description="公開フラグ。true なら全ユーザーから閲覧可能",
    )
    status: Literal["draft", "published", "archived"] = Field(
        default="draft",
        description="ステータス。draft=下書き、published=公開、archived=非表示",
    )
```

### dataclass の場合

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserInput:
    name: str
    age: int
    # 公開フラグ — true なら全ユーザーから閲覧可能
    is_public: bool = False
    # ステータス — draft=下書き、published=公開、archived=非表示
    status: str = "draft"
```

### TypedDict の場合

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: str
    name: str
    # オプションフィールド — 未指定なら年齢不明
    age: NotRequired[int]
```

---

## パターン 3: ブロックコメント（処理セクション）

長めの関数の中で、論理ブロックを `# ` 単行コメントでラベル付け。

```python
async def handle_chat(input: ChatInput, *, chat: AsyncChatFn) -> ChatOutput:
    """ユーザー入力を LLM に投げ、レスポンスを整形して返す。"""

    # 入力の前処理
    cleaned = _strip_control_chars(input.text)
    messages = _build_messages(cleaned, input.history)

    # LLM 呼び出し
    raw = await chat(messages)

    # 後処理（Markdown 除去 + 文字数制限）
    text = _strip_markdown(raw)
    return ChatOutput(text=text[:MAX_RESPONSE_LEN])
```

### マーカーだけでなく中身にもコメント

ブロックマーカーだけでは足りない。**各ステップが何をしてなぜそうするのか**、特に非自明な箇所に一言コメントを足す。これは**レイヤーに関係なく**適用する — ユースケースを束ねるサービス、機能内部のヘルパー、末端のユーティリティ、どれも同じように書く。「高レイヤーだから濃く」ではなく、コメントの量はコードの非自明さに従う。レイヤーで分けない。

下の例はたまたまサービス関数だが、内部ヘルパーやユーティリティもまったく同じように書く。

```python
async def handle_personal_chat(
    input: PersonalChatInput,
    *,
    classify: ClassifyIntent,
    chat: AsyncChatFn,
    save_log: SaveChatLog,
) -> PersonalChatOutput:
    """個人チャットを処理する。意図分類 → 応答生成 → ログ保存までを束ねる。"""

    logger.info("personal chat start: user=%s", input.user_id)

    # ユーザー発話の意図を分類し、後続の分岐に使う
    intent = await classify(input.text)

    # 意図ごとに応答の組み立て方を変える
    if intent == "question":
        # 質問: 履歴を文脈に含めて LLM に投げる
        messages = _build_messages(input.text, input.history)
        reply = await chat(messages)
    elif intent == "smalltalk":
        # 雑談: 履歴は使わず軽量プロンプトで短く返す（コスト削減）
        reply = await chat(_smalltalk_messages(input.text))
    else:
        # 未分類: LLM を呼ばず定型文でフォールバック
        reply = FALLBACK_REPLY

    # 応答を永続化（分析・再学習用）
    await save_log(user_id=input.user_id, text=input.text, reply=reply)

    return PersonalChatOutput(reply=reply, intent=intent)
```

`logger.info(...)` の行には**コメントを付けていない** — `logger` と書いてある時点で何をしているか自明だから。一方で `if` / `elif` / `else` の各分岐には、**条件の意味とその分岐で何をするか**を 1 行コメントで付けている。

### 条件分岐

条件で分岐するときは、各分岐に「何の条件か」「その中で何が起きるか」をラベル付けする。読み手がコメントだけで判断ツリーを追えるようにする。

```python
# 在庫が残っているか
if stock.remaining > 0:
    # あり: 通常購入フロー
    order = _place_order(stock, qty)
elif stock.restock_eta is not None:
    # 切れているが再入荷予定あり: 予約として受け付ける
    order = _reserve(stock, qty)
else:
    # 完全な在庫切れ: 購入不可エラー
    raise OutOfStockError(stock.id)
```

分岐が自明なとき（例: `if x is None: return`）だけ、分岐ごとのコメントを省略してよい。

---

## パターン 4: 変更履歴コメント

コードから意図が読み取れない変更を 1 行で記録。日本語、PR 番号付き。

```python
# PR123: 年齢上限フィールドを追加。要件 #45 対応。
age_upper: int | None = None

# PR101: 旧 calculate() を廃止し新仕様に統一。互換性のため null チェックを追加。
if value is None:
    return 0

# PR132: API ステータスを 200 → 204 に変更（フロントは互換）
return Response(status_code=204)
```

### 書くべきとき

- コードから消える意図（互換性 shim、業務上のレアケース対応）
- API / スキーマ変更で外部呼び出し側に影響があるもの
- 一時的に残してある移行期コード
- バグ修正で、根本原因がコード上では追えないもの

### 書かなくていいとき

- リネーム / フォーマット
- 振る舞いが変わらないリファクタ
- 単に「触った行」全部に記録するのは `git log` の役割

5 個以上の履歴コメントが溜まったらファイル先頭に `# History:` ブロックで集約するか、
CHANGELOG に切り出すことを検討する。

---

## パターン 5: TODO / FIXME

`TODO:` は未完了の作業。後で着手できるだけの文脈を含める。
**issue 番号必須**（プロジェクト管理と紐付けるため）。

```python
# TODO(#123): コメントテーブル作成後に有効化する
# pinned_comment_id: UserId | None = None

# TODO(PR133): 子供が複数いる場合の選択 UI を追加
child_id = children[0].id if children else None
```

`FIXME:` はマージ / リリース前に必ず直すべき既知バグ。

```python
# FIXME(#234): age_from が None のとき NaN になる
age_diff = age_to - age_from
```

---

## 書いてはいけないもの

```python
# ❌ コードを言い換えただけ
# user_id を取得する
user_id = user.id

# ❌ 自明な動作
# state を更新する
is_open = True

# ❌ ログ出力への説明（logger と書いてあれば自明）
# 処理開始をログに出す
logger.info("start")
```

```python
# ✅ 隠れた制約を説明する
# IME 入力中は Enter を無視する（変換確定キーと競合するため）
if event.key == "Enter" and not is_composing:
    handle_submit()

# ✅ 関数の目的
def select_family_quests(*, db: Db, family_id: FamilyId, page: int) -> list[Quest]:
    """家族 ID でクエストを絞り込み、ページネーションして返す。"""
    ...
```

---

## 制約まとめ

- 公開関数 / 型 / DTO には 1 行 docstring 必須
- Pydantic / dataclass の設計上重要なフィールドには説明必須
- 長い関数の論理ブロックは `# ` ラベル推奨
- **複数ステップの関数はマーカーだけでなく中身にもコメント** — 各ステップの意図を、レイヤーに関係なく書く
- **条件分岐**: 各分岐に「条件の意味 + 何をするか」をラベル付け、レイヤーに関係なく
- **ログ出力のみの行にはコメントを付けない** — `logger.*` は自明
- 変更履歴コメントは非自明な変更のみ、日本語 1 行、PR 番号付き
- TODO / FIXME は issue / PR 番号必須
- `@param` / `@returns` / `@type` は書かない（型ヒントに任せる）
- コードと同じことを繰り返さない
- `git log` が一次変更履歴

---

## 関連ファイル

- `core/naming.md` — 命名規約
- `core/type-hints.md` — 型ヒントの書き方
- `architecture/ts-style.md` — DTO 定義の実例
