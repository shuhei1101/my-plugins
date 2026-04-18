# Pythonルール

py-wizardが生成するPythonプロジェクトは以下のルールに従う。

---

## マイクロサービス設計方針

- 各ツールは完全に独立したパッケージ（別リポジトリ・別プロジェクト）
- ツール間連携が必要な場合:
  - コンフィグ or 環境変数で他ツールのパスを指定
  - デフォルトパスは特定ディレクトリ配下にある前提で設定済み
  - 自動ダウンロードは考えない（各自クローンして使う）

---

## フォルダ構成テンプレート

```
{package-name}/
├── {package_name}/
│   ├── {機能サブフォルダ}/    ...機能ごとに分割
│   ├── __init__.py            ...パッケージ初期化
│   ├── __main__.py            ...python -m {package_name} のエントリーポイント
│   ├── config.py              ...設定読み込み
│   ├── main.py                ...引数処理・起動分岐
│   ├── gui.py                 ...tkinter GUI
│   ├── cli.py                 ...argparse処理
│   ├── logger.py              ...logger初期化・設定
│   ├── exceptions.py          ...カスタム例外クラス
│   ├── constants.py           ...定数定義
│   └── utils.py or common/    ...共通ユーティリティ
├── gui.bat                    ...venv自動有効化機能付き（プロジェクトルート直下）
├── {モード別}.bat             ...venv自動有効化機能付き（プロジェクトルート直下）
├── setup/                     ...セットアップ用bat一式
│   ├── setup_venv.bat         ...venv作成＋依存ライブラリインストールまで完結
│   └── install_{外部ツール}.bat ...自動インストール不可能な外部ツール向け専用bat（任意）
├── docs/                      ...自動インストール不可能な外部ツールの手動手順書（任意）
│   └── install_{外部ツール}.md ...手動インストール手順（READMEからリンク）
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {機能名}/              ...機能ミラー構成
│       ├── conftest.py
│       └── test_{機能名}.py
├── venv/                      ...Python仮想環境（.gitignore対象）
├── resources/                 ...GUIリソース等
├── log/                       ...ログ（固定）
├── input/                     ...入力ファイル（任意。大量入力がある場合）
├── output/                    ...出力ファイル（任意。大量出力がある場合）
├── cache/                     ...作業中キャッシュ（任意）
├── activate.bat               ...venv有効化ショートカット
├── .env.sample
├── .gitignore                 ...venv/, .env, log/等を除外
├── README.md
└── pyproject.toml
```

**空フォルダの管理**:
- `log/`, `input/`, `output/`, `cache/` 等の空フォルダには `.gitkeep` を配置
- README.mdは不要（Gitリポジトリでフォルダ構造を保持するためのみ使用）

**仮想環境（venv）の推奨**:
- プロジェクトごとに独立した Python 環境を作成（依存関係の競合を防ぐ）
- `setup_venv.bat` で自動セットアップ
- すべての `.bat` ファイルはプロジェクトルート直下に配置（`bat/` サブフォルダは作らない）
- すべての `.bat` ファイルは venv が存在する場合自動的に有効化
- `.gitignore` に `venv/` を追加（リポジトリに含めない）

**外部ツールの自動インストール**:
- 可能な限り自動インストールスクリプトを提供（例: ffmpegの場合はwingetで自動インストール）
- 自動インストール失敗時は手動インストールガイドにフォールバック
- インストール済みチェック機能を含める

---

## 設定関連

- `config.py` と `.env`、`.env.sample` を用意
- `config.py`: 上部でデフォルト値定義 → 下部で.env読み込み上書き（.envが後勝ち）
- 設定優先順位: 環境変数（初期ロード）→ 引数による上書き
- アプリ内の外部ライブラリの引数などはだいたい設定できるようにする
- `.env`未存在時: `.env.sample`をコピーして`.env`を作成（キー空）

---

## 起動関連

- 引数なしでbat実行 → GUIで起動
- 引数ありで実行 → コマンドラインで直接起動
  - `--help`, `-h` でヘルプ表示
- 複数モードがある場合はモードごとにbatファイルを用意
- `main.py`: 引数処理と起動方法の分岐のみ（高レベル）
  - 低レベル処理は書かない。抽象クラス・インターフェースに分離する

---

## GUI関連

- tkinterを使用してシンプルなGUIを作成
  - 実行ボタンは青色
  - 設定ボタンを配置、クリックで設定画面をモーダル表示
- 設定画面:
  - すべての設定項目をGUI上でも変更可能にする
  - 設定変更で.envファイルの内容を更新
  - 実行後に反映できない設定は赤字で「再起動後に適用されます」と表示
- GUI案はプロジェクトごとにAIが都度生成（3案提示 → ユーザー選択）

---

## コーディングスタイル

- `typing` を使用して型は厳格にする（Literal, Union等を積極的に。TypeScriptの型定義を参考に）
- docstringはreStructuredText形式
- コメントは関数ドキュメンテーションに加え、複雑な行は適宜コメント
- リーダブルコード意識（仮変数の活用）
- デザインパターン適用（テンプレート、ストラテジー等、適材適所）

---

## 言語使用ルール

### 英語を使用する箇所（batで日本語がバグるため）
- **print文**: すべて英語で記述
- **logger出力**: すべて英語で記述（logger.info(), logger.error() 等）

### 日本語を使用する箇所
- **コメント**: すべて日本語で記述（docstring、インラインコメント）
- **環境変数の説明**: .env.sample等のコメント
- **変数名・関数名**: 英語（Python命名規則に従う）
- **GUI表示文言**: 日本語（tkinter等のUI文字列）

### 例
```python
# ファイル存在チェックを行う
def check_file_exists(file_path: Path) -> bool:
    """
    ファイルが存在するかチェックする
    
    :param file_path: チェック対象のファイルパス
    :return: 存在する場合True、しない場合False
    """
    if not file_path.is_file():
        logger.error(f"File not found: {file_path}")  # ← logger は英語
        return False
    
    logger.info(f"File exists: {file_path}")  # ← logger は英語
    return True
```

---

## ログ仕様

- pythonのloggerを使用（`logger.py`で初期化・設定を集約）
- ログレベルごとに出力内容を変える
- ログレベルは設定で変更可能
- がっつりログを入れる（デバッグ時に処理を追いやすくする）
- ログメッセージは英語で記述（言語使用ルール参照）

### Python logger（必須）

生成されるプロジェクトには以下を必ず含める:

- `{package_name}/logger.py` に `setup_logger()` を定義し、`main.py` / `__main__.py` の起動直後に呼び出す
- `constants.py` に `LOG_DIR = PROJECT_ROOT / "log"` を定義
- `setup_logger()` の必須仕様:
  - `LOG_DIR.mkdir(parents=True, exist_ok=True)` でログフォルダ自動作成
  - ファイル名はタイムスタンプ付きとし、`LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` の形式で生成（毎回新規ファイル、過去実行を上書きしない）
  - `StreamHandler(sys.stdout)` + `FileHandler(..., encoding="utf-8")` の両方をアタッチ
  - bat ログ（後述）と同じタイムスタンプ粒度にすることで、同一実行の bat ログと python ログをソート順で相関できる
  - フォーマット例: `[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
  - 多重追加防止（`if logger.handlers: return logger`）
  - 初期化時に `logger.info("Logger initialized. level=%s, log_file=%s", ...)` を出す
  - `latest.log` のような固定名シンボリックリンク/コピーは任意（必要ならオプションで追加）。デフォルトは強制しない
- サブモジュールは `get_logger(__name__)` でロガー取得
- 参考実装: `voice-paste/voice_paste/logger.py`

### .bat ランチャーログ（必須）

生成される `run.bat` および `bat/*.bat` には以下を必ず組み込む（サイレント失敗防止）:

- `chcp 65001 > nul` + `setlocal` で開始
- `set "LOG_DIR=%~dp0log"` → `if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"`
- **タイムスタンプ付きログファイル名（必須）**: 固定の `run_bat.log` は禁止（過去実行が上書きされるため）。実行ごとに `YYYYMMDD_HHMMSS_run_bat.log` を新規作成する。正準スニペット（ASCII-only / CP932安全）:

  ```bat
  for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
  set "BAT_LOG=%LOG_DIR%\%TS%_run_bat.log"
  ```

  **`wmic` は使わないこと**。Windows 11 24H2 以降では `wmic` が既定で削除されており、`for /f ... wmic os get localdatetime ...` は `LDT` を空のまま通過し、`%LDT:~0,14%` がリテラル文字列 `~0,14` に展開されて `~0,14_run_bat.log` のようなゴミファイル名が生成される（サイレント失敗）。PowerShell 版はサポート対象の全 Windows バージョンで動作するため、常にこちらを採用する
- 開始・cwd・venv有効化・起動コマンドを `echo [%date% %time%] ... >> "%BAT_LOG%"` で記録
- venv自動有効化は `call ...\activate.bat >> "%BAT_LOG%" 2>&1`
- Python起動は `python -m {package_name} >> "%BAT_LOG%" 2>&1` で stdout/stderr を両方キャプチャ
- `set "EXITCODE=%ERRORLEVEL%"` を退避し、非ゼロの場合は画面にエラー＋ログパスを出し `pause`（ウィンドウ維持）
- `endlocal & exit /b %EXITCODE%` で終了コード伝播
- **長時間コマンドは PowerShell パイプでコンソールとログに同時出力する**: 通常の `>> "%BAT_LOG%" 2>&1` だとコンソールが無音になり、PyInstaller ビルドやモデルダウンロードなど数分かかる処理でユーザに進捗が見えずフリーズと誤認される。その場合は PowerShell の `Write-Host` + `Add-Content` パイプを使う:

  ```bat
  long_command.exe args 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
  ```

  ポイント:
  - `[Console]::InputEncoding = UTF8` で、`chcp 65001` 配下の子プロセスが出す UTF-8 バイト列を PowerShell が正しく解釈する（設定しないと PS は既定で ANSI=CP932 として読み込み、日本語 Windows で激しい文字化けが発生する）
  - `Write-Host` でコンソール表示、`Add-Content -Encoding utf8` でログファイルに UTF-8 追記
  - `-LiteralPath` で `[` `]` などを含むパスのワイルドカード展開を防ぐ
  - Windows PowerShell 5.1（Windows 7 SP1 以降に標準搭載）で動作

  **なぜ `Tee-Object` を直接使わないか**: `Tee-Object` は一見この用途に合うが、Windows PowerShell 5.1 の `Tee-Object` には `-Encoding` パラメータが存在せず（PS 6+ / `pwsh` のみ対応）、出力ファイルの文字コードを制御できない。さらに `[Console]::InputEncoding` を UTF-8 に設定しないと、CP932 環境では UTF-8 入力が CP932 として解釈され、ログが丸ごとモジバケする。上記の `Write-Host` + `Add-Content` 形式なら PS 5.1 のみで文字化けなく動作する。

  **注意: パイプ後の `%ERRORLEVEL%` は元コマンドではなく PowerShell の終了コードを反映する**。成功判定には ERRORLEVEL ではなく既知の生成物の存在確認を使うこと。例:

  ```bat
  pyinstaller --onefile foo.py 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
  if not exist "dist\foo.exe" (
    echo [ERROR] build failed. see %BAT_LOG%
    pause
    exit /b 1
  )
  ```

  使い分け:
  - 短時間コマンド（`pip show`、venv 有効化など）: 素直に `>> "%BAT_LOG%" 2>&1` でよい
  - 長時間コマンドで進捗が見えないと困るもの（PyInstaller ビルド、モデルダウンロード、テスト実行など）: 上記の `Write-Host` + `Add-Content` パターンを使う
- 参考実装: `voice-paste/run.bat`
- **【最重要・ASCII限定】`.bat` ファイルの中身は ASCII 文字のみにすること（日本語コメント・`echo` 文字列すべて禁止）**。理由: `cmd.exe` は bat をシステムANSIコードページ（日本語Windowsでは CP932）でパースする。ファイル先頭に `chcp 65001` を書いても**パーサ側の字句解析にはそれが適用されない**ため無意味。UTF-8保存の日本語バイト（例: 「起動」= `E8 B5 B7 E5 8B 95`）が CP932 のリードバイトとして誤認され、続くコマンド文字を食い潰す。実例: `setlocal` の直前に日本語コメントがあると `'etlocal' is not recognized as an internal or external command`（先頭の `s` が直前バイトに吸われる）という謎エラーになる。日本語の説明文は `README.md` 側に書き、bat 内のコメント・echo はすべて英語で書くこと。Shift-JIS保存でも動くが環境依存で壊れやすいので必ず ASCII-only を選ぶ。

---

## 命名規則

### インターフェース/抽象クラスと実装の関係

**インターフェース/抽象基底クラスの命名**:
- インターフェース的な役割の場合、以下のいずれかを採用（プロジェクト内で統一）:
  1. `{name}able.py` — 推奨。インターフェース的な役割を明示（例: `media_convertable.py`, `loggable.py`）
  2. `i_{name}.py` — Interface prefix（例: `i_converter.py`）
  3. `base_{name}.py` — 抽象基底クラス的な役割（例: `base_converter.py`）
  4. `{name}.py` — シンプルな命名（例: `converter.py`）

**実装クラスの命名**:
- インターフェース/抽象クラスを実装する場合: `{implementation}_{name}.py`
- 例:
  - `media_convertable.py` → `ffmpeg_converter.py`, `moviepy_converter.py`
  - `base_converter.py` → `ffmpeg_converter.py`, `custom_converter.py`
  - `i_logger.py` → `file_logger.py`, `console_logger.py`

**命名の一貫性**:
- 同一プロジェクト内では命名パターンを統一すること
- 例: プロジェクト全体で `~able.py` を採用したら、他のインターフェースも `~able.py` とする

---

## テスト関連

- pytestを使用
- テストコードは単体レベルでは不要。基本は統合テストのみ作成
  - 外部API・外部ライブラリの呼び出しはモック化
  - 環境変数もモック化可能に設計
- モックファイルは再利用可能な別ファイルとして管理（毎回作成しない）:
  - `tests/mocks/mock_env.py` — 環境変数モック
  - `tests/mocks/mock_externals.py` — 外部ライブラリ返却値モック
- テストフォルダは機能ミラー構成
- テストコードは `tests/` フォルダに配置

---

## パッケージ化

- `pyproject.toml` を使用
- Python >= 3.11
- 依存ライブラリは `~=` 指定

---

## セットアップ

- `setup/` フォルダにセットアップ用bat一式を配置
- Windowsユーザ向け

**`setup_venv.bat` の役割**:
- venv の作成から `pip install` による依存ライブラリのインストールまで1本で完結させる
- Python がインストール済みであることを前提とする（Python 自体のインストールは `winget` 等で自動実行する場合を除き、ユーザーが事前に行う）

**外部ツール（ffmpeg、CUDA等）の扱い**:
- `winget` / `choco` 等で自動インストール可能なものは `setup_venv.bat` 内に組み込む、または専用の `install_{外部ツール}.bat` を作成して実際にインストールまで行う
- 自動インストールが不可能なもの（ライセンス手続き・手動DLが必須のもの等）は `docs/install_{外部ツール}.md` に手順を記載し、`README.md` からリンクを貼る

**禁止事項**:
- `install_python.bat` のような「案内だけ」で実際のインストールを行わない bat は作成しない
- `install_dependencies.bat`（レガシー・グローバル環境用）は作成しない
- bat ファイルは必ず「実行したら完了する」ものにする

---

## .gitignore

適切に設定する:
- `.env`
- `__pycache__/`
- `log/`
- `cache/`
- `*.pyc`
- `.venv/`
- 等

---

## 技術選定

- 開発技術・ライブラリ選定時は **MCP（context7）やWeb検索を使って最新情報を調査する**
- 該当ステップ: 2.5（開発技術）、3.2（実装計画）
