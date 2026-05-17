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

**状態**: 未決定

`/rule-creator` で `.claude/rules/` 配下にルールを作成するが、対象パスとチェック内容を確定する必要あり:

候補内容:
- 対象 path: `**/*.css`, `**/*.js`, `**/*.html` または FLOCSS の各レイヤーごと
- トリガー: CSS クラス名追加・削除・改名時、JS の DOM アクセスが対応する CSS と紐づくか確認
- 命名規則(BEM)と DOM 取得(`document.querySelector(".c-Button__icon")`)の整合確認

**前提**: rule-creator スキル実行時にユーザーと相談しながら決定する。

---

## QA-009: ログレベル定義(`logging` スキル内容)

**状態**: 未決定

`logging` スキルに書くレベル別ガイドの初版は、Claude が Web 等を参考に「適当に」書き、ユーザーがレビューする方針。
具体的に何の出典・サイトをベースにするか:

- A: 業界一般のベストプラクティス(syslog レベル準拠:debug/info/notice/warning/error/critical/alert/emergency)
- B: Python `logging` モジュール準拠(DEBUG/INFO/WARNING/ERROR/CRITICAL)
- C: Web フロントエンドの実情に合わせて簡略化(debug/info/warn/error のみ、critical は重大事故時)

**前提**: TODO の現案は B(Python logging に揃える)+ ユーザーレビュー後に調整。
