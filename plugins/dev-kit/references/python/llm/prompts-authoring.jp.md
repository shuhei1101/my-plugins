<!-- This file is a Japanese mirror of prompts-authoring.md. When updating the English original, update this file too. -->
# llm/prompts-authoring — プロンプトファイルの書き方と組み立て

> このファイルは `prompts-authoring.md` の日本語ミラーです。

プロンプトを **コード内に埋め込まない**。ファイル化し、**部品を細かく分割** して、index.yaml で組み立てる。
ローダー実装は別ファイル（`llm/prompts-loader.md`）。

---

## 配置: プロジェクトルート直下の `prompts/`

```
{project_root}/
├── pyproject.toml
├── prompts/                       # ← プロンプトファイルは src/ の外に置く
│   ├── index.yaml                 # 部品メタデータと組み立て定義の SoT
│   ├── characters/                # キャラごとの不変設定（任意）
│   ├── shared/                    # 横断的な部品（履歴・出力スキーマ・few-shot）
│   ├── modes/                     # ユースケースごとの部品
│   └── settings.yaml.sample       # 環境別パラメータ（任意）
├── src/{pkg}/
│   └── integrations/llm/prompts/  # ローダー実装（YAML 読み込み + Jinja2 + 部品結合）
└── tests/
```

### なぜルート直下か

- **プロンプトは「コード」より「設定 + 文芸物」** なので、ソースツリーから外す
- 配信者や非エンジニアでも編集できる（IDE で `src/` を意識せず）
- パッケージング時に同梱するか分離するか選べる（`include` で個別制御）
- ローダーは `src/{pkg}/integrations/llm/prompts/` 配下に置き、`prompts/` をプロジェクトルートからの相対 / `Path` で参照する

---

## 部品の粒度: H3 セクション単位で分割

**1 ファイル = 1 つの H3 セクション** が原則。理由:
- LLM プロンプトは「役割」「方針」「出力フォーマット」「入力例」「制約」… と多数の小ブロックの寄せ集め
- 大きな .md に詰めると **どの LLM がどのブロックを必要としているか** が見えない
- 微修正（1 ブロックだけ差し替え）で他 LLM への影響が見えなくなる
- フック注入と同じ思想 — **使わない情報をコンテキストに入れない**

### 標準ファイル構造

```markdown
### Notify Role

You are the AITuber, speaking a brief monologue right after finishing a task.
This is a notification voice for the completion of work...
```

- ファイル先頭は **`### {タイトル}`** から始める（H3）。タイトルは **ファイル本文が SoT**
- 本文はそのまま LLM に渡るので、Markdown フォーマットは「LLM が読める範囲」で
- 1 ファイル数行〜30 行程度を目安。長くなる場合は分割を検討

---

## 静的 vs 動的: `.md` と `.j2`

| 拡張子 | 用途 | キャッシュ |
|---|---|---|
| `*.md` | 静的部品。変数なし | プロンプトキャッシュ対象 |
| `*.j2` | Jinja2 テンプレート。`{{var}}` で埋め込み | リクエスト毎に変動 → キャッシュ対象外 |

```
prompts/modes/notify/
├── static/                          # キャッシュさせたい固定部分
│   ├── role.md                      # 役割定義（不変）
│   ├── policy_chat.md               # 方針（不変）
│   └── output_csv_format.md         # 出力フォーマット（不変）
└── dynamic/                         # リクエストごとに変わる部分
    └── situation.j2                 # 現在の状況（duration、project 等）
```

### 配置原則（プロンプトキャッシュとの整合）

`llm/cost-cache.md` に書いた **「固定値は上、動的値は下」** をディレクトリ構造で表現:

- 組み立て時は **`static/` → `dynamic/`** の順に積む
- そうすれば `static/` 全体が共通プレフィックスになり、プロンプトキャッシュが効く
- `dynamic/` のテンプレートを末尾に置けば、変数が変わっても上部はキャッシュヒット

---

## `index.yaml` で SoT 管理

部品の場所・種別・分類をすべて `prompts/index.yaml` に集約する。
**ハードコード禁止** — Python 側で `STATIC_PARTS = [...]` のようなパス一覧を持たない。

### 最小サンプル

```yaml
# prompts/index.yaml

# ----- 部品一覧 -----
parts:
  - path: modes/notify/static/role.md
    kind: static
    role: system
    category: role
  - path: modes/notify/static/policy_chat.md
    kind: static
    role: system
    category: policy
  - path: modes/notify/static/output_csv_format.md
    kind: static
    role: system
    category: output_format
  - path: modes/notify/dynamic/situation.j2
    kind: dynamic
    role: user
    category: situation

# ----- LLM ごとの組み立て定義 -----
llms:
  notify_chat:
    template_id: notify_chat
    includes:
      - modes/notify/static/role.md
      - modes/notify/static/policy_chat.md
      - modes/notify/static/output_csv_format.md
      - modes/notify/dynamic/situation.j2
```

### 何を書くか

| キー | 内容 |
|---|---|
| `parts[]` | 全部品の `path` + メタ（`kind`, `role`, `category`, 任意で `group` / `mirror_of` 等） |
| `llms[]` | 各 LLM 呼び出しが使う部品の `includes` リスト（順序が積む順） |
| `display` | UI に出す表示名（モード名 / カテゴリ名）の多言語ラベル（任意） |
| `legacy_aliases` | 旧パス → 新 ID のマッピング（リネーム時の後方互換、任意） |

### 並び順 = 積み順 = キャッシュ境界

`includes` の **上が先頭**、下が末尾。
**上ほど静的、下ほど動的** にして、上部がキャッシュヒットする並びにする。

---

## グループ化 (H2 ラッパー)

複数の部品を 1 つの H2 セクションでまとめたい場合（例: 「## キャラクター設定」配下に
personality / speaking_style / preferences を並べたい）:

```yaml
display:
  categories:
    character:
      h2_jp: キャラクター設定
      h2_en: Character Profile
    output_format:
      h2_jp: 出力
      h2_en: Output

parts:
  - path: characters/akane/static/personality.md
    category: character
  - path: characters/akane/static/speaking_style.md
    category: character
```

ローダーは同じ category の部品連続をまとめて `## キャラクター設定\n\n### personality...\n### speaking_style...` のように囲む。
詳細な合成ロジックは `llm/prompts-loader.md` 側。

---

## 部品の i18n / ミラー

同じ部品を日本語 / 英語両方持ちたい場合は **ファイル名サフィックス** で:

```
prompts/shared/response_generation/dynamic/
├── character_info.j2          # 英語版
└── character_info.jp.j2       # 日本語版
```

`index.yaml` の parts には両方を載せ、`mirror_of` キーで対を明示:

```yaml
parts:
  - path: shared/response_generation/dynamic/character_info.j2
    lang: en
  - path: shared/response_generation/dynamic/character_info.jp.j2
    lang: jp
    mirror_of: shared/response_generation/dynamic/character_info.j2
```

ローダーは `lang` パラメータで切り替え。

---

## 「組み立て」を変えやすくしておく

最終プロンプト = 部品の連結。**連結ロジックは外部設定で変えられる** ようにする:

- `llms.{id}.includes` の差し替えで A/B テスト
- 部品追加 → `parts[]` + 該当 LLM の `includes[]` に追記するだけ
- ハードコードした `STATIC_INSTRUCTIONS = "..."` は禁止（**新規部品追加が二重作業になる**）

---

## やってはいけないこと

```python
# ❌ Python コード内に長いプロンプトを直書き
SYSTEM = """あなたは...
（100 行）"""

# ❌ システムプロンプトに動的値を混入（キャッシュが切れる）
system = f"You are an assistant. Now: {now()}"

# ❌ includes リストを Python 側で組む
SYSTEM_PARTS = ["role", "policy", "output_format"]   # → index.yaml に書く

# ❌ 同じプロンプト本文をコピペで複数 LLM にハードコード
TASK_A_PROMPT = "..."
TASK_B_PROMPT = "..."   # 同じ部品を共有するなら parts + includes で
```

---

## 関連ファイル

- `llm/prompts-loader.md` — index.yaml を読み込んで部品を結合する実装
- `llm/cost-cache.md` — プロンプトキャッシュの設計考え方
