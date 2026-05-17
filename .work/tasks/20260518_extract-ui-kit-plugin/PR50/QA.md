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

ただし A〜D は「**共通コンポーネントとして定義**しておく」方針を ui-design.md に明記する。
各画面で独自実装しない(loading/empty/error/toast、フォーム、a11y 部品、モーションすべて共通化)。

---

## QA-013: JSDoc 型表現の範囲

**状態**: 決定済み(2026-05-18)

JSDoc + `// @ts-check` で以下を活用する(principles.md に追記):
- リテラル型: `@typedef {"draft"|"published"|"archived"} Status`
- 型エイリアス: `@typedef {{ id: string; name: string }} User`
- ユニオン / インターセクション
- ジェネリクス(`@template T`)
- 関数の引数注入(コンストラクタ注入相当)

「クラスはほぼ不要」「アロー関数中心」を明確にする。

---

## QA-014: AI 前提の拡張性設計

**状態**: 決定済み(2026-05-18)

「AI が実装するからスモールスタート / YAGNI で良い」ではなく、**最初から拡張性高めに作る**。
- ハードコードは避け、定数 / トークン / Protocol-like (JSDoc `@typedef`) で抽象化
- 「とりあえずハードコード」を禁止
- principles.md に明示

---

## QA-015: 集約規約(ルーティング・定数)

**状態**: 決定済み(2026-05-18)

- **ルーティング**: 1 ファイルに集約(例: `static/js/routes.js`)。各画面から URL ハードコード禁止
- **定数**: 1 ファイルに集約(例: `static/js/constants.js`)。ブレイクポイント・色トークン参照・APIエンドポイントなど
- principles.md に明記

「画面のデザインを設定する画面」(定数を GUI から編集)はオプション・任意機能としてメモに残す。

---

## QA-016: 共通コンポーネント先読みの強制

**状態**: 決定済み(2026-05-18)

UI 実装系スキル(mock / implement / flocss-apply / debug-fab / logging)では最初のステップで
**共通コンポーネント / constants / routing を必読**にする。これに違反すると画面ごとに独自実装が
量産されるため。

仕組み:
- 各 SKILL.md の Step 1 に「共通コンポーネント / 定数 / ルーティングを確認」と明記
- `plugins/ui-kit/templates/rules/common-component-first.md` をテンプレートとして提供
- 関連スキルの実行時に `.claude/rules/` にコピー(`flocss-apply` のステップ 11 同様の方式)

---

## QA-017: 新スキル `ui-kit:implement`

**状態**: 決定済み(2026-05-18)

モック確定後の実装フェーズ用スキル:

1. **構造把握**: 既存 constants / routing / 共通コンポーネント(`c-*` / `p-*`)を読み込む
2. **設計フェーズ**: モックを分解し、何を共通化するか / 既存を再利用するか / 新規追加するかを計画する
3. **拡張ポイント計画**: 将来の追加にも耐える構造(JSDoc 型・関数引数注入)を選ぶ
4. **実装**: 計画に従い、constants / routing / 共通コンポーネントを必ず経由する
5. **ルール連携**: 終了時に `/rule-creator` で生成された JS/CSS/HTML を紐付ける

「実装フェーズで constants も routing も共通コンポーネントも見ないで独自に作る」を防ぐのが目的。

---

## QA-018: 最終ステップでルール連携を明記

**状態**: 決定済み(2026-05-18)

`mock` / `implement` / `flocss-apply` の最終ステップで:
- 生成された JS/CSS/HTML が散らからないよう、`/rule-creator` でルール作成 or 既存ルール導入を促す
- 既に `css-js-link.md` がコピーされていれば導入済み扱い

---

## QA-019: ルールテンプレートの多言語化

**状態**: 決定済み(2026-05-18)

ユーザー運用に合わせる:
- `.claude/rules/` (英、Claude が自動読み込み)
- `.claude/rules-jp/` (日、人間用ミラー、Claude 読み込み対象外)

プラグイン側 templates 構造:
```
plugins/ui-kit/templates/rules/
├── css-js-link.md           → user .claude/rules/css-js-link.md
├── css-js-link.jp.md        → user .claude/rules-jp/css-js-link.md  (.jp サフィックスは落とす)
├── common-component-first.md       → user .claude/rules/common-component-first.md
└── common-component-first.jp.md    → user .claude/rules-jp/common-component-first.md
```

flocss-apply / implement スキルが両方をコピーする。

---

## QA-021: flocss-apply と implement の統合

**状態**: 決定済み(2026-05-18)

`flocss-apply` の機能は `implement` の構造把握 + 実装ステップに内包される。
両者で「ルール導入」テーブルが重複していたこともあり、**`flocss-apply` を `implement` に統合して削除**する。

統合後の `implement` ステップ:
1. リファレンス読み込み
2. 共通リソース棚卸し
3. **FLOCSS セットアップ**(未整備なら Foundation→Layout→Object 構築 / 既存 CSS あるが FLOCSS でないなら再分類)
4. 再利用 / 拡張 / 新規追加 の振り分け
5. JSDoc 型を先に書く
6. 実装
7. ルール導入(EN+JP 両方コピー)

ui-kit/skills は `debug-fab` / `logging` / `mock` / `implement` の 4 つに集約。

---

## QA-020: 共通コンポーネントの具体例

**状態**: 決定済み(2026-05-18)

ui-design.md の「共通コンポーネント化必須」セクションに、よく使う部品を明示:
- Header(ヘッダー)
- Sidebar / Drawer(サイドバー / ドロワー)
- Buttons(各種ボタン variant)
- FAB(Floating Action Button)
- Modal / Dialog(モーダル / 確認ダイアログ)
- Toast(通知)
- Form Field(ラベル + 入力 + エラー)
- Loading Skeleton / Spinner
- Empty State Card
- Tab Bar / Card Grid / Action Bar
- その他、複数画面で使い回す可能性のあるものはここに集約

運用ガイドとして「よく使うものはここに入れましょう」を明文化。

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

