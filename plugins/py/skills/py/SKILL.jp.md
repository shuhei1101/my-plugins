# SKILL.jp.md — py スキル（日本語訳）

> このファイルは `SKILL.md` の日本語翻訳です。Claude Code には自動読み込みされません。内容を確認するための参照用ファイルです。
> 変更を加える場合は、まずこのファイルを更新し、その後 `SKILL.md`（本体）にも同じ変更を反映してください。

---

**スキル名**: py  
**トリガー**: Python コードの作成・レビュー・修正、`.py` ファイルの編集、`.bat` ランチャーの作成、`pyproject.toml` の設定、新規 Python プロジェクトの立ち上げなど、Python に関わるあらゆる作業で自動適用される

---

# py — Python プロジェクトコーディング規約

## 設計方針

各ツールは **完全に独立したパッケージ**（別リポジトリ・別プロジェクト）として作る。ツール間で連携が必要な場合は、設定ファイルや環境変数で他ツールのパスを指定する — プロセス内での共有や自動ダウンロードはしない。

---

## フォルダ構成

```
{パッケージ名}/
├── {package_name}/
│   ├── {機能サブフォルダ}/    # 機能ごとに分割
│   ├── __init__.py
│   ├── __main__.py             # python -m {package_name} のエントリーポイント
│   ├── config.py
│   ├── main.py                 # 引数処理と起動分岐のみ（高レベル）
│   ├── gui.py                  # tkinter GUI
│   ├── cli.py                  # argparse 処理
│   ├── logger.py               # ロガー初期化
│   ├── exceptions.py           # カスタム例外クラス
│   ├── constants.py            # 定数（LOG_DIR, PROJECT_ROOT など）
│   └── utils.py または common/ # 共通ユーティリティ
├── gui.bat                     # venv 自動有効化付き
├── {モード}.bat                # モードごとに1ファイル、venv 自動有効化付き
├── setup/
│   ├── setup_venv.bat          # venv 作成 + 依存ライブラリインストールまで一括
│   └── install_{ツール}.bat    # 自動インストールできない外部ツール用
├── docs/
│   └── install_{ツール}.md     # 手動インストール手順（README からリンク）
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {機能名}/
│       ├── conftest.py
│       └── test_{機能名}.py
├── venv/                       # .gitignore 対象 — コミットしない
├── resources/                  # GUI アセット
├── log/                        # .gitkeep
├── input/                      # .gitkeep（任意）
├── output/                     # .gitkeep（任意）
├── cache/                      # .gitkeep（任意）
├── activate.bat
├── .env.sample
├── .gitignore
├── README.md
└── pyproject.toml
```

**注意点：**
- すべての `.bat` ファイルはプロジェクトルート直下に置く — `bat/` サブフォルダは作らない
- 空フォルダ（`log/`, `input/`, `output/`, `cache/`）には `.gitkeep` を置く — 中に README.md は不要
- `main.py` は引数処理と起動ルーティングのみ — 低レベルロジックは専用モジュールへ

---

## 設定（Config）

- `config.py` と `.env` / `.env.sample` を用意する
- `config.py`：上部でデフォルト値を定義し、下部で `.env` を読み込んで上書き（env が優先）
- 優先順位：環境変数（初期ロード）→ CLI 引数で上書き
- 外部ライブラリの設定は可能な限り環境変数で変更できるようにする
- `.env` が存在しない場合：`.env.sample` を自動コピーして `.env` を作成（値は空）

---

## 起動方法

- 引数なし + bat 実行 → GUI 起動
- 引数あり → CLI モード
- `--help` / `-h` → ヘルプ表示
- 複数モードがある場合 → モードごとに bat ファイルを用意
- `main.py` はルーティングのみ。低レベル処理は専用モジュールに分離

---

## GUI（tkinter）

- tkinter でシンプルな GUI を作成
- 実行ボタン：青色
- 設定ボタンを配置 → クリックでモーダル設定画面を開く
- 設定画面：全設定項目を GUI から変更可能。変更内容は `.env` ファイルに保存
- 再起動が必要な設定：赤字で「再起動後に適用されます」と表示
- GUI レイアウト：プロジェクトごとに AI が 3 案提示 → ユーザーが選択

---

## コーディングスタイル

- `typing` を厳格に使用：`Literal`、`Union`、`Optional`、ジェネリクス — TypeScript の型定義を参考に
- docstring は reStructuredText 形式（`:param:`、`:return:`、`:raises:`）
- コメント：複雑なロジック・深いネスト・非自明な式・珍しいライブラリの使用箇所に適宜追加
- リーダブルコードを意識：意図を明確にするための中間変数を積極的に使う
- デザインパターンを適材適所で適用（Template、Strategy など）— 過度な抽象化は避ける

---

## Pydantic（API / IO 境界に使用）

実行時バリデーションが重要なシステム境界では、型ヒントだけでなく Pydantic モデルを使う：

**Pydantic を使う箇所：**
- 外部 API へのリクエスト・レスポンス
- LLM への入力（構造化プロンプト）と出力（Instructor 経由）
- 設定ファイルの読み込み（YAML / JSON）
- ファイル間で受け渡すデータ（CSV / JSONL のレコード）
- ユーザー入力のパース
- スレッド / プロセス間で受け渡すイベントデータ

**型ヒントのみで十分な箇所：**
- 単一関数内で完結する内部ロジックの引数・戻り値
- 関数内に閉じた `dict` / `list` の型表現

```python
from pydantic import BaseModel, Field
from typing import Optional

class APIRequest(BaseModel):
    user_id: str
    query: str
    max_results: int = Field(default=10, ge=1, le=100)

class APIResponse(BaseModel):
    status: str
    results: list[dict]
    error: Optional[str] = None

def call_api(req: APIRequest) -> APIResponse:
    response = requests.post(URL, json=req.model_dump())
    return APIResponse(**response.json())
```

---

## 言語使用ルール

**英語のみ**（bat ファイルで日本語がバグるため）：
- すべての `print()` 文
- すべての `logger` 出力（`logger.info()`、`logger.error()` など）

**日本語を使う箇所：**
- コードコメント（docstring・インラインコメント）
- `.env.sample` のコメント
- GUI の表示文字列（tkinter の UI テキスト）

```python
# ファイル存在チェックを行う
def check_file_exists(file_path: Path) -> bool:
    """
    ファイルが存在するかチェックする。

    :param file_path: チェック対象のファイルパス
    :return: 存在する場合 True
    """
    if not file_path.is_file():
        logger.error(f"File not found: {file_path}")   # 英語
        return False
    logger.info(f"File exists: {file_path}")            # 英語
    return True
```

---

## ログ仕様

すべてのプロジェクトに `{package_name}/logger.py` と `setup_logger()` 関数を含める。

**必須要件：**
- `constants.py` に `LOG_DIR = PROJECT_ROOT / "log"` を定義
- `setup_logger()` 内で `LOG_DIR.mkdir(parents=True, exist_ok=True)` を呼ぶ
- ログファイル名：`LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — 毎回新規ファイル、上書きしない
- `StreamHandler(sys.stdout)` と `FileHandler(..., encoding="utf-8")` の両方をアタッチ
- フォーマット：`[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- ハンドラーの重複追加を防ぐ：`if logger.handlers: return logger`
- 初期化時にログを出す：`logger.info("Logger initialized. level=%s, log_file=%s", ...)`
- サブモジュール：`get_logger(__name__)` でロガーを取得

`setup_logger()` は `main.py` / `__main__.py` の起動直後に呼ぶ。

---

## .bat ランチャーの規則

生成するすべての `.bat` ファイルに以下のルールを適用する：

### 基本構造

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run_bat.log"

echo [%date% %time%] Starting >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} %* >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

### 重要なルール

**タイムスタンプ付きログファイル名は必須。** `run_bat.log` のような固定名は禁止 — 毎回新規ファイルを作成する。上記の PowerShell スニペットを使う（`wmic` は Windows 11 24H2 以降で削除済みのため使用禁止）。

**.bat ファイルの内容は ASCII 文字のみ。** コメント・echo 文字列・ラベルに日本語を入れてはいけない。`cmd.exe` は bat ファイルをシステムの ANSI コードページ（日本語 Windows では CP932）でパースする。ファイル先頭に `chcp 65001` を書いてもパーサー側には効果がない。日本語 UTF-8 のバイト列が CP932 のリードバイトとして誤認され、後続のコマンド文字が消えて「`'etlocal' is not recognized`」のような謎エラーが発生する。説明文は README.md に書き、bat 内のコメント・echo はすべて英語にする。

**長時間コマンド**（PyInstaller ビルド・モデルダウンロード・テスト実行など）でコンソールが無音になるのを避けるため、PowerShell パイプでコンソールとログに同時出力する：

```bat
long_command.exe args 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

なぜ `Tee-Object` を使わないか：Windows PowerShell 5.1 の `Tee-Object` には `-Encoding` パラメータがないため、CP932 環境でログが文字化けする。`Write-Host` + `Add-Content` パターンなら PS 5.1 で文字化けなく動作する。

パイプ後のコマンドは `%ERRORLEVEL%` が PowerShell のものを反映するため、成功判定は生成物の存在確認で行う：

```bat
if not exist "dist\foo.exe" (
    echo [ERROR] build failed. see %BAT_LOG%
    pause
    exit /b 1
)
```

短時間コマンド（pip show・venv 有効化など）は通常の `>> "%BAT_LOG%" 2>&1` でよい。

---

## 命名規則

### インターフェース / 抽象基底クラス

プロジェクト内で1つのパターンを選んで統一する：

1. `{name}able.py` — 推奨（例：`media_convertable.py`）
2. `i_{name}.py` — Interface プレフィックス（例：`i_converter.py`）
3. `base_{name}.py` — 抽象基底クラス（例：`base_converter.py`）
4. `{name}.py` — 意図が明確な場合

### 実装クラス

`{実装名}_{name}.py` — 例：`ffmpeg_converter.py`、`file_logger.py`

---

## テスト

- pytest を使用
- 統合テストのみ作成 — 個々のメソッドの単体テストは不要
- 外部 API・外部ライブラリはモック化
- 環境変数もモック化できるように設計（`mock_env.py` を使用）
- 再利用可能なモックは `tests/mocks/` にまとめる — テストファイルごとに作り直さない
- テストフォルダはソースフォルダ構成をミラーリング

---

## パッケージング

- `pyproject.toml` を使用
- Python `>= 3.11`
- 依存ライブラリは `~=`（compatible release）で指定

---

## セットアップスクリプト

すべてのセットアップスクリプトは `setup/` に配置：

- `setup_venv.bat`：venv 作成 + 全依存ライブラリのインストールを一本で完結（Python はインストール済みを前提）
- `install_{ツール}.bat`：`winget` / `choco` でインストール可能な外部ツール用 — 実際にインストールまで行うスクリプト
- 手動手順が必要なツール（ライセンス手続き・手動 DL 必須）：`docs/install_{ツール}.md` に手順を書き、README からリンク

**禁止事項：**
- 説明だけ表示してインストールを行わない `install_python.bat` のような bat
- グローバル環境向けの `install_dependencies.bat`
- 「手動で何かを実行してください」と案内するだけの bat

---

## .gitignore

必ず含める：
```
.env
__pycache__/
*.pyc
venv/
.venv/
log/
cache/
```

---

## 技術選定

ライブラリやフレームワークを選ぶときは、決定前に MCP（context7）や Web 検索で最新の安定バージョンや破壊的変更を確認する。

---

## 簡易スクリプトの規則

単一 `.py` ファイルで完結するスクリプト向けのルール：

### ファイルヘッダー（必須）

```python
"""
{スクリプト名} — {何をするかの1行説明}

Usage:
  python {スクリプト名}.py [options] {positional_args}

  # 引数・オプションの説明をここに書く
"""
```

### コード構成テンプレート

```python
"""...(ヘッダー docstring)..."""

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
import sys
from pathlib import Path
from typing import Literal, Optional

# ── サードパーティ ──────────────────────────────────────────
import some_lib  # pip install some_lib

# ── 定数 ────────────────────────────────────────────────────
SOME_CONSTANT: str = "value"

# ── プライベート関数 ─────────────────────────────────────────
def _helper(value: str) -> str:
    """
    補助処理。

    :param value: 処理対象
    :return: 処理結果
    """
    return value.strip()

# ── メイン処理 ──────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    """メイン処理。:param args: コマンドライン引数"""
    ...

def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。:return: 解析済み引数"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)
```

**フルパッケージとの違い：**
- `logger.py` は不要 — `print()` または `logging.basicConfig()` で簡易出力
- `config.py` / `.env` は不要 — 設定は引数または定数で管理
- テスト・bat ファイル・setup スクリプト・`pyproject.toml` は生成しない
- 必要なサードパーティ製パッケージは `# pip install {package}` コメントで明示
