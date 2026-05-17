# SKILL.jp.md — ui-kit:flocss-apply(日本語ミラー)

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更時は JP ミラーを先に更新し、その後 `SKILL.md` にも反映する。

---

**スキル名**: ui-kit:flocss-apply
**トリガー**: 画面に FLOCSS + Design Tokens を適用するとき。
新規画面の CSS 設計、既存画面の整理・トークン化、いずれもカバーする。
「FLOCSS で書き直して」「デザイントークンに揃えて」「新しい管理画面の CSS 設計して」など。

---

# ui-kit:flocss-apply — FLOCSS + Design Tokens 適用

FLOCSS のレイヤー構造と Design Tokens(CSS Custom Properties)を画面に適用する。
**新規画面**(ゼロからレイヤーを組む)と**既存画面**(現状のスタイルを FLOCSS レイヤーへ再分類)の両方を扱う。

---

## 作業内容

### ステップ1: 規約を読み込む

参照:

```
{plugin_root}/references/principles.md   # セクション 2(CSS アーキテクチャ)
```

要点:
- レイヤー: Foundation → Layout(`l-`)→ Object(`c-` Component / `p-` Project / `u-` Utility)
- 内部命名: BEM(`c-button__icon--large`)
- すべてのデザイン値は `:root` の CSS Custom Properties から
- 依存方向: 外側から内側へは触れない、横断的な変更はトークン経由

→ ステップ2へ

---

### ステップ2: モード判定(新規 vs 既存)

#### 処理内容

| シグナル | モード |
|---|---|
| 「新しい画面」「new screen」、まだ CSS がない | **新規** — ステップ3へ |
| 「既存」「書き直して」、既に CSS がある | **既存** — ステップ7へ |

不明な場合はユーザーに確認する。判定後、分岐する。

---

## 新規画面の流れ(ステップ3〜6)

### ステップ3: Foundation(トークン)を整備する

#### 処理内容

1. `static/css/foundation.css`(またはプロジェクトの CSS 場所)を作成または拡張する:
   - 最小リセット(margin/padding/box-sizing/フォント基本)
   - `:root` のデザイントークン:
     - `--color-*` — カラーパレット
     - `--space-*` — 4px または 8px グリッド
     - `--font-*` — body / mono スタック、サイズ、行高
     - `--radius-*`、`--shadow-*`
2. ダークモード予定があれば `:root[data-theme="dark"] { --color-bg: ...; ... }` を定義する。
3. 続行前にトークンをユーザーに確認する。

→ ステップ4へ

---

### ステップ4: Layout レイヤー(`l-`)を計画する

#### 処理内容

1. ページレベルのレイアウトブロック(ヘッダ・メイン・サイドバー・フッタ・グリッド枠組み)を洗い出す。
2. それぞれに `l-` クラスを作る: `l-page`, `l-grid`, `l-sidebar`, `l-main`。
3. Layout のルールでは余白等にトークン値のみを使う。

→ ステップ5へ

---

### ステップ5: Component(`c-`)と Project(`p-`)を計画する

#### 処理内容

1. 再利用可能なアトム/モレキュールを列挙 — これらが `c-*` になる(`c-button`, `c-card`, `c-input`)。
2. 画面固有のコンポジット(複数の `c-*` を組み合わせてドメイン的な意味を持つもの)を列挙 — `p-*`
   (`p-userList`, `p-loginForm`)。
3. 各々の BEM サブ構造をスケッチする: `c-button { } c-button__icon { } c-button--primary { }`。
4. CSS を生成する前にユーザーに構造を確認する。

→ ステップ6へ

---

### ステップ6: Utility(`u-`)を最小限追加する

#### 処理内容

1. 単発調整用のユーティリティを少量定義: `u-mt8`, `u-textCenter`, `u-hidden`。
2. 各ユーティリティは単一目的。コンポーネントスタイルをユーティリティで重複させない。
3. ユーティリティは独立ファイル `utility.css` に置き、読み込み順は最後。

→ ステップ11(共通最終ステップ)へ

#### 出力

- 読み込み順: `foundation.css`(reset + tokens)→ `layout.css`(`l-*`)→ `component.css`(`c-*`)→ `project.css`(`p-*`)→ `utility.css`(`u-*`)
- 詳細度が低くて予測可能

---

## 既存画面の流れ(ステップ7〜10)

### ステップ7: 現状のスタイルを棚卸しする

#### 処理内容

1. この画面に関連する既存の CSS ファイルを列挙する。
2. 各ルールを頭の中で分類する:
   - reset 相当 → Foundation
   - レイアウト構造 → Layout
   - 再利用ウィジェット → Component
   - 画面固有のコンポジット → Project
   - 単発ヘルパ → Utility
3. ハードコードされた値(色・余白・角丸など)でトークン化すべきものを特定する。

→ ステップ8へ

---

### ステップ8: Foundation トークンを導入・拡張する

#### 処理内容

1. `foundation.css`(相当)がなければ作成する。
2. 繰り返し出てくるハードコード値を `:root` トークンへ移す。
3. 使用箇所を `var(--token)` 参照に置換する。
4. トークン名は契約になるのでユーザーに確認する。

→ ステップ9へ

---

### ステップ9: クラス名を FLOCSS レイヤーへリネームする

#### 処理内容

1. レイアウトルール → `l-` プレフィックス(`.layout-grid` → `.l-grid`)。
2. 再利用ウィジェット → `c-` プレフィックス(`.button` → `.c-button`、サブ要素 `.c-button__icon`)。
3. 画面固有コンポジット → `p-` プレフィックス(`.user-list` → `.p-userList`)。
4. 単発ヘルパは `u-` プレフィックスへ、もしくはコンポーネント内へ吸収する。
5. 消費側を全て更新する — HTML マークアップ・JS の `querySelector`・テスト。

#### 補足

`.claude/rules/` の CSS-JS 紐付けルールが発火し、両側のチェックを要求する。指示に従う。

→ ステップ10へ

---

### ステップ10: 検証と仕上げ

#### 処理内容

1. `c-/p-/l-` ルール内にハードコードされたデザイン値が残っていないことを確認する。
2. `u-` ユーティリティが単一目的で、コンポーネントスタイルを重複させていないことを確認する。
3. 読み込み順を確認: foundation → layout → component → project → utility。
4. 画面が正しく描画されることを目視確認する。

→ ステップ11へ

#### 出力

- 既存スタイルが FLOCSS レイヤーへ再分類された
- ハードコード値がデザイントークンに統合された

---

## 共通の最終ステップ

### ステップ11: CSS-JS 紐付けルールを導入

#### 処理内容

プロジェクトに `.claude/rules/css-js-link.md` がなければ、以下からコピーする:

```
{plugin_root}/templates/rules/css-js-link.md
```

をプロジェクトルートの `.claude/rules/css-js-link.md` に配置する。

このルールは Claude が `.css`・`.js`・`.html` ファイルを読むときに自動でロードされ、
FLOCSS クラス定義と JS / HTML での使用箇所の紐付けを強制する。

→ 完了

#### 補足

- このステップは新規・既存どちらのパスにも適用される
- プロジェクトに既に存在するなら触らない
- プロジェクト独自の FLOCSS プレフィックス(`c-`/`p-`/`l-`/`u-` 以外)を使う場合は、
  コピー後にルール本文を編集してから commit する

---

## 参考資料

- `{plugin_root}/references/principles.md` — セクション 2(CSS アーキテクチャ)、セクション 1(DRY)
- FLOCSS リファレンス(外部): <https://github.com/hiloki/flocss>
