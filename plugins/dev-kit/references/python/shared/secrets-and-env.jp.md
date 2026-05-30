<!-- This file is a Japanese mirror of secrets-and-env.md. When updating the English original, update this file too. -->
# secrets-and-env — シークレット / 環境 / 構造 / アセットの分離

> このファイルは `secrets-and-env.md` の日本語ミラーです。

設定値の保管先を **シークレット / 個人環境 / 構造定義 / アセット / ランタイム状態** で明確に分離する。
**シークレットは絶対に `settings.yaml` やコードに書かない**。

---

## どこに何を書くか

| 種別 | 保管先 | git | 理由 |
|---|---|---|---|
| **シークレット**（API キー / OAuth トークン / DB パスワード） | `.env` | ❌ ignore | `settings.yaml` は worktree 共有・バックアップ混入のリスクあり、コミット事故も多い |
| **個人環境固有**（Windows パス / ローカルポート / 既定モデル名） | `config/settings.yaml` | ❌ ignore | 環境ごとに違うが秘匿性は低い |
| **構造定義**（スキーマ / 選択肢 / カテゴリ） | コード（`shared/constants.py` / `Literal` / `StrEnum`） | ✅ committed | 変更は PR で意図的に行う |
| **アセット定義**（プロンプト / メディア / カタログ） | `prompts/index.yaml` / `assets/{kind}/index.yaml` | ✅ committed | コード扱い（LLM 入力にもなる） |
| **ランタイム状態**（履歴・キャッシュ・セッション） | `data/` | ❌ ignore | アプリ実行で生成 |

---

## `.env` 運用

```
{project_root}/
├── .env              # 実値（gitignore）
└── .env.sample       # テンプレート（committed）
```

`.gitignore`:

```
.env
```

`.env.sample` は **必要な env キーとプレースホルダ値** を載せる。
新規開発者は `.env.sample` をコピーして `.env` を作る。

```bash
# .env.sample
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DB_PASSWORD=changeme
```

詳細な読み込み方は `shared/settings.md`（`pydantic_settings.BaseSettings`）。

---

## なぜシークレットを `settings.yaml` に書かないか

`settings.yaml` は以下のリスクがある:
- IDE 補完で「設定値」として目に入りやすく、コミット事故が起きやすい
- worktree 間で共有されることがある（hardlink / symbolic link）
- バックアップ / 同期ツール（OneDrive / iCloud）に混入する
- 過去スクショ / ログ / バグレポートに紛れ込む

**`.env` は秘密情報専用** として OS / IDE / git のいずれも「触らないもの」として認識されている。

---

## SecretStr の扱い

Python 側で `.env` を読むときは `SecretStr` でラップして、間違ってログに出ないようにする:

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: SecretStr
    db_password: SecretStr


settings = Settings()

# ログ
logger.info(f"key = {settings.openai_api_key}")
# → "key = SecretStr('**********')" になる（実値が出ない）

# 実値を取り出すのは外部 API 呼び出し直前のみ
chat = make_openai_chat(api_key=settings.openai_api_key.get_secret_value())
```

詳細は `shared/settings.md`。

---

## 環境変数の命名規約

- **大文字 + アンダースコア区切り**: `OPENAI_API_KEY`、`DB_PASSWORD`
- **プレフィックスでドメインを示す**: 外部サービス系は `{SERVICE}_{NAME}`（`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`）
- **ネスト構造**: `pydantic_settings` の `env_nested_delimiter="__"` を使うと `DB__HOST` → `Settings.db.host` にマップできる

```python
class DatabaseSettings(BaseModel):
    host: str
    port: int

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")
    db: DatabaseSettings
```

```
DB__HOST=localhost
DB__PORT=5432
```

---

## YAML を SoT として使う場合（任意）

新規ドメインのデータ管理に YAML を使うなら、`index.yaml` + `settings.yaml` の **2 段構成** を推奨:

| ファイル | 役割 | git |
|---|---|---|
| `{feature}/index.yaml` | **キー本体** — 環境非依存、構造定義、一覧性が要るもの | ✅ committed |
| `{feature}/settings.yaml` | 付随メタデータ — 画面から更新する / 環境別 / 個人差 | ❌ ignore |
| `{feature}/settings.yaml.sample` | `settings.yaml` の committed テンプレート | ✅ committed |

どっちに書くかの判断:
- **ユーザーが画面ポチポチで変える** → `settings.yaml`
- **ファイル追加と同時に増える本質的なキー** → `index.yaml`
- **git で全員揃ってほしい値** → `index.yaml` または `settings.yaml.sample`

---

## やってはいけないこと

```python
# ❌ シークレットを settings.yaml に書く
# config/settings.yaml
# openai_api_key: sk-xxx   ← 絶対 NG、.env に移す

# ❌ シークレットをコードにハードコード
OPENAI_API_KEY = "sk-..."   # 絶対 NG

# ❌ os.environ 直読みで型検証なし
import os
key = os.environ["OPENAI_API_KEY"]   # → pydantic_settings 使う

# ❌ .env をコミット
git add .env   # 絶対 NG

# ❌ SecretStr を str() でログ出力（マスクされずに出る場合あり）
logger.info(f"key = {str(settings.api_key)}")   # → settings.api_key（SecretStr のまま）
```

---

## 関連ファイル

- `shared/settings.md` — `pydantic_settings` の使い方
- `shared/constants.md` — 計算済み定数の置き場
- `architecture/refactoring-judgement.md` — 設定外出し判断
- `dev-kit:yaml`（外部） — index.yaml / settings.yaml の運用全般
