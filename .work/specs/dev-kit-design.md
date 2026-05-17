---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成（PR47）
related_specs:
  - py-kit-design.md
related_prs:
  - PR47
---

# dev-kit — 実装支援プラグイン設計仕様

## 概要

`dev-kit` は実装作業全般を支援する Claude Code プラグイン。
旧 `py-kit` と `yaml-rule` を統合し、`references/` というフラットな資料群と、
各種実装スキル（言語別・用途別）で構成される。

将来的に TypeScript / Java / Node.js / フロントエンド系の規約やスキルも
このプラグインに追加していくことを想定する。

## プラグイン構造

```
plugins/dev-kit/
├── .claude-plugin/
│   └── plugin.json
├── references/                    # フラット構造の資料群
│   ├── common.md                  # 全体共通（Markdown 等）
│   ├── frontend.md                # フロントエンド共通（HTML/CSS/JS）
│   ├── backend.md                 # バックエンド共通
│   ├── python.md                  # Python 共通規約
│   ├── yaml.md                    # YAML 規約
│   └── vscode-extension.md        # VS Code 拡張の作り方
└── skills/
    ├── py-script/                 # Python 簡易スクリプト作成
    ├── py-new-project/            # Python 新規プロジェクト作成
    ├── py-project/                # Python 既存プロジェクト対応
    └── yaml-rule/                 # YAML ファイル管理規約
```

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
| `plugins/py-kit/skills/py-new-project/` | `plugins/dev-kit/skills/py-new-project/` |
| `plugins/py-kit/skills/py-project/` | `plugins/dev-kit/skills/py-project/` |
| `plugins/yaml-rule/skills/yaml-rule/` | `plugins/dev-kit/skills/yaml-rule/`、規約部分は `plugins/dev-kit/references/yaml.md` に分離 |

## 拡張予定

将来追加する想定のあるリファレンス・スキル:

- `references/typescript.md` — TypeScript の書き方
- `references/java.md` — Java の書き方
- `references/nodejs.md` — Node.js の書き方
- VS Code 拡張機能作成スキル（`vscode-extension.md` をベース）
