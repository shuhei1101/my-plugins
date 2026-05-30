<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->
# SKILL.jp.md — dev-kit:html-mock(日本語ミラー)

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更時は JP ミラーを先に更新し、その後 `SKILL.md` にも反映する。

---

**スキル名**: dev-kit:html-mock
**トリガー**: 1 つの画面タイプに対して複数案のモックを単一 HTML で生成するとき。
各案は意味のあるデザイン軸(レイアウト・密度・ナビゲーションパターン)で差をつける(色違いだけは不可)。
「設定画面のモック作って」「トップ画面の案出して」「一覧詳細のモック数パターン欲しい」など。

---

# dev-kit:html-mock — 複数案モックジェネレータ

1 つの画面タイプの複数デザイン案を単一 HTML ファイルにまとめ、上部のタブで切り替える形で出力する。
各案は `principles.md`(FLOCSS + Design Tokens、JS 規約)と `ui-design.md`(画面タイプ別 UX パターン)に従う。
出力先はプロジェクトの `tmp/mocks/`。

---

## 作業内容

### ステップ1: リファレンス読み込み + 共通リソースの棚卸し

#### 処理内容

1. 全文読み込み:

   ```
   {plugin_root}/references/html/principles.md   # FLOCSS、デザイントークン、JS 規約
   {plugin_root}/references/html/ui-design.md    # 画面タイプ別 UX パターン
   ```

2. **プロジェクトの共通リソースを棚卸しする**(モックでも必須 — 各案が並行に別物を作らないため):
   - `static/js/constants.js`(相当) — デザイントークン
   - `static/js/routes.js`(相当) — ルート名 / URL パターン
   - CSS のコンポーネント層 — `c-*` 定義
   - JS のコンポーネント層 — 共有コンポーネントモジュール

   まだない場合は不在を記録 — モックでも「ここにこれが入る」を示唆する。

プラグインルートはこのスキルファイルの2階層上。

→ ステップ2へ

---

### ステップ2: 画面タイプを確定

#### 処理内容

モックでどの**単一**画面タイプを探るかをユーザーに確認する:

| タイプ | 備考 |
|---|---|
| **トップ画面**       | サイドバーがカテゴリ列挙、メインにカードグリッド |
| **設定画面**         | セクション分けのフォーム行、スティッキーアクションバー、最下に Danger zone |
| **一覧 + 詳細**       | PC は 2 ペイン |

1 モック = 1 画面タイプ。複数の画面タイプを 1 HTML に混ぜない。

→ ステップ3へ

---

### ステップ3: 案のデザイン軸を決める

#### 処理内容

1. 案ごとに意味のある差を生むデザイン軸を 3〜5 個ピックアップ。例:
   - サイドバー型 vs トップタブ型
   - 密度の高いカードグリッド vs ゆとりのあるグリッド(2 列 vs 4 列)
   - 詳細を右ペイン vs モーダル
   - ライトテーマ vs ダーク基調
   - インライン編集 vs 別画面編集
2. 各案 = 比較する価値のある軸の組み合わせ
3. 色違い・文言違いだけの案は**生成しない**。Claude が検出して却下する
4. 生成前にユーザーに軸を確認する

→ ステップ4へ

---

### ステップ4: `frontend-design` スキルを適用

#### 処理内容

`principles.md` セクション 4 に従い、`frontend-design:frontend-design` スキルを呼び出して
モックの美的方向性(タイポグラフィ・配色・モーション・全体トーン)を確定する。

美的方向性は同じモックファイル内の全案で共有する(各案はレイアウト / パターンの差を見るためで、
美的差を見るためではない)。

→ ステップ5へ

---

### ステップ5: モック HTML を生成

#### 処理内容

**出力先をプロジェクト種別で分ける:**

| プロジェクト種別 | 出力先 | 理由 |
|---|---|---|
| FastAPI / Flask / Django など Web サーバーあり | サーバーが配信できる場所(後述) | 起動中のサーバー経由で即アクセスできるため |
| サーバーなし / 静的プロジェクト | `tmp/mocks/` | ローカルサーバーで配信する |

**FastAPI などのサーバープロジェクトの場合:**

1. モック画面を一覧できるページがすでにあるか確認する(例: `/dev/mocks`、`/debug/mocks` などの開発用ルート)
2. あればそのルートが読み込むテンプレートディレクトリに HTML を配置する(例: `templates/mocks/`, `app/templates/dev/`)
3. なければ開発用モックルートを新規作成し、テンプレートディレクトリを決めて HTML を配置する
4. ルーティング設定(例: `router.py`, `urls.py`)にモック一覧へのエントリを追加する

ファイル名は `{画面タイプ}-{YYYYMMDD}.html`(例: `settings-20260518.html`)。

ファイル構造:

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{画面タイプ} — Mock</title>
  <style>
    /* 自己完結モック用に FLOCSS をインラインで:
       Foundation(reset + tokens)→ Layout(l-*)→ Component(c-*)→ Project(p-*)→ Utility(u-*) */
  </style>
</head>
<body>

  <!-- ── 上部タブ ─────────────────────────────────────────── -->
  <nav class="l-mockTabs" role="tablist">
    <button class="l-mockTabs__tab" data-variant="a" aria-selected="true">案 A — {軸サマリ}</button>
    <button class="l-mockTabs__tab" data-variant="b" aria-selected="false">案 B — {軸サマリ}</button>
    <!-- ... 続く ... -->
  </nav>

  <!-- ── モック本体 — 案ごとに 1 セクション ────────────────── -->
  <main class="l-mockBody">
    <section data-variant="a" class="p-variant"> ... 案 A の内容 ... </section>
    <section data-variant="b" class="p-variant" hidden> ... 案 B の内容 ... </section>
    <!-- ... -->
  </main>

  <script>
    // @ts-check
    // タブ切替: クリックされたタブと一致するセクションを表示、他は隠す
  </script>
</body>
</html>
```

実装ルール:

- スタイルはすべて `<style>` 内にインライン(単一ファイルモック、外部 CSS なし)
- JS もすべて `<script>` 内にインライン(`// @ts-check` 必須)
- FLOCSS のレイヤー順を保つ
- デザイントークンは `:root` の Foundation 層に定義
- 各案セクションは選択された画面タイプに沿った完全レイアウト(サイドバー / ヘッダー / メイン)
- 案切替はタブ経由、表示は `hidden` 属性で 1 案ずつ

→ ステップ6へ

---

### ステップ6: サーバーを起動してURLをユーザーに伝える

#### 処理内容

**FastAPI などのサーバープロジェクトの場合:**

1. すでにサーバーが起動しているか確認する(`ps aux | grep uvicorn` など)
2. 起動済みであればそのポートをそのまま使う
3. 起動していなければ空きポートを探して起動する:
   ```bash
   # 空きポートを探す
   python -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()"
   # サーバー起動(例: FastAPI)
   uvicorn app.main:app --port {空きポート} --reload &
   ```
4. モック一覧ページのURL(例: `http://localhost:{port}/dev/mocks`)をユーザーに伝える

**サーバーなし / 静的プロジェクトの場合:**

1. 空きポートを探して `python -m http.server` でローカルサーバーを起動する:
   ```bash
   PORT=$(python -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
   python -m http.server $PORT --directory tmp/mocks &
   echo "http://localhost:$PORT/{ファイル名}.html"
   ```
2. 起動したURLをユーザーに伝える

**共通:**

- ユーザーに渡すのは**クリックすれば即開くURL**。ファイルパスだけを伝えない
- 各案の軸とURLをセットで伝える
- モック確定後は実装フェーズへ — `/dev-kit:html-implement` を推奨
  (実装時に共通リソース再利用を強制するため)

→ 完了

#### 出力

- モック HTML(サーバープロジェクトなら配信用テンプレートに、それ以外は `tmp/mocks/` に)
- ブラウザで即開けるURL
- 全案が `principles.md` + `ui-design.md` に準拠

---

## 参考資料

- `{plugin_root}/references/html/principles.md` — FLOCSS、デザイントークン、JS 規約
- `{plugin_root}/references/html/ui-design.md` — 画面タイプ別 UX パターン
- `{plugin_root}/skills/mock/templates/mock-skeleton.html` — モック雛形 HTML
