<!-- This file is a Japanese mirror of design-principles.md. When updating the English original, update this file too. -->
# 設計原則の優先順位

コード追加・リファクタリングを判断するときの基本優先順位。

---

## 順位

1. **DRY (Don't Repeat Yourself)** — **最重視**
2. **SOLID** — 重視（特に `I` Interface Segregation と `L` Liskov）
3. **拡張性意識** — YAGNI は強制しない、先回り抽象化を許容

### DRY — 最重視

- 同じロジック・データ・構造を **2 箇所以上に書かない**
- 2 箇所目を書きそうになったら、まず共通化を検討
- ただし「3 箇所目以降のために」過剰に抽象化はしない（**3 度書いてから抽象化** の指針は `refactoring-judgement.md`）
- インライン重複（同じ計算・同じ if 連鎖・同じ dict キー列挙）は最優先で DRY 化対象

### SOLID — 重視

- **S (Single Responsibility)**: 1 関数 / 1 モジュールが複数の理由で変更されないように
- **O (Open/Closed)**: 拡張に開き、変更に閉じる（新 feature / 新 provider 追加のとき重要）
- **L (Liskov Substitution)**: Protocol で抽象化したら、実装は **構造的に等価** であること（戻り値の型 / 例外契約 / 副作用範囲）
- **I (Interface Segregation)**: 巨大な Protocol を作らない。用途別に小さく分ける（`AsyncChatFn` と `EmbedFn` を別 type で）
- **D (Dependency Inversion)**: 高レイヤは低レイヤを **関数の型エイリアス** で抽象化（dev-kit Python は関数の型でやる、`architecture/ts-style.md` / `architecture/dependencies.md`）

### 拡張性意識（YAGNI は強制しない）

- 「いずれ来そう」な拡張ポイントは **最初から関数の型で抽象化** しておく（後付けより安い）
- ただし「来るかわからない抽象化」を増やすのは控える（`@overload` / `Protocol` の量産は逆効果）
- 抽象化の閾値判断は `refactoring-judgement.md`

---

## クラスと関数の優先順位

dev-kit Python は **関数ファースト**（`architecture/ts-style.md`）。クラスは:
- DTO（`@dataclass` / `BaseModel`）
- ライブラリ要求（FastAPI Middleware、Pydantic BaseModel 継承、CLI Command）
- 長期保持のランタイム状態（接続プール、WebSocket セッション）

それ以外（サービス / Repository / Provider / Validator 等）は関数で書く。

---

## やってはいけないこと

```python
# ❌ 同じパース処理を 2 箇所に書く
def handle_a(raw: str) -> int:
    return int(raw.strip().lower().replace(",", ""))

def handle_b(raw: str) -> int:
    return int(raw.strip().lower().replace(",", ""))   # DRY 違反、_helpers.py へ

# ❌ 1 関数が複数の理由で変わる
def process_order(order: Order) -> None:
    validate(order)
    save_to_db(order)
    send_email(order)
    log_audit(order)
    update_metrics(order)
    # ↑ S 違反、責務を分割
```

---

## 関連ファイル

- `architecture/refactoring-judgement.md` — 共通化 / 抽象化 / 設定外出しの判断基準
- `architecture/ts-style.md` — 関数ファースト + 型エイリアスでの DI
- `architecture/dependencies.md` — 依存方向と DIP
