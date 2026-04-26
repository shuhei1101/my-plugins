# py-wizard セッション記録 - 20260426143052

## セッション情報
- 開始時刻: 2026-04-26 14:30:52
- モード: 新規作成
- プロジェクト名: youtube-comment-fetcher
- プロジェクトパス: C:/Users/shuhe/repo/youtube-comment-fetcher

## 要件まとめ
YouTube Live のコメントを取得して CSV に保存する CLI ツール。
OAuth 認証済みの API キーを使い、指定した動画 ID のチャット ID を取得後、ポーリングでコメントを収集する。
GUI（tkinter）で動画 URL 入力 + 開始/停止ボタン付き。

## 作業ログ
- [x] README 作成
- [x] フォルダ構成生成（youtube_comment_fetcher/）
- [x] GUI 設計（アスキーアート案）
- [ ] main.py 実装
- [ ] tests/ 実装

## 作成・変更ファイル
| ファイル名 | 操作 | パス |
|------------|------|------|
| README.md | 新規 | ./README.md |
| main.py | 新規 | youtube_comment_fetcher/main.py |
| gui.py | 新規 | youtube_comment_fetcher/gui.py |
| logger.py | 新規 | youtube_comment_fetcher/logger.py |
| run.bat | 新規 | ./run.bat |

## テスト結果
- pass: 0
- fail: 0

## 完了情報
- 完了時刻: -
- 残タスク: main.py 実装、tests/ 実装
