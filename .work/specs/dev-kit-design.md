---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成(PR47)
  - 2026-05-18 — UI 関連を ui-kit に分離。dev-kit は開発規約のみ(PR50)
related_specs:
  - py-kit-design.md
  - ui-kit-design.md
related_prs:
  - PR47
  - PR50
---

# dev-kit — 実装支援プラグイン設計仕様

## 概要

`dev-kit` は実装作業の**開発規約**を提供する Claude Code プラグイン。
言語別の規約資料(Python・YAML 等)と、各種実装スキル(言語別・用途別)で構成される。

UI 関連(フロントエンド規約・UI コンポーネント・ロギング)は PR50 で `ui-kit` プラグインに分離した。

将来的に TypeScript / Java / Node.js などのバックエンド系規約・スキルも
このプラグインに追加していくことを想定する。

## プラグイン構造

```
plugins/dev-kit/
├── .claude-plugin/
│   └── plugin.json
├── references/                    # フラット構造の資料群(言語別規約)
│   ├── python.md                  # Python 共通規約
│   └── yaml.md                    # YAML 規約
└── skills/
    ├── py-script/                 # Python 簡易スクリプト作成
    ├── py-project/                # Python プロジェクト全般(新規作成 + 既存対応を統合)
    └── yaml/                      # YAML ファイル管理規約
```

### スキル統合の方針

旧 `py-kit` には `py-new-project`（新規作成）と `py-project`（既存対応）の 2 スキルがあったが、
`dev-kit` では `py-project` 1 つに統合する。最初のステップで「新規 / 既存」を判定し、
既存プロジェクトの場合は分岐後のステップ（プロジェクト構造把握 → 品質チェック → 変更実装 …）から開始する。

## 設計方針

### references/ をフラットに置く理由

当初は `references/core/{frontend,backend,common}` と `references/language/{python,...}` の
2 階層構造も検討したが、

- 「フレームワーク」「拡張機能の作り方」など分類が曖昧なものが多い
- フラットの方がスキルからの参照パスが単純で取り回しが良い

ため、`references/` 直下にトピック別の `.md` を並べる形に統一した。

### スキルと references の関係

- スキルは実行ステップを定義する（手順・トリガー）
- references は規約・知識を定義する（参照される資料）
- スキルから `references/{topic}.md` を参照する形で連携する

## 移植元

| 移植元 | 移植先 |
|---|---|
| `plugins/py-kit/references/python-standards.md` | `plugins/dev-kit/references/python.md` |
| `plugins/py-kit/skills/py-script/` | `plugins/dev-kit/skills/py-script/` |
| `plugins/py-kit/skills/py-new-project/` + `py-project/` | `plugins/dev-kit/skills/py-project/`（統合） |
| `plugins/yaml-rule/skills/yaml-rule/` | `plugins/dev-kit/skills/yaml/`、規約部分は `plugins/dev-kit/references/yaml.md` に分離 |

## ui-kit への分離(PR50)

PR50 で UI 関連を `ui-kit` プラグインに切り出した:

| 移行元 | 移行先 |
|---|---|
| `dev-kit/skills/ui-dev/` | `ui-kit/skills/debug-fab/`(改名) |
| `dev-kit/references/frontend.md`(frontend-design ルール) | `ui-kit/references/principles.md` |
| `dev-kit/references/common.md`(ログ規約) | `ui-kit/skills/logging/` |

合わせて、雛形のみで実体がなかった以下の references を削除:
`backend.md` / `vscode-extension.md` / `html.md` / `css.md` / `js.md`

dev-kit のバージョンを 1.1.0 → 2.0.0 に bump(破壊的変更)。

## 拡張予定

将来追加する想定のあるリファレンス・スキル:

- `references/typescript.md` — TypeScript の書き方
- `references/java.md` — Java の書き方
- `references/nodejs.md` — Node.js の書き方
