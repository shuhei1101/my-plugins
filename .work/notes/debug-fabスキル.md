# debug-fabスキル — 開発系画面のフロートデバッグボタン

## 概要

`dev-kit:html-debug-fab` は、開発系画面（管理画面・内部ツール・デバッグ画面）に必ず設置するフロートデバッグボタン（FAB）＋モーダル。画面情報（関連ファイルパス + 直近 JS ログ）を JSON でクリップボードにコピーし、そのまま Claude Code に貼り付けてデバッグできることを目的とする。本番ユーザー向け画面では使わない。

## 共通化方針

- 各画面に同じデバッグ実装をコピペするのは禁止。共通の `uidev.css` / `uidev.js` を 1 回読み込む。
- 各画面は関連ファイルを `data-debug-files` 属性（または `window.__uidevFiles` グローバル）で宣言するだけ。両方併用可で、`uidev.js` は両方を読み取りマージする。

## フロートボタン

| 項目 | デフォルト |
|---|---|
| 位置 | 右下 (`bottom: 16px; right: 16px;`) |
| アイコン | 🐛 |
| サイズ | 48px 丸 |
| z-index | 9999 |

- クリックまたは `Ctrl+Shift+D` でモーダルを開閉。
- 位置はモーダル内のセレクトで変更でき localStorage に保存。

## モーダル

- タブなしの縦スクロール。セクション順: 概要 → 関連ファイル → 直近ログ（最下）。
- ヘッダー: タイトル | ボタン位置セレクト | コピーボタン | 閉じる。
- ログ枠は固定高 320px（中身の量で枠サイズが変わらない）。
- コピーボタン押下で `page` / `url` / `files` / `logs` を含む JSON をクリップボードへコピー。

## ログ収集

- `console.log / info / warn / error / debug` をラップしてリングバッファに溜める。
- `window.onerror` と `unhandledrejection` も自動取り込み。
- バッファ上限は 2000 行（古いものから捨てる）。表示・コピーは設定行数（デフォルト 100）で絞る。

## localStorage キー

| キー | 用途 | デフォルト |
|---|---|---|
| `uidev.lines` | ログ表示・コピー行数 | 100 |
| `uidev.level` | 出力レベル（error / warn / info / debug） | error |
| `uidev.pos` | フロートボタン位置 | bottom-right |

## クリップボードコピー（copyJSON）

非セキュアコンテキスト（SSH 経由 HTTP 等）では `navigator.clipboard` が undefined になるため、以下の順で試みる。

1. `navigator.clipboard.writeText()`
2. 失敗時: `textarea` + `document.execCommand('copy')` フォールバック
3. それも失敗時: `alert` でエラーメッセージ表示

## 参考ドキュメント

- `plugins/dev-kit/skills/html-debug-fab/SKILL.md`: スキル本体
- `plugins/dev-kit/skills/html-debug-fab/templates/uidev.css` / `uidev.js`: 共通モジュール

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成（specsから統合） | 260531_notes-spec-and-ref-inject |
