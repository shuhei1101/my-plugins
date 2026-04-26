# youtube-comment-fetcher — プロジェクト構造

## 概要
YouTube Live のコメントをリアルタイム取得して CSV に保存する CLI + GUI ツール

---

## 機能A: コメント取得

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| fetcher.py | YouTube Data API v3 でチャット取得 | youtube_comment_fetcher/fetcher.py |
| auth.py | OAuth2 認証フロー | youtube_comment_fetcher/auth.py |

---

## 機能B: データ保存

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| exporter.py | CSV 出力処理 | youtube_comment_fetcher/exporter.py |

---

## 共通モジュール

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| config.py | 設定読み込み | youtube_comment_fetcher/config.py |
| main.py | エントリーポイント | youtube_comment_fetcher/main.py |
| gui.py | tkinter GUI | youtube_comment_fetcher/gui.py |
| logger.py | ログ設定（log/app.log への FileHandler + StreamHandler） | youtube_comment_fetcher/logger.py |
| run.bat | メインランチャー（log/run_bat.log へ stdout/stderr 記録） | run.bat |
| exceptions.py | カスタム例外 | youtube_comment_fetcher/exceptions.py |
| constants.py | 定数定義（API_BASE_URL, MAX_RESULTS 等） | youtube_comment_fetcher/constants.py |
| utils.py | 共通ユーティリティ | youtube_comment_fetcher/utils.py |

---

## テスト

| ファイル名 | 概要 | ファイルパス |
|------------|------|-------------|
| mock_env.py | 環境変数モック | tests/mocks/mock_env.py |
| mock_externals.py | YouTube API レスポンスモック | tests/mocks/mock_externals.py |
