# SKILL.jp.md — ui-kit:implement(日本語ミラー)

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更時は JP ミラーを先に更新し、その後 `SKILL.md` にも反映する。

---

**スキル名**: ui-kit:implement
**トリガー**: UI 画面の実装 — モック(`ui-kit:mock` 出力)や機能要件を実コードに落とす。
最初に共通リソース(定数・ルート・共通コンポーネント)を読み込み、再利用 / 拡張 / 新規追加を計画してから実装、最後にルールで紐付けるワークフローを強制する。
モック確定後の実装フェーズ、既存画面への機能追加、デザインのコード化など。
「モック確定したから実装して」「この画面に機能追加して」「モックを実装に落とし込んで」など。

---

# ui-kit:implement — 画面実装ワークフロー

モックや機能仕様を実コードに落とし込みつつ、プロジェクトの共通リソース(定数・ルート・コンポーネント)を
強制的に再利用させる。**画面ごとに独自実装が量産されるのを防ぐ**ためのスキル。

---

## 作業内容

### ステップ1: リファレンス読み込み

参照:

```
{plugin_root}/references/principles.md   # DRY / 共通化、FLOCSS、JS 規約
{plugin_root}/references/ui-design.md    # UX パターン、共通コンポーネント化必須
```

→ ステップ2へ

---

### ステップ2: 共通リソースを先に読む(必須)

#### 処理内容

コードを書く前に、プロジェクトの共通リソースを読み込む:

1. **定数ファイル** — 例: `static/js/constants.js`。デザイントークン、ブレイクポイント、API エンドポイント、デフォルト値
2. **ルートファイル** — 例: `static/js/routes.js`。既存ルート名、URL パターン、ルートテーブルの形
3. **コンポーネント層(CSS)** — 例: `static/css/component.css`(プロジェクトの `c-*` 定義)。既存コンポーネントをリスト化
4. **コンポーネント層(JS)** — 例: `static/js/components/`。共有コンポーネントモジュールをリスト化
5. **api/ レイヤー** — 既存の API ラッパーをリスト化

プロジェクトにまだ存在しないものがあれば、このステップ内で空スキャフォールド(`// @ts-check` ヘッダのみ)を作成してから先へ進む。**集約はオプションではない**。

→ ステップ3へ

#### 出力

- 共通リソースの所在メモ(何が、どこに、ある/ない)

#### 補足

##### 禁止事項

- インベントリ完了前に実装を始めない
- 「この画面には不要そう」と判断してファイルをスキップしない

---

### ステップ3: 再利用 / 拡張 / 新規追加の計画

#### 処理内容

モック(または機能仕様)を見て、各要素を 3 つのバケットに振り分ける:

| バケット | アクション |
|---|---|
| **再利用** | 既存の共通コンポーネントをそのまま使う(例: 既存の `c-button`) |
| **拡張**   | 既存コンポーネントにモディファイア / バリアントを追加(例: `c-button--ghost`)。変更は共有層に入れる、画面側ではない |
| **新規**   | 真に汎用的な新規コンポーネント → 共有層へ追加してから使う / 画面固有なら `p-*` 層へ |

計画を書き出して(チャットまたはコードコメント)、ユーザーに確認してから進める。

#### 出力

- 画面ごとの 再利用/拡張/新規 テーブル
- 各「新規」項目: どこに置くか(`c-*` 共有 or `p-*` 画面固有)

→ ステップ4へ

---

### ステップ4: 拡張ポイントの設計

#### 処理内容

新規コンポーネント・新規挙動には、**JSDoc 型を先に定義する**:

```js
// @ts-check

/** @typedef {"primary"|"secondary"|"ghost"|"danger"} ButtonVariant */
/** @typedef {{ label: string; variant?: ButtonVariant; onClick?: () => void; disabled?: boolean }} ButtonProps */
```

その後で型に対して実装を書く。型が契約となり、将来のバリアントがリファクタなしで収まるようになる。

ファクトリ / DI:

```js
/**
 * @param {{ api: Api; logger: Logger }} deps
 * @returns {{ submit: (form: FormData) => Promise<void> }}
 */
export const createSubmitHandler = ({ api, logger }) => ({ /* ... */ });
```

→ ステップ5へ

---

### ステップ5: 実装

#### 処理内容

1. 以下に従う:
   - FLOCSS レイヤー + Design Tokens(`principles.md` セクション 2)
   - `// @ts-check` + JSDoc 型(セクション 3)
   - アロー関数 + 関数引数 DI(セクション 3)
   - レイヤー分離 UI / State / API(セクション 3)
   - インライン `<script>` / `onclick` 禁止
   - すべての値は定数 / トークン / ルート経由 — ハードコード文字列・16 進カラー禁止
2. 新規共通コンポーネントは `c-*` 層へ先に置き、画面はそれを消費するのみ
3. 画面固有コンポジットは `p-{画面名}` 層(`p-userList`、`p-loginForm`)
4. JS の DOM セレクタは CSS のクラス名と一致(FLOCSS プレフィックス維持)

→ ステップ6へ

#### 出力

- 実装が共通化ルールに従って配置されている

---

### ステップ6: ルールを導入してファイル間を紐付ける(必須)

#### 処理内容

この画面で生成した JS/CSS/HTML が散らからないよう、英語版と日本語版の両ミラーをコピー
(コピー先が既に存在するペアはスキップ):

| コピー元(プラグイン) | コピー先(プロジェクト) |
|---|---|
| `{plugin_root}/templates/rules/css-js-link.md`              | `.claude/rules/css-js-link.md` |
| `{plugin_root}/templates/rules/css-js-link.jp.md`           | `.claude/rules-jp/css-js-link.md`(`.jp` サフィックスは落とす) |
| `{plugin_root}/templates/rules/common-component-first.md`   | `.claude/rules/common-component-first.md` |
| `{plugin_root}/templates/rules/common-component-first.jp.md`| `.claude/rules-jp/common-component-first.md` |

`.claude/rules/*.md` は Claude が対象ファイルを読むときに自動ロード、
`.claude/rules-jp/*.md` は人間用ミラー(Claude は読まない)。

プロジェクト固有の追加ルール(例: 特定の設定ファイル ↔ 特定の画面の紐付け)が必要なら、
`/rule-creator` で作成する。

→ 完了

#### 出力

- 紐付けルールが配置済み
- 次回この画面を編集すると、関連ルールが発火しクロスファイルチェックを促す

---

## 補足

- このスキルはモックが既にあるか機能仕様が明確な前提。どちらもないなら先に `/ui-kit:mock` を実行
  してフィードバックを集める。
- 共有層が未整備の新規プロジェクトでは、ステップ2でスキャフォールドファイルを作成する。
  これ以降の画面が同じ構造を継承する。

---

## 参考資料

- `{plugin_root}/references/principles.md` — DRY、FLOCSS、JS 規約
- `{plugin_root}/references/ui-design.md` — UX パターン、共通コンポーネント化必須
- `{plugin_root}/skills/mock/SKILL.md` — モック生成(コンパニオン)
- `{plugin_root}/skills/flocss-apply/SKILL.md` — CSS アーキテクチャ追加時
- `{plugin_root}/skills/logging/SKILL.md` — ロガー規約
