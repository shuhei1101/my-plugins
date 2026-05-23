# plugin-creator スキル — 仕様書

## 概要

`claude-kit` プラグイン内のスキル（`/claude-kit:plugin-creator`）。
プラグインの新規作成・更新を対話式にガイドし、`changelogs/` によるバージョン管理を標準化する。

## スキル一覧

| スキル名 | 呼び出し方 | 説明 |
|---|---|---|
| `plugin-creator` | `/claude-kit:plugin-creator` | プラグインの新規作成・更新。バージョン管理（`changelogs/`）を必ず実施する。 |

## plugin-creator スキル

### 目的

- 新規作成・更新の両モードに対応
- `plugins/<name>/` 以下の標準ディレクトリ構造を対話式に生成・更新する
- バージョンバンプ（MAJOR/MINOR/PATCH）を判定し `plugin.json` と `marketplace.json` を更新する
- `changelogs/v{version}.md` を毎回作成し変更履歴を記録する

### バージョン管理フォルダ構造

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       └── SKILL.jp.md
└── changelogs/
    ├── v1.0.0.md   # 初回リリースの変更履歴
    └── v1.1.0.md   # 次バージョン以降（更新時に追加）
```

### バージョンバンプ基準

| 変更種別 | バンプ |
|---|---|
| バグ修正・軽微な修正 | PATCH（`1.x.y` → `1.x.y+1`） |
| 新スキル追加・動作変更 | MINOR（`1.x.0` → `1.x+1.0`） |
| 全面的な再設計 | MAJOR（`1.0.0` → `2.0.0`） |

### changelog ファイルの形式

```markdown
# v{X.Y.Z} — {YYYY-MM-DD}

## 変更内容

- {変更点1}
- {変更点2}

## 構造の変更

{ディレクトリ構造や設定ファイルの変更があれば記載。なければ「なし」と書く。}
```

### スキル実行フロー（新規作成）

1. モード確認（create）
2. プラグイン名・説明・スキル名を確認
3. ディレクトリ構造を生成（`SKILL.md` + `SKILL.jp.md` 含む）
4. `plugin.json`（v1.0.0）を作成
5. `changelogs/v1.0.0.md` を作成
6. `marketplace.json` へのエントリ追加

### スキル実行フロー（更新）

1. モード確認（update）・現バージョン確認
2. 変更内容と変更種別を確認
3. 対象スキルファイルを編集
4. `plugin.json` バージョンをバンプ・`marketplace.json` も更新
5. `changelogs/v{NEW_VERSION}.md` を作成
