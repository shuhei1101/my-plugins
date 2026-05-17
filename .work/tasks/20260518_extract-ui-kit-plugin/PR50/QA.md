# QA — PR50 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX(連番)として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: プラグイン構成

**状態**: 決定済み(2026-05-18)

- 新規プラグイン: `ui-kit`(v1.0.0)
- 既存 `dev-kit` は破壊的変更(UI 関連を切り出し): 1.1.0 → 2.0.0
- 役割: dev-kit = 開発規約 / ui-kit = 開発用 UI コンポーネント + UI 規約

---

## QA-002: ui-kit references 構成

**状態**: 決定済み(2026-05-18)

ファイルは `principles.md`(+ JP)1 本に集約。
セクション構成:
1. 共通化原則(DRY/centralization)
2. CSS アーキテクチャ — FLOCSS + Design Tokens(CSS Custom Properties)
3. JS 規約 — `// @ts-check` + JSDoc 型注釈、レイヤー分け、過度なインライン抑制
4. frontend-design スキル必須(dev-kit/references/frontend.md から移行)

---

## QA-003: スキル構成

**状態**: 決定済み(2026-05-18)

ui-kit/skills/:
- `debug-fab` — 旧 ui-dev を改名・移植(フロートデバッグボタン + モーダル)
- `logging` — ログ整備スキル(出力レベル別 debug/info/warn/error/critical の指針)
- `flocss-apply` — FLOCSS + Design Tokens を画面に適用(新規/既存両対応、最初のステップで分岐)

---

## QA-004: dev-kit から削除する references

**状態**: 決定済み(2026-05-18)

中身が雛形のみ・実体なしのものを全て削除:
- `backend.md` / `backend.jp.md`
- `vscode-extension.md` / `vscode-extension.jp.md`
- `html.md` / `html.jp.md`(空)
- `css.md` / `css.jp.md`(空)
- `js.md` / `js.jp.md`(空)
- `frontend.md` / `frontend.jp.md` — 内容(frontend-design 必須ルール)は ui-kit/principles.md に移行のうえ削除
- `common.md` / `common.jp.md` — ログ規約は ui-kit/skills/logging に移行のうえ削除

残す: `python.md` / `yaml.md`(+ JP)

---

## QA-005: CSS 設計

**状態**: 決定済み(2026-05-18)

**FLOCSS + Design Tokens(CSS Custom Properties)** を採用。
レイヤー: Foundation(reset + tokens)→ Layout(`l-`)→ Object(`c-` Component / `p-` Project / `u-` Utility)
コンポーネント内部は BEM 風の Block-Element-Modifier 命名。

---

## QA-006: JavaScript 規約

**状態**: 決定済み(2026-05-18)

- バニラ JS + `// @ts-check` ファイル先頭ディレクティブ
- JSDoc 型注釈(`@param`/`@returns`/`@typedef`)を必須にする
- インラインスクリプトは最小限(ハンドラを HTML に書かない)
- バックエンド通信はモジュール分離(`api/` などのレイヤー)
- レイヤー分け:UI 層 / 状態層 / API 層を明確化
- 関数型寄り(クラスではなく関数 + クロージャ中心)
- CSS クラス名と JS 側 DOM アクセスを紐付けるルールを `.claude/rules/` に作成

---

## QA-007: TypeScript 採用

**状態**: 決定済み(2026-05-18)

採用しない(Node.js / ビルドツール導入の負担を回避するため)。
代替として `// @ts-check` + JSDoc 型注釈で型ヒントを得る。

---

## QA-008: CSS-JS 紐付けルール

**状態**: 決定済み(2026-05-18)

スコープ: **FLOCSS 定義クラス ↔ JS 取得**。
CSS で定義された `.c-*` / `.p-*` / `.l-*` / `.u-*` クラスと、JS の `querySelector`/`getElementById` 等の DOM 取得式を紐付け、片方の変更時に他方の同期確認を促す。

`/rule-creator` で `.claude/rules/{name}.md` を作成。

---

## QA-009: ログレベル定義(`logging` スキル内容)

**状態**: 決定済み(2026-05-18)

**Web 実情版**: `debug` / `info` / `warn` / `error` の 4 段階。
critical は `error` に統合(重大事故も同じレベル)。Web フロントエンドの実情に合わせた最小構成。

---

## QA-010: JS 規約の必須化レベル

**状態**: 決定済み(2026-05-18)

バニラ JS + `// @ts-check` + JSDoc 型注釈を**必須**化(principles.md に明記)。
TypeScript / Node.js 環境は導入しない。

---

## QA-011: `mock` スキル仕様

**状態**: 決定済み(2026-05-18)

- スキル名: `ui-kit:mock`
- 出力形式: 単一 HTML ファイル(タブで案を切り替え、目安 A〜E)
- タブ位置: 画面最上部、案数は内容次第
- 画面下部にモック本体を表示
- PC + モバイル両対応(レスポンシブ)
- 出力先: ユーザーのプロジェクト内 `tmp/mocks/`(.gitignore 推奨)
- 粒度: 1 画面タイプ × 複数案(画面タイプを混ぜない)
- 対応画面タイプ: 設定画面 / 一覧 + 詳細画面 / トップ画面(サイドメニュー + ツールカード列)
- テーブル画面は不要

---

## QA-012: `ui-design.md` に書く内容(凡例 + 追加候補)

**状態**: 決定済み(2026-05-18)

採用: ユーザー明示トピック + **A + B + C + D 全部**

ユーザーから明示されたトピック:
- 画面操作系: タブ切替・サイドメニュー多用
- レイアウト: 2 ペイン / 3 ペイン構造
- アクションボタン(保存等)の位置固定化
- ヘッダー構成
- サイドメニュー(PC 固定 / モバイルドロワー、サイドメニューに入れる内容のガイド)
- 「ホームに戻る」動線はサイドメニュー経由
- レスポンシブ:PC サイドメニュー → モバイルドロワー、2 ペイン → モバイル画面遷移

### Claude からの追加候補(QA で要選定)

A: フィードバック・状態系
- 読み込み中(skeleton / spinner)
- 空状態(empty state)の文言とビジュアル
- エラー状態 / トースト通知パターン

B: 入力系
- フォームバリデーション表示(inline error vs サマリ)
- 確認ダイアログ(取り消し不能アクション)
- キーボードショートカット規約

C: アクセシビリティ・モバイル詳細
- レスポンシブブレイクポイントの定義(PC / タブレット / モバイル)
- タッチターゲット最小サイズ(44px)
- ダークモード切替パターン

D: モーション
- アニメーション・トランジション規約(目的のある最小限)

**前提**: 全部入れたい場合は A〜D 全部、最小ならユーザー明示トピック + A のみ等。

