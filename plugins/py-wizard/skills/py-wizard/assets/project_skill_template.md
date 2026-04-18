# {プロジェクト名} — プロジェクト構造

## 概要
{プロジェクトの1行概要}

---

## 機能A: {機能名}

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| xxx.py | XXXの処理 | {pkg}/xxx/xxx.py |

---

## 機能B: {機能名}

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|

---

## 共通モジュール

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| config.py | 設定読み込み | {pkg}/config.py |
| main.py | エントリーポイント | {pkg}/main.py |
| gui.py | tkinter GUI | {pkg}/gui.py |
| cli.py | argparse処理 | {pkg}/cli.py |
| logger.py | ログ設定（`log/{pkg}.log` への FileHandler + StreamHandler を設定、必須） | {pkg}/logger.py |
| run.bat | メインランチャー（`log/run_bat.log` へ stdout/stderr 記録、失敗時 pause、必須） | run.bat |
| exceptions.py | カスタム例外 | {pkg}/exceptions.py |
| constants.py | 定数定義 | {pkg}/constants.py |
| utils.py | 共通ユーティリティ | {pkg}/utils.py |

---

## テスト

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| mock_env.py | 環境変数モック | tests/mocks/mock_env.py |
| mock_externals.py | 外部ライブラリモック | tests/mocks/mock_externals.py |
