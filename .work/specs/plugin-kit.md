# plugin-creator スキル — 仕様書

## 概要

`claude-kit` プラグイン内のスキル（`/claude-kit:plugin-creator`）。
新規プラグイン作成を対話式にガイドし、`changelogs/` によるバージョン管理を標準化する。

## スキル一覧

| スキル名 | 呼び出し方 | 説明 |
|---|---|---|
| `plugin-creator` | `/claude-kit:plugin-creator` | 新規プラグインを作成する。バージョン管理フォルダ（`changelogs/`）も必ず生成する。 |

## plugin-creator スキル

### 目的

- `plugins/<name>/` 以下の標準ディレクトリ構造を対話式に生成する
- `changelogs/` フォルダを作成し、初回バージョン（`v1.0.0.md`）の変更履歴を記録する
- `marketplace.json` へのエントリ追加を案内する

### バージョン管理フォルダ構造

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
└── changelogs/
    ├── v1.0.0.md   # 初回リリースの変更履歴
    └── v1.1.0.md   # 次バージョン以降（更新時に追加）
```

### changelog ファイルの形式

```markdown
# v{X.Y.Z} — {YYYY-MM-DD}

## 変更内容

- {変更点1}
- {変更点2}

## 構造の変更

{ディレクトリ構造や設定ファイルの変更があれば記載}
```

### スキル実行フロー

1. プラグイン名・説明・バージョン・スキル名を確認
2. ディレクトリ構造を生成
3. `plugin.json` を作成
4. 各スキルの `SKILL.md` を作成
5. `changelogs/v{version}.md` を作成
6. `marketplace.json` へのエントリ追加を案内
