---
created_at: 2026-05-18
updates:
  - 2026-05-18 — 初版作成(PR50)
related_specs:
  - dev-kit-design.md
  - ui-dev-design.md
related_prs:
  - PR50
---

# ui-kit — 開発用 UI コンポーネント + UI 規約 設計仕様

## 概要

`ui-kit` は開発支援画面に対して以下を提供する Claude Code プラグイン:

1. **コンポーネント提供スキル**: フロートデバッグボタンなど、画面に組み込む UI 部品
2. **UI 設計規約**: FLOCSS + Design Tokens、JS 規約、frontend-design 必須ルール
3. **横断スキル**: ログ整備、FLOCSS 適用

`dev-kit` は開発規約の置き場(Python/YAML 等)、`ui-kit` は UI に閉じた領域を担う。

## プラグイン構造

```
plugins/ui-kit/
├── .claude-plugin/
│   └── plugin.json
├── references/
│   ├── principles.md / principles.jp.md
│   │   ├ 共通化原則(DRY/centralization)
│   │   ├ CSS アーキテクチャ(FLOCSS + Design Tokens)
│   │   ├ JS 規約(`@ts-check` + JSDoc + レイヤー分け + インライン抑制)
│   │   └ frontend-design スキル必須ルール
│   └── ui-design.md / ui-design.jp.md
│       ├ ナビゲーション & レイアウト(サイドバー / 2 ペイン / トップタブ等)
│       ├ ヘッダー / サイドバー(PC) / ドロワー(モバイル)
│       ├ アクションボタン位置の固定ルール
│       ├ レスポンシブ(640 / 1024 ブレイクポイント、タッチターゲット 44px)
│       ├ 画面タイプ別パターン(トップ / 設定 / 一覧+詳細)
│       ├ フォーム・確認ダイアログ・キーボードショートカット
│       ├ 状態表示(loading/empty/error/toast)
│       ├ アクセシビリティ
│       ├ ダークモード
│       └ モーション規約
├── templates/
│   └── rules/
│       └── css-js-link.md   # FLOCSS クラス ↔ JS DOM アクセス紐付けルール(プロジェクトの .claude/rules/ にコピー)
└── skills/
    ├── debug-fab/           # フロートデバッグボタン + モーダル(旧 ui-dev)
    │   ├── SKILL.md / SKILL.jp.md
    │   └── templates/       # 共通モジュール(uidev.css/uidev.js/example.html)
    ├── logging/             # ログ整備スキル(レベル別ガイド)
    │   └── SKILL.md / SKILL.jp.md
    ├── flocss-apply/        # FLOCSS + Design Tokens 適用(新規/既存両対応)
    │   └── SKILL.md / SKILL.jp.md
    └── mock/                # 単一画面タイプの複数案モック生成(タブ切替)
        ├── SKILL.md / SKILL.jp.md
        └── templates/
            └── mock-skeleton.html
```

## references/principles.md の構成

### 1. 共通化原則

- 同じ概念を 2 箇所以上に書かない
- スタイルは Design Tokens(CSS Custom Properties)に集約
- DOM アクセスはセレクタ定数を共有モジュールで管理
- 紐付けは `.claude/rules/` で監査する

### 2. CSS アーキテクチャ — FLOCSS + Design Tokens

| レイヤー | プレフィックス | 内容 |
|---|---|---|
| Foundation | (なし) | リセット + Design Tokens(`:root` の CSS Custom Properties) |
| Layout     | `l-`   | ページレイアウト・グリッド(`l-grid`, `l-sidebar`) |
| Object — Component | `c-` | 再利用可能な小コンポーネント(`c-button`, `c-card`) |
| Object — Project   | `p-` | プロジェクト固有コンポーネント(`p-userList`, `p-loginForm`) |
| Object — Utility   | `u-` | 単機能ユーティリティ(`u-mt8`, `u-textCenter`) |

各コンポーネント内部は BEM 風: `c-button__icon--large`。

### 3. JS 規約

- 全ファイル先頭に `// @ts-check` を入れる
- 関数/変数/エクスポートは JSDoc 型注釈
- HTML へのインラインスクリプト(`<script>` 直書きや `onclick=`)は避ける
- バックエンド通信は `api/` レイヤーに分離
- UI 層 / 状態層 / API 層を明確に分割
- 関数型寄り(クラスではなく関数 + クロージャ)
- CSS クラス名と JS の DOM アクセスは紐付けルールで監査

### 4. frontend-design スキル必須ルール

UI 設計判断時は例外なく `frontend-design:frontend-design` スキルを使う(旧 dev-kit/references/frontend.md から移行)。

## スキル仕様

### debug-fab(旧 ui-dev)

開発系画面に必ず設置するフロートデバッグボタン + デバッグモーダル。
詳細は `ui-dev-design.md` 参照(本 PR で内容統合)。スキル名のみ `debug-fab` に変更。

### logging

ログ整備規約スキル。

レベル別ガイド(初版・Web 調査ベース、ユーザーレビュー後調整):
- `debug`    — 開発時のみの詳細トレース
- `info`     — 通常運用・ユーザー操作・状態遷移
- `warn`     — 回復可能な異常・リトライ・フォールバック
- `error`    — 注意が必要な失敗(処理は継続するが要対応)
- `critical` — システムが回復不能な障害(アラート対象)

共通ルール:
- JSON Lines 形式(必須フィールド: `ts` / `level` / `msg`)
- 操作ログを積極的に出す
- 1 行を短く保つ
- シークレット禁止
- 本番デフォルトレベルは `error`、開発時は `debug` に切替可能

### flocss-apply

FLOCSS + Design Tokens を画面に適用するスキル。

最初のステップで分岐:
- 新規 — Foundation → Layout → Object の順で骨格を作る
- 既存 — 既存スタイルを FLOCSS レイヤーへ再分類

両パス終了後、共通ステップで `.claude/rules/css-js-link.md` をプロジェクトに導入する。

### mock

単一画面タイプの複数デザイン案を上部タブ切替で単一 HTML に並べるスキル。

- 出力先: `tmp/mocks/{画面タイプ}-{日付}.html`
- 対応画面タイプ: トップ / 設定 / 一覧+詳細(テーブル系は対象外)
- 各案は意味のあるデザイン軸(レイアウト・密度・ナビゲーション等)で差をつける(色違いだけは NG)
- モバイル対応必須(`ui-design.md` のブレイクポイントに従う)
- 美的方向性は `frontend-design` スキルで確定し、案内で共有

## 移行

| 移行元 | 移行先 |
|---|---|
| `dev-kit/skills/ui-dev/` | `ui-kit/skills/debug-fab/`(改名) |
| `dev-kit/references/frontend.md`(frontend-design ルール) | `ui-kit/references/principles.md`(セクション統合) |
| `dev-kit/references/common.md`(ログ規約) | `ui-kit/skills/logging/SKILL.md` |

## バージョン

- ui-kit: 新規 v1.0.0
- dev-kit: 1.1.0 → 2.0.0(破壊的変更: ui-dev 削除、空 references 削除、common.md 削除)
