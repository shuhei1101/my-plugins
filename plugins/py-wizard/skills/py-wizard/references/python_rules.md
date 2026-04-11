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
├── bat/
│   ├── gui.bat                ...venv自動有効化機能付き
│   └── {モード別}.bat         ...venv自動有効化機能付き
├── setup/                     ...セットアップ用bat一式
│   ├── setup_venv.bat         ...venv作成+依存関係インストール
│   ├── install_dependencies.bat ...レガシー（グローバル環境用）
│   ├── install_python.bat     ...Pythonインストールガイド
│   └── install_{外部ツール}.bat ...外部ツール自動インストール
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
- Windowsユーザ向け（Pythonインストールから案内）

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
