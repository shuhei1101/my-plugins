<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->
# SKILL.jp.md — dev-kit:py-project（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: dev-kit:py-project
**トリガー**: Python プロジェクトに関する作業全般。
新規プロジェクトをゼロから作る場合（機能フォルダ型レイアウト・関数ファースト設計・テスト雛形を生成）と、
既存プロジェクトへの作業（レビュー・機能追加・リファクタ・バグ修正）の両方をカバーする。
「新しい Python プロジェクト作って」「土台から作りたい」「このコード見て」「機能追加して」
「リファクタして」「バグ直して」「コードレビューして」など。
簡易な単発スクリプトには使わない → `dev-kit:py-script` を使う。

---

# dev-kit:py-project — Python プロジェクト（新規 or 既存）

dev-kit Python の方針（機能フォルダ型レイアウト + TypeScript 風 + 関数ファースト）で
Python プロジェクトを扱う。

---

## タスク

### ステップ1: 規約を読み込む

まず references のインデックスを読む:

```
{plugin_root}/references/python/index.yaml
```

スキルファイルの 2 階層上がプラグインルート（例: `Base directory: .../skills/py-project` → プラグインルートは `.../dev-kit/`）。

`index.yaml` の `references:` リストに全 reference のパスと 1 行説明が、
`{plugin_root}/references/python/injection_rules.yaml` の `rules:` で「どの編集対象パスにどの reference を割り当てるか」が定義されている。

このスキルで常に読むべきもの:
- `{plugin_root}/references/python/core/命名規則.md`
- `{plugin_root}/references/python/core/コメント.md`
- `{plugin_root}/references/python/core/型ヒント.md`
- `{plugin_root}/references/python/core/言語ルール.md`
- `{plugin_root}/references/python/core/スタイル.md`
- `{plugin_root}/references/python/architecture/レイアウト.md`
- `{plugin_root}/references/python/architecture/TypeScriptスタイル適用.md`
- `{plugin_root}/references/python/architecture/コンポジションルート.md`
- `{plugin_root}/references/python/architecture/依存関係管理.md`

タスクに応じて以下も:
- 新規プロジェクト → `testing/strategy.md`, `packaging/pyproject.md`, `packaging/dependencies.md`
- FastAPI 使用 → `fastapi/app.md`, `fastapi/routes.md`, `fastapi/schemas.md`
- LLM 使用 → `llm/providers.md`, `llm/exceptions-retry.md`（必要なら `llm/instructor.md`, `llm/prompts-authoring.md`, `llm/prompts-loader.md`）

→ ステップ2へ

---

### ステップ2: モードを判定する（新規 vs 既存）

#### 処理

ユーザーが新規プロジェクトを作りたいのか、既存プロジェクトへの作業をしたいのかを判定する:

| シグナル | モード |
|---|---|
| 「新規」「create a new project」「土台から作りたい」・プロジェクトファイルなし | **新規** → ステップ3へ |
| 「このコード見て」「機能追加」「リファクタ」「レビュー」・プロジェクトが既存 | **既存** → ステップ8へ |

判断が難しい場合はユーザーに確認する。

---

## 新規プロジェクト（ステップ3〜7）

### ステップ3: 要件収集

1. プロジェクト名・パッケージ名（`snake_case`）を確認する
2. プロジェクトの目的と呼び出し元を確認する
3. 主要ユースケース（feature）を 3〜5 個列挙する（動詞ベース）
4. 外部依存（LLM・TTS・OBS・HTTP API 等）を特定する
   - 注: DB は基本扱わない方針。永続化が必要なら別途相談
5. インターフェース種別（CLI / FastAPI / GUI / バックグラウンドワーカー）を確認する
6. 環境変数の要件を確認する

→ ステップ4へ

---

### ステップ4: 機能フォルダ設計

`architecture/layout.md` の規約に従って:

1. **必須フォルダ**: `shared/` + `main.py`
2. **任意フォルダ**: 必要なものだけ作る
   - `features/` — ビジネス機能（ユースケースごと）
   - `integrations/` — 外部サービス（LLM、TTS 等）
   - `runtime/` — 実行時インフラ（queue 等。AITuber 規模で）
   - `server/` — FastAPI を使うなら
3. **各 feature の内部構成**: `types.py` + `service.py` を最小として、必要なら `query.py` / `route.py` / `client.py` / `prompts/` を足す
4. **設計をユーザーに提示** して確認を得る

→ ステップ5へ

---

### ステップ5: プロジェクト雛形を生成する

1. ディレクトリ構造を作成（`src/{pkg}/...`、`tests/`、`log/`、`.gitkeep` で空フォルダ確保）
2. `pyproject.toml` 作成（`packaging/pyproject.md` の完全サンプル参照、`requires-python = ">=3.12"`）
3. `.gitignore` 作成（`.env`・`__pycache__/`・`.venv/`・`log/`・`dist/` を含む）
4. `.env.sample` 作成（必要な env キーとプレースホルダ値）
5. `.python-version` 作成（`3.12` 固定）
6. `src/{pkg}/shared/`:
   - `logger.py`（`shared/logger.md` のテンプレ）
   - `settings.py`（`shared/settings.md` のテンプレ）
   - `errors.py`（`shared/errors.md` の例外階層）
   - `types.py`（共通型エイリアス）
   - `constants.py`（計算済みパス）
7. 各 feature のスタブ:
   - `types.py`（DTO + 型エイリアス）
   - `service.py`（関数 + 簡単なロジック）
   - 必要なら `query.py` / `route.py`
8. `src/{pkg}/main.py`（`build_handlers(settings) -> Handlers` パターン）
9. Windows ランチャーが必要なら `setup/setup_venv.bat` + `run.bat`（`scripts/launchers-windows.md`）

→ ステップ6へ

---

### ステップ6: 関数の配線

1. 全外部依存を **関数の型エイリアス** で抽象化する（`architecture/ts-style.md`）
2. `main.py` の `build_handlers(settings)` で `functools.partial` を使って配線する
3. 戻り値は `Handlers` dataclass で型安全に保持
4. 「クラスベース DI コンテナ」「Repository クラス」は **作らない**
5. FastAPI を使う場合は `server/app.py` で lifespan → `app.state.handlers = build_handlers(settings)`

→ ステップ7へ

---

### ステップ7: テスト雛形を作成する

`testing/strategy.md` の方針に従う:

1. `tests/conftest.py`（共通 fixture: test_settings, freeze_time 等）
2. `tests/{feature}/test_{usecase}.py` のスタブ
3. **単体テストは作らない**。結合テストのみ書く
4. 外部依存（LLM 等）は Mock 関数で注入（`testing/mocks.md`）
5. スモークテストは `tests/smoke/` 配下に隔離し、`--run-smoke` フラグでガード（AI 自動実行禁止）

→ 完了（新規プロジェクトフロー終了）

---

## 既存プロジェクト（ステップ8〜12）

### ステップ8: プロジェクト構造を把握する

1. トップレベルのディレクトリ一覧を読む
2. レイアウトを特定する（機能フォルダ型 / 純 DDD / その他）
3. `pyproject.toml` を読む（依存関係と Python バージョン）
4. メインエントリーポイント（`main.py` / `__main__.py` / `server/app.py`）と既存テストを特定する
5. `.env.sample` / `.python-version` を確認

→ ステップ9へ

---

### ステップ9: 品質チェック

新方針の観点でチェック:

1. **命名**: `core/naming.md` 通りか（snake_case 関数、UpperCamel 型）
2. **コメント**: `core/comments.md` の必須項目（exported 関数の docstring、設計上重要フィールドの description）
3. **型ヒント**: PEP 695 で書かれているか、`Any` の濫用がないか
4. **関数ファースト**: クラスが過剰に使われていないか（DTO / ライブラリ要求以外でクラスが出ていないか）
5. **依存方向**: `shared` ← `integrations` ← `features/server` が守られているか
6. **DI**: 外部依存が関数の型エイリアスで注入されているか
7. **例外**: `AppError` 階層が使われているか、vendor 例外がラップされているか
8. **テスト**: 結合テスト中心で書かれているか、スモークテストが分離されているか
9. レビューのみの依頼ならここで報告して終了

→ 実装が必要な場合はステップ10へ

---

### ステップ10: 変更を実装する

1. タスク（機能追加・リファクタ・バグ修正）を実施する
2. 編集対象ファイルパスに対する `injection_rules.yaml` の `rules` を確認し、該当 reference を読む（自動注入フックが走るなら結果を待ってもよい）
3. 規約に従って実装する:
   - 振る舞いは関数で書く（クラスは DTO / ライブラリ要求のみ）
   - 外部依存は関数の型エイリアスで注入
   - 型ヒントを全箇所付ける
   - `print` / 英語メッセージ / 日本語コメント
4. タスク要件を超えた抽象化を加えない（YAGNI）

→ ステップ11へ

---

### ステップ11: 同期チェック

変更したファイルと連動して更新すべきものを確認:

| 変更箇所 | 同時更新すべきもの |
|---|---|
| `features/{feature}/types.py` の DTO | 対応する `schemas.py`（FastAPI 使用時） |
| `shared/errors.py` の例外追加 | `server/error_handlers.py` のマッピング |
| `pyproject.toml` の依存 | `uv.lock`（`uv sync` で更新） |
| feature 追加 | `main.py` の `build_handlers` で配線 + `Handlers` dataclass に追加 |
| FastAPI route 追加 | `server/app.py` の `include_router` |

→ ステップ12へ

---

### ステップ12: テストを更新する

1. 変更したソースに対応する結合テスト（`tests/{feature}/test_{usecase}.py`）を更新する
2. 外部依存は Mock 関数で注入（`testing/mocks.md`）
3. `uv run pytest tests/ --ignore=tests/smoke/` でテストが通ることを確認する
4. スモークテストは **走らせない**（ユーザー手動実行のみ）

→ 完了（既存プロジェクトフロー終了）

---

## 参考資料

詳細は `{plugin_root}/references/python/index.yaml` を参照。

このスキルが扱う代表的な reference:
- `core/*` — 言語ルール
- `architecture/*` — レイアウトと関数配線
- `shared/*` — 横断インフラ
- `testing/*` — 結合テスト方針
- `packaging/*` — pyproject.toml と uv
- `fastapi/*` — FastAPI 使用時
- `llm/*` — LLM 使用時
