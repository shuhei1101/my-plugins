# {project-name} — プロジェクト構造

## 概要
{このツールが何をするかを1〜2行で}

---

## 機能A: {機能名}

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| {module}.py | {処理の概要} | {package_name}/{module}.py |

---

## 機能B: {機能名}

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| {module}.py | {処理の概要} | {package_name}/{module}.py |

---

## 共通モジュール

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| config.py | 設定読み込み | {package_name}/config.py |
| main.py | エントリーポイント | {package_name}/main.py |
| gui.py | tkinter GUI | {package_name}/gui.py |
| logger.py | ログ設定（log/ への FileHandler + StreamHandler） | {package_name}/logger.py |
| run.bat | メインランチャー（log/ へ stdout/stderr 記録） | run.bat |
| exceptions.py | カスタム例外 | {package_name}/exceptions.py |
| constants.py | 定数定義 | {package_name}/constants.py |
| utils.py | 共通ユーティリティ | {package_name}/utils.py |

---

## テスト

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| mock_env.py | 環境変数モック | tests/mocks/mock_env.py |
| mock_externals.py | 外部ライブラリ返却値モック | tests/mocks/mock_externals.py |
