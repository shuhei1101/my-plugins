# QA — PR48 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX(連番)として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: スキル description のトリガー範囲

**状態**: 決定済み(2026-05-17)

A: 開発系画面の作成・編集時に常に発動(新規・既存問わず)。

---

## QA-002: 対象技術スタック

**状態**: 決定済み(2026-05-17)

スキル本体では特定フレームワークを指定しない。
バニラ HTML/CSS/JS で完結する**共通モジュール**を提供し、各画面はインポートして使う。
参考として `references/frontend.md` および `references/{html,css,js}.md` を SKILL.md からリンクするだけにする。

---

## QA-003: 開発系画面の判定

**状態**: 決定済み(2026-05-17)

本番判定の規約は設けない。`ui-dev` は「開発をサポートする画面」専用で、本番ユーザー向けには表示しない前提。
「不要な画面では明示的に呼ばない」運用とする。

---

## QA-004: フロートボタンの配置とスタイル

**状態**: 決定済み(2026-05-17)

デフォルト: 右下・🐛 絵文字・48px 丸・z-index 9999。
位置はモーダルヘッダーの「ボタン位置」セレクトで上下左右に変更でき、localStorage に保存。

---

## QA-005: JS ログの収集方法

**状態**: 決定済み(2026-05-17)

- `console.log/info/warn/error/debug` をラップしてリングバッファに収集
- `window.onerror` と `unhandledrejection` も自動取り込み
- バッファは全レベル収集、表示・コピーは設定レベル/行数でフィルタ
- ログ規約(JSON Lines 形式・ロガー必須・操作ログ重視・1 行ログ短く)を `references/common.md` に追加し、ui-dev スキルからリンクする

---

## QA-006: コピー時の JSON 形式

**状態**: 決定済み(2026-05-17)

スキーマ:

```json
{
  "page": "{location.pathname}",
  "url":  "{location.href}",
  "files": {
    "html": [], "css": [], "js": [], "backend": [], "other": []
  },
  "logs": {
    "limit": 100,
    "level": "error",
    "entries": [{ "ts": "ISO8601", "level": "log|info|warn|error|debug", "args": ["..."] }]
  },
  "capturedAt": "ISO8601"
}
```

関連ファイルの登録は `data-debug-files` 属性(JSON 文字列)または `window.__uidevFiles` グローバル。

---

## QA-007: ログ行数のユーザー設定

**状態**: 決定済み(2026-05-17)

localStorage に保存(`uidev.lines` キー)。デフォルト 100 行。
ログセクションのヘッダに inline で行数入力欄を置く。

---

## QA-008: ui-dev に関連 references の追加

**状態**: 決定済み(2026-05-17)

本 PR で以下も実施:

- `references/common.md` にログ規約セクションを追加(JSON Lines・ロガー必須・操作ログ重視・1 行ログ短く)
- `references/html.md` / `references/css.md` / `references/js.md` の雛形を新規作成(中身は今後追記)
- ui-dev SKILL.md から `references/frontend.md` / `references/html.md` / `references/css.md` / `references/js.md` / `references/common.md`(ログ規約)へリンク

---

## QA-009: モーダル UI 構成(モック確定版)

**状態**: 決定済み(2026-05-17)

モック検証の結果、最終 UI 構成:

- タブなし、縦スクロール
- セクション順: 概要 → 関連ファイル → 直近ログ(最下)
- ヘッダー: タイトル | ボタン位置セレクト | コピーボタン | 閉じる
- ログ枠は固定高(320px) — 中身の量で枠サイズは変わらない
- ログセクション内にレベル/行数の inline 設定
- ショートカット: Ctrl+Shift+D で開閉

---

## QA-010: 共通化方針(複数画面間)

**状態**: 決定済み(2026-05-17)

ボタン本体・ロガーフック・モーダルは**共通モジュール**として一度だけ読み込む。
各画面は `data-debug-files` 属性または `window.__uidevFiles` で関連ファイルを宣言するのみ。

スキル内テンプレートとして:

```
plugins/dev-kit/skills/ui-dev/templates/
├── uidev.css       — フロートボタン + モーダルのスタイル
├── uidev.js        — ロガーフック + モーダル制御 + コピー処理
└── README.md       — 使い方(各画面でのインポート方法・引数渡し方)
```

各画面側は `<link rel="stylesheet" href=".../uidev.css">` + `<script src=".../uidev.js" defer></script>` を読み込み、
関連ファイルを `data-debug-files` で宣言するだけ。
