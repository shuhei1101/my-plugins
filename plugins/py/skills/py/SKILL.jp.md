# SKILL.jp.md — py スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: py
**トリガー**: Python コードの作成・レビュー・修正、`.py` ファイルの編集、`.bat` ランチャーの作成、`pyproject.toml` の設定、新規 Python プロジェクトの立ち上げなど、Python に関わるあらゆる作業で自動適用される

---

# py — Python プロジェクトコーディング規約

このプロジェクトで Python コードを書くときに従うべき規約とコーディング標準を提供する。

---

## 概要

各ツールは **完全に独立したパッケージ**（別リポジトリ・別プロジェクト）として作る。ツール間で連携が必要な場合は、設定ファイルや環境変数で他ツールのパスを指定する — プロセス内での共有や自動ダウンロードはしない。

---

## 作業内容

### ステップ1: コーディング前のコンテキスト確認

#### 条件

- 常に — Python コードを書いたりファイルを作成する前に実行する

#### 処理内容

1. プロジェクトの種別を判断する：
   - **新規プロジェクト** → ステップ2でスキャフォールドを設定する
   - **既存プロジェクト** → 既存のフォルダ構成を読んでからステップ3へ進む
2. **単一ファイルの簡易スクリプト**（フルパッケージではない）の場合 → 参考資料の「簡易スクリプトの規則」へ直接進む

→ ステップ2（新規プロジェクト）またはステップ3（既存プロジェクトか簡易スクリプト）へ進む

#### 出力

- コンテキスト確認済み：新規プロジェクト・既存プロジェクト・簡易スクリプトのいずれか

---

### ステップ2: プロジェクトスキャフォールドの設定

#### 条件

- 新規 Python プロジェクトをゼロから作成するとき

#### 入力

- プロジェクト名・パッケージ名

#### 処理内容

1. フォルダ構成を作成する（参考資料のフォルダ構成参照）。
2. Python `>= 3.11`・依存ライブラリは `~=` で指定した `pyproject.toml` を作成する。
3. `.gitignore` を作成する（最低限：`.env`、`__pycache__/`、`*.pyc`、`venv/`、`.venv/`、`log/`、`cache/`）。
4. `.env.sample` を作成する（すべての必須環境変数をプレースホルダーで記述）。
5. `setup/setup_venv.bat` を作成する — venv 作成 + 全依存ライブラリのインストールを一本で完結。
6. `activate.bat` を作成する（利便性のため）。
7. 空フォルダ（`log/`、`input/`、`output/`、`cache/`）に `.gitkeep` を置く。

→ ステップ3へ進む

#### 出力

- 必要なすべてのファイルとディレクトリを含むプロジェクトスキャフォールドが作成済み

#### 補足

##### 禁止事項

- `bat/` サブフォルダを作らない — すべての `.bat` ファイルはプロジェクトルート直下に置く
- 空フォルダの中に README.md を置かない — `.gitkeep` のみ使用する

---

### ステップ3: Python コードを書く

#### 条件

- Python ソースファイル（`.py`）を書いたり修正するとき

#### 入力

- タスクの説明と対象ファイル

#### 処理内容

1. `typing` を厳格に使用する — `Literal`、`Union`、`Optional`、ジェネリクス（TypeScript の型定義を参考に）。
2. docstring は reStructuredText 形式で書く（`:param:`、`:return:`、`:raises:`）。
3. 実行時バリデーションが重要なシステム境界では型ヒントだけでなく Pydantic モデルを使う（対象範囲は参考資料の「Pydantic の境界」参照）。
4. 言語使用ルールに従う：
   - **英語のみ**：すべての `print()` 文と `logger` 出力
   - **日本語 OK**：コードコメント・`.env.sample` のコメント・GUI の表示文字列
5. ロガーが正しく設定されているか確認する（参考資料のロガー仕様参照）。
6. デザインパターンを適材適所で適用する（Template・Strategy など）— 過度な抽象化は避ける。
7. リーダブルコードを意識して書く：意図を明確にするための中間変数を積極的に使う。

→ bat ランチャーが必要な場合はステップ4へ、そうでなければ完了

#### 出力

- プロジェクトの規約に従って Python コードが書かれている

#### 補足

##### 禁止事項

- `print()` や `logger` の呼び出しに日本語を入れない — bat ファイルで文字化けする
- bat ファイルで `wmic` を使わない — Windows 11 24H2 以降で削除済み。代わりに PowerShell のタイムスタンプスニペットを使う

---

### ステップ4: bat ランチャーを作成する

#### 条件

- プロジェクトの `.bat` 起動スクリプトを作成するとき

#### 入力

- パッケージ名と起動モード

#### 処理内容

1. 参考資料の「bat ランチャーテンプレート」を使用する。
2. 必須要件を守る：
   - タイムスタンプ付きログファイル名は**必須** — `run_bat.log` のような固定名は禁止
   - `.bat` ファイルの内容は**すべて ASCII 文字のみ** — コメント・echo 文字列・ラベルに日本語を入れない
   - タイムスタンプには PowerShell の `Get-Date` スニペットを使う（`wmic` 禁止）
3. FastAPI / HTTP サーバーの場合：参考資料の「FastAPI run.bat テンプレート」を使用する。
4. 長時間コマンドの場合：コンソールとログへの同時出力のために PowerShell パイプパターンを使用する。

→ 完了

#### 出力

- すべてのルールに従った `.bat` ランチャーが作成済み

#### 補足

##### なぜ bat ファイルを ASCII のみにするか

`cmd.exe` は bat ファイルをシステムの ANSI コードページ（日本語 Windows では CP932）でパースする。`chcp 65001` をファイル先頭に書いてもパーサー側には効果がない。日本語 UTF-8 のバイト列が CP932 のリードバイトとして誤認され、後続のコマンド文字が消えて「`'etlocal' is not recognized`」のような謎エラーが発生する。説明文は README.md に書く。

---

### ステップ5: テストを書く

#### 条件

- プロジェクトのテストを書くとき

#### 入力

- テスト対象の機能またはモジュール

#### 処理内容

1. pytest を使用する。
2. 統合テストのみ作成する — 個々のメソッドの単体テストは不要。
3. 外部 API・外部ライブラリはモック化する。
4. 環境変数もモック化できるように設計する（`mock_env.py` を使用）。
5. 再利用可能なモックは `tests/mocks/` にまとめる — テストファイルごとに作り直さない。
6. テストフォルダはソースフォルダ構成をミラーリングする。

→ 完了

#### 出力

- プロジェクトの規約に従ってテストが作成済み

---

### ステップ6: プロジェクトへのルール展開

#### 条件

- プロジェクトでこのスキルを初めて使用するとき

#### 処理内容

1. プロジェクトルートで `Glob(".claude/rules/implementation.md")` を実行して確認。
2. 存在しなければ、`.claude/rules/implementation.md` を以下の内容で作成：

```markdown
---
paths:
  - "src/**/*.py"
---

# 実装作業

## コードを書く前に

1. `wiki/` に仕様が存在するか確認する。関連する wiki ドキュメントが不足しているか、リクエストと矛盾している場合は、ユーザーに報告してから進む。
2. このエリアに関わる未決定 Issue が `wiki/Issues.md` にある場合は、着手前にユーザーへ通知する。
3. Python コードを書く前に `/py:py` スキルを読む。

## コミット前チェックリスト

- [ ] コード・設定ファイルの変更
- [ ] `docs/PR/PR{N}.md` の作成または更新
- [ ] 実装が文書化された動作を変更した場合は wiki ドキュメントを更新
- [ ] 新しいファイル種別・ディレクトリを追加した場合は `.gitignore` を更新
- [ ] 新しい設計上の決定を `wiki/Issues.md` または関連する機能ドキュメントに記録
```

3. `.claude/rules-jp/implementation.md` をスタブとして作成：

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/implementation.md`。**
```

4. コミット：`git add .claude/rules/ && git commit -m "chore: add implementation rule"`

→ 完了

#### 出力

- `.claude/rules/implementation.md` が作成・コミット済み

---

## 参考資料

### フォルダ構成

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
├── gui.bat
├── {モード}.bat                # モードごとに1ファイル
├── setup/
│   ├── setup_venv.bat
│   └── install_{ツール}.bat
├── docs/
│   └── install_{ツール}.md
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {機能名}/
│       ├── conftest.py
│       └── test_{機能名}.py
├── venv/                       # .gitignore 対象
├── resources/
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

### Pydantic の境界

実行時バリデーションが重要なシステム境界では、型ヒントだけでなく Pydantic モデルを使う：

**Pydantic を使う箇所：** 外部 API へのリクエスト・レスポンス、LLM への入力と出力（Instructor 経由）、設定ファイルの読み込み（YAML / JSON）、ファイル間で受け渡すデータ（CSV / JSONL のレコード）、ユーザー入力のパース、スレッド / プロセス間で受け渡すイベントデータ

**型ヒントのみで十分な箇所：** 単一関数内で完結する内部ロジックの引数・戻り値、関数内に閉じた `dict` / `list` の型表現

### ロガー仕様

すべてのプロジェクトに `{package_name}/logger.py` と `setup_logger()` 関数を含める：

- `constants.py` に `LOG_DIR = PROJECT_ROOT / "log"` を定義する
- `setup_logger()` 内で `LOG_DIR.mkdir(parents=True, exist_ok=True)` を呼ぶ
- ログファイル名：`LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — 毎回新規ファイル
- `StreamHandler(sys.stdout)` と `FileHandler(..., encoding="utf-8")` の両方をアタッチする
- フォーマット：`[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- ハンドラーの重複追加を防ぐ：`if logger.handlers: return logger`
- サブモジュール：`get_logger(__name__)` でロガーを取得する

`setup_logger()` は `main.py` / `__main__.py` の起動直後に呼ぶ。

### bat ランチャーテンプレート

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

長時間コマンドは PowerShell パイプでコンソールとログに同時出力する：

```bat
long_command.exe args 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

パイプ後のコマンドは `%ERRORLEVEL%` が PowerShell のものを反映するため、成功判定は生成物の存在確認で行う：

```bat
if not exist "dist\foo.exe" (
    echo [ERROR] build failed. see %BAT_LOG%
    pause
    exit /b 1
)
```

### FastAPI run.bat テンプレート

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run.log"

if not "%1"=="" set "PORT=%1"

echo [%date% %time%] Starting. PORT=%PORT% >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

ポートの運用：メインリポジトリ用の固定ポートを予約し、worktree テスト起動では固定ポート + 1 以上を使う。

### 簡易スクリプトの規則

単一 `.py` ファイルで完結するスクリプト向けのルール：

**ファイルヘッダー（必須）：**

```python
"""
{スクリプト名} — {何をするかの1行説明}

Usage:
  python {スクリプト名}.py [options] {positional_args}

  # 引数・オプションの説明をここに書く
"""
```

**コード構成テンプレート：**

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
    return value.strip()

# ── メイン処理 ──────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    ...

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)
```

フルパッケージとの違い：`logger.py` は不要・`config.py`/`.env` は不要・テスト・bat・setup スクリプト・`pyproject.toml` は生成しない。必要なサードパーティ製パッケージは `# pip install {package}` コメントで明示。

### 命名規則

**インターフェース / 抽象基底クラス** — プロジェクト内で1つのパターンを選んで統一する：
1. `{name}able.py` — 推奨（例：`media_convertable.py`）
2. `i_{name}.py` — Interface プレフィックス（例：`i_converter.py`）
3. `base_{name}.py` — 抽象基底クラス（例：`base_converter.py`）

**実装クラス：** `{実装名}_{name}.py`（例：`ffmpeg_converter.py`）

### GUI（tkinter）

- 実行ボタン：青色
- 設定ボタンを配置 → クリックでモーダル設定画面を開く
- 設定画面：全設定項目を GUI から変更可能。変更内容は `.env` ファイルに保存
- 再起動が必要な設定：赤字で「再起動後に適用されます」と表示
- GUI レイアウト：プロジェクトごとに AI が 3 案提示 → ユーザーが選択
