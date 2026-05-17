# SKILL.jp.md — py-kit:py-new-project（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: py-kit:py-new-project
**トリガー**: Python プロジェクトをゼロから作成する依頼時。
「新しい Python プロジェクト作って」「土台から作りたい」「パッケージ作って」など。
簡易スクリプトには使わない → `py-kit:py-script` を使う。

---

# py-kit:py-new-project — 新規 Python プロジェクト作成

DDD レイヤー構造・DI 設計・ルールファイル・テスト雛形を含む本格 Python プロジェクトを作成する。

---

## 作業内容

### ステップ1: 規約を読み込む

共通 Python 規約をすべて読み込む：

```
{plugin_root}/references/python-standards.md
```

特に注目するセクション：**プロジェクトフォルダ構成**・**DDD**・**SOLID**・**拡張性重視設計**・**依存性逆転**・**Pydantic の境界**・**ロガー仕様**・**テスト方針**・**bat ランチャーテンプレート**。

→ ステップ2へ

---

### ステップ2: 要件ヒアリング

#### 処理内容

1. プロジェクト名とパッケージ名（`snake_case`）を確認。
2. ドメインを特定：このプロジェクトが解決する実世界の問題は何か？
3. 主要ユースケースを列挙（3〜5個の動詞：「ユーザーが注文を作成する」など）。
4. 外部依存を特定：データベース・API・ファイルシステム・メッセージキュー。
5. インターフェース種別を確認：CLI / FastAPI / tkinter GUI / バックグラウンドワーカー。
6. 環境変数の要件を確認。

→ ステップ3へ

---

### ステップ3: DDD レイヤー設計

#### 処理内容

1. ユースケースを **Application Service** にマッピング（ユースケースグループごとに1クラス）。
2. **エンティティ**（ID あり・ミュータブル）と**値オブジェクト**（イミュータブル・値で等値判定）を特定。
3. **集約ルート**とその不変条件を定義。
4. `domain/repositories/` に **Repository Protocol** を定義（集約ルートごとに1つ）。
5. 複数エンティティにまたがるロジックを **ドメインサービス** として特定。
6. **Infrastructure** 実装の計画：どの Repository Protocol にどの具象クラスを充てるか。
7. コード生成前にユーザーへレイヤー図を提示して確認を得る。

→ ステップ4へ

---

### ステップ4: プロジェクトスキャフォールド生成

#### 処理内容

1. 規約のフォルダ構成に従ってディレクトリ構造を作成。
2. Python `>= 3.11`・依存ライブラリは `~=` で指定した `pyproject.toml` を作成。
3. `.gitignore` を作成（`.env`・`__pycache__/`・`*.pyc`・`venv/`・`.venv/`・`log/`・`cache/` を含む）。
4. `.env.sample` を作成（全環境変数キーをプレースホルダーで記述）。
5. `setup/setup_venv.bat` を作成（ASCII のみ・venv 作成 + 依存インストール一本化）。
6. `activate.bat` を作成。
7. 空フォルダ（`log/` など）に `.gitkeep` を置く。
8. 計画した全モジュールのスタブファイルを作成（正しいインポートと型スタブのみ）。
9. ロガー仕様に従って `logger.py` を作成。
10. `PROJECT_ROOT` と `LOG_DIR` を定義した `constants.py` を作成。

→ ステップ5へ

---

### ステップ5: 依存性注入の配線

#### 処理内容

1. 全リポジトリ・サービスインターフェースの `Protocol` 定義を作成。
2. コンポジションルート（`main.py` or `container.py`）で全具象実装をインスタンス化してインジェクト。
3. ドメイン層・アプリケーション層は具象クラスを直接インポートしないことを確認。
4. 規約に従って Strategy / Factory / Decorator パターンを適切に適用。

→ ステップ6へ

---

### ステップ6: ルール展開

#### 処理内容

1. `{plugin_root}/rules/class-structure.md` テンプレートを使用してプロジェクトの `.claude/rules/class-structure.md` を作成。
2. `{plugin_root}/rules/config-source-link.md` テンプレートを使用して `.claude/rules/config-source-link.md` を作成。
3. `{plugin_root}/rules/source-test-link.md` テンプレートを使用して `.claude/rules/source-test-link.md` を作成。
4. `.claude/rules-jp/` 配下に各ルールの日本語ミラーを作成。
5. コミット：`git add .claude/rules/ .claude/rules-jp/ && git commit -m "chore: add py-kit rules"`。

→ ステップ7へ

---

### ステップ7: テスト雛形の作成

#### 処理内容

1. 共有 pytest フィクスチャを含む `tests/conftest.py` を作成。
2. 環境変数モッキングヘルパー `tests/mocks/mock_env.py` を作成。
3. 外部 API / DB クライアントのスタブ `tests/mocks/mock_externals.py` を作成。
4. 計画した各ユースケースに対応する `tests/{feature}/test_{feature}.py` スタブを作成。
5. テストは外部 I/O 境界のみモック — 個々のメソッドの単体テストは書かない。

→ 完了

---

## 参考資料

`{plugin_root}/references/python-standards.md`：
- プロジェクトフォルダ構成
- DDD（ドメイン駆動設計）
- SOLID 原則
- 拡張性重視の設計
- 依存性逆転・DI
- Pydantic の境界
- ロガー仕様
- テスト方針
- bat ランチャーテンプレート
- 命名規則
- 言語ルール
