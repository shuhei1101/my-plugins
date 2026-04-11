# Mermaid リファレンス（v11.14.0）

図の作成時に参照する Mermaid 構文リファレンス。

---

## 目次

1. [共通ルール](#共通ルール)
2. [フローチャート](#フローチャート)
3. [クラス図](#クラス図)
4. [シーケンス図](#シーケンス図)
5. [ユースケース図（flowchartで代替）](#ユースケース図)
6. [ER図](#er図)

---

## 共通ルール

### コメント
```
%% これはコメント（全図種共通）
A --> B  %% インラインコメントも可能
```

### 方向指定
- `TD` / `TB`: 上から下（Top-Down）— フロー図・クラス図のデフォルト
- `LR`: 左から右 — ユースケース図・横長の図
- `BT`: 下から上
- `RL`: 右から左

### ノート（図種により構文が異なる）
- クラス図: `note "テキスト"` / `note for ClassName "テキスト"`
- シーケンス図: `Note right of Actor: テキスト` / `Note over A,B: テキスト`

---

## フローチャート

### 基本構文
```mermaid
flowchart TD
    %% 開始
    A([開始]) --> B{条件分岐}
    
    %% 分岐
    B -->|Yes| C[処理A]
    B -->|No| D[処理B]
    
    %% 終了
    C --> E([終了])
    D --> E
```

### ノード形状
```
A[四角形]         B(角丸)           C([スタジアム型])
D[[サブルーチン]]  E[(データベース)]   F((円形))
G{ひし形}         H{{六角形}}        I[/平行四辺形/]
```

### リンク種類
```
A --> B          %% 矢印
A --- B          %% 線のみ
A -.-> B         %% 点線矢印
A ==> B          %% 太線矢印
A ~~~ B          %% 不可視リンク
A -->|テキスト| B %% ラベル付き矢印
```

### サブグラフ
```mermaid
flowchart LR
    subgraph グループ名 ["表示名"]
        direction TB
        A --> B
    end
```

### スタイル
```
classDef highlight fill:#f9f,stroke:#333,stroke-width:2px;
class nodeA highlight;
A:::highlight --> B   %% インラインでクラス適用
```

---

## クラス図

### 基本構文
```mermaid
classDiagram
    direction TB
    
    %% クラス定義
    class Animal {
        <<abstract>>
        +String name
        -int age
        +makeSound()*
        +sleep()$
    }
    
    %% 関係
    Animal <|-- Dog : 継承
    Animal <|-- Cat : 継承
    
    %% ノート
    note for Animal "基底クラス"
```

### アクセス修飾子
- `+` Public
- `-` Private
- `#` Protected
- `~` Package/Internal

### メソッド修飾子
- `*` 抽象メソッド（例: `draw()*`）
- `$` 静的メソッド（例: `getInstance()$`）

### 関係の種類
```
A <|-- B    %% 継承（Inheritance）
A *-- B     %% コンポジション（Composition）
A o-- B     %% 集約（Aggregation）
A --> B     %% 関連（Association）
A ..> B     %% 依存（Dependency）
A ..|> B    %% 実現（Realization）
```

### 多重度
```
ClassA "1" --> "0..*" ClassB : has
```

### アノテーション
```
class Shape {
    <<interface>>
}
class Color {
    <<enumeration>>
    RED
    BLUE
}
```

### 名前空間
```
namespace BaseShapes {
    class Triangle
    class Rectangle
}
```

### ジェネリクス
```
class List~T~ {
    +add(T item)
    +get(int index) T
}
```

---

## シーケンス図

### 基本構文
```mermaid
sequenceDiagram
    %% 参加者定義
    participant C as Client
    participant S as Server
    participant DB as Database
    
    %% メッセージ
    C ->> S: リクエスト
    activate S
    S ->> DB: クエリ
    DB -->> S: 結果
    S -->> C: レスポンス
    deactivate S
    
    %% ノート
    Note over C,S: 通信フロー
```

### 矢印の種類
```
A ->> B     %% 実線 + 矢印（同期）
A -->> B    %% 点線 + 矢印（応答）
A -x B      %% 実線 + ×（失敗/ロスト）
A -) B      %% 実線 + 開矢印（非同期）
```

### アクティベーション
```
A ->>+ B: リクエスト    %% + でアクティベート
B -->>- A: レスポンス   %% - でディアクティベート
```

### 制御構造
```
%% ループ
loop 毎分
    A ->> B: ハートビート
end

%% 条件分岐
alt 正常
    A ->> B: 成功
else エラー
    A ->> B: 失敗
end

%% オプション
opt 追加処理
    A ->> B: 処理
end

%% 並列
par アクション1
    A ->> B: Hello
and アクション2
    A ->> C: Hello
end
```

### 背景ハイライト
```
rect rgb(200, 255, 200)
    A ->> B: ハイライト区間
end
```

### 番号付け
```
autonumber
```

### 参加者のグループ化
```
box Aqua "グループ名"
    participant A
    participant B
end
```

---

## ユースケース図

Mermaidはユースケース図をネイティブサポートしていないため、flowchartで代替する。

### 代替構文
```mermaid
flowchart LR
    %% アクター定義
    User([ユーザー])
    Admin([管理者])
    
    %% システム境界
    subgraph System ["システム名"]
        UC1((ログイン))
        UC2((ダッシュボード閲覧))
        UC3((ユーザー管理))
    end
    
    %% アクターとユースケースの関係
    User --> UC1
    User --> UC2
    Admin --> UC1
    Admin --> UC3
    
    %% include/extend関係
    UC3 -.->|"<<include>>"| UC1
    UC2 -.->|"<<extend>>"| UC3
```

### ルール
- アクター: スタジアム型 `([名前])` で表現
- ユースケース: 二重丸 `((名前))` で表現
- システム境界: `subgraph` で表現
- include/extend: 点線矢印 `-.->` + ラベルで表現

---

## ER図

### 基本構文
```mermaid
erDiagram
    %% エンティティと属性
    USER {
        int id PK "ユーザーID"
        string name "名前"
        string email UK "メールアドレス"
        datetime created_at "作成日時"
    }
    
    POST {
        int id PK "投稿ID"
        int user_id FK "投稿者ID"
        string title "タイトル"
        text content "内容"
    }
    
    %% リレーション
    USER ||--o{ POST : "投稿する"
```

### リレーションの種類
```
||--||    %% 1対1
||--o{    %% 1対多
}o--o{    %% 多対多
||--o|    %% 1対0or1
```

### リレーション記号の意味
- `||` : ちょうど1つ（必須）
- `o|` : 0または1つ（任意）
- `}o` : 0以上（任意、複数可）
- `}|` : 1以上（必須、複数可）

### 属性のキー表記
- `PK` : 主キー
- `FK` : 外部キー
- `UK` : ユニークキー

---

## フォルダ構成図（プレーンテキスト）

Mermaidではなくプレーンテキストで作成する。

### 書式ルール
```plaintext
/project-name
├── src/                # ソースコード
│   ├── index.ts        # エントリポイント
│   ├── components/     # UIコンポーネント
│   │   ├── Header.tsx  # ヘッダー
│   │   ├── Footer.tsx  # フッター
│   │   └── ...         # その他のコンポーネント
│   └── utils/          # ユーティリティ
│       └── helpers.ts  # ヘルパー関数
├── tests/              # テスト
│   └── ...             # テストファイル
├── package.json        # パッケージ設定
└── README.md           # プロジェクト説明
```

### ルール
- ツリー罫線: `├──`（途中）、`└──`（最後）、`│`（縦線）
- コメント: `#` の後にスペースを入れて記載
- 省略: 重要でないファイルは `...` で省略（# コメントで省略内容を説明）
- ディレクトリ: 末尾に `/` を付ける
- 省略判断基準:
  - **残す**: 設定ファイル、エントリポイント、主要モジュール、README
  - **省略対象**: 生成物（dist/, build/）、キャッシュ（node_modules/, __pycache__/）、ボイラープレート、テストの個別ファイル
