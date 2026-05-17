# debug-fab templates

> 日本語ミラー: `CLAUDE.jp.md`(参照用、Claude Code は読み込まない)
> 変更時は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映する。

`ui-kit:debug-fab` スキルが提供する共通デバッグウィジェットのテンプレート集。
開発をサポートする画面に必ず設置するフロートデバッグボタン + モーダルの本体ファイル。

---

## フォルダ構成

| ファイル | 役割 |
|---|---|
| `uidev.css` | フロートボタン + デバッグモーダルのスタイル |
| `uidev.js`  | ロガーフック + モーダル制御 + コピー処理 |
| `example.html` | 最小組み込み例(各画面に組み込むときの参考) |
| `CLAUDE.md` / `CLAUDE.jp.md` | このフォルダの使い方ガイド(自動読み込み) |

---

## 各画面での使い方

### ① CSS / JS を 1 回読み込む(プロジェクトで共有)

```html
<link rel="stylesheet" href="/static/uidev.css" />
<script src="/static/uidev.js" defer></script>
```

`uidev.js` は読み込まれた瞬間から `console.log/info/warn/error/debug` を全て収集する。
`window.onerror` と `unhandledrejection` も自動で取り込む。

### ② 各画面で関連ファイルを宣言

**A. `data-debug-files` 属性で宣言(推奨)**

```html
<body data-debug-files='{
  "html":    ["pages/user_list.html"],
  "css":     ["styles/user_list.css"],
  "js":      ["scripts/user_list.js"],
  "backend": ["api/users.py"]
}'>
```

複数要素に分けて書いてもよい(マージされる):

```html
<form data-debug-files='{"backend":["api/auth.py"]}'>...</form>
<table data-debug-files='{"backend":["api/users.py"]}'>...</table>
```

**B. `window.__uidevFiles` グローバルで宣言**

```html
<script>
  window.__uidevFiles = {
    html:    ["pages/user_list.html"],
    css:     ["styles/user_list.css"],
    js:      ["scripts/user_list.js"],
    backend: ["api/users.py"]
  };
</script>
```

A と B は併用可能(両方マージ)。動的に追加したいときは B、静的なら A が簡単。

---

## 操作

| 操作 | 結果 |
|---|---|
| 右下(または設定位置)の 🐛 をクリック | デバッグモーダルを開く |
| ヘッダーの「📋 コピー」ボタン | 関連ファイル + ログを JSON でクリップボードへ |
| `Ctrl + Shift + D` | モーダル開閉トグル |
| モーダル内のレベル/行数セレクタ | 表示・コピー対象を絞り込み(localStorage に保存) |
| ヘッダーの「ボタン位置」セレクタ | フロートボタンの配置を変更(localStorage に保存) |

---

## コピーされる JSON のスキーマ

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
    "entries": [
      { "ts": "ISO8601", "level": "log|info|warn|error|debug", "args": ["..."] }
    ]
  },
  "capturedAt": "ISO8601"
}
```

そのまま Claude Code に貼り付けて「これでデバッグして」と渡せる形式。

---

## 制約

- `uidev.js` は同一ページで複数回読み込まれても 1 回だけ初期化する(`window.__uidevLoaded` でガード)
- 本番ユーザー向け画面では読み込まないこと(debug-fab は開発用画面専用)
- ログバッファ上限は 2000 行(古いものから捨てる)
- このフォルダのテンプレートを各画面ごとにインラインで書き換えるのは禁止
  カスタマイズが必要な場合はプロジェクト側でフォークする
