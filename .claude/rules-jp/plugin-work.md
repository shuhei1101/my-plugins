---
name: plugin-work
description: プラグインの作成・更新手順のルール。plugins/** 配下のファイルを編集するときに自動ロードされる。
type: reference
paths:
  - "plugins/**"
  - ".claude-plugin/**"
---

> このファイルは `.claude/rules/plugin-work.md` の日本語訳です。Claude Code には自動読み込みされません。内容を確認するための参照用ファイルです。
> 変更を加える場合は、まずこのファイルを更新し、その後 `.claude/rules/plugin-work.md`（本体）にも同じ変更を反映してください。

---

# プラグイン作業ルール

## 前提：必ずワークツリーを使う

新しいプラグインを作成する場合も、既存プラグインを更新する場合も、**必ず `wt` スキルを使ってワークツリーとブランチを作成してから作業を開始すること**。

```bash
/wt:wt
```

メインブランチ上で直接作業してはいけない。

---

## プラグインファイルを編集したら必ずやること

**コミット前に、バージョンが記載されている 2 箇所を必ず更新する：**

- [ ] `plugins/{プラグイン名}/.claude-plugin/plugin.json` — `version` をバンプ
- [ ] `.claude-plugin/marketplace.json` — 対応するプラグインの `version` をバンプ

どちらかを忘れると、カタログとインストール済みプラグインのバージョンがずれてしまう。

---

## 新しいプラグインの作成手順

### 1. プラグインディレクトリを作成

```
plugins/{プラグイン名}/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── {スキル名}/
        └── SKILL.md
```

### 2. plugin.json を書く

```json
{
  "name": "{プラグイン名}",
  "description": "{このプラグインが何をするかの短い説明}",
  "version": "1.0.0"
}
```

フィールドのルール：
- `name`: kebab-case の識別子。スキルの名前空間としても使われる
- `version`: セマンティックバージョニング（`MAJOR.MINOR.PATCH`）

### 3. SKILL.md を書く

```markdown
---
name: {スキル名}
description: {いつトリガーするか、何をするか。具体的なフレーズとコンテキストを含める}
---

# {スキルタイトル}

{スキルの説明（英語で記述）。外部参照ファイルは作らず、全内容をここに書く}
```

### 4. marketplace.json に登録

`.claude-plugin/marketplace.json` のエントリを追加：

```json
{
  "name": "{プラグイン名}",
  "source": "./plugins/{プラグイン名}",
  "description": "{plugin.json の description と同じ}",
  "version": "1.0.0"
}
```

### 5. ローカルでテスト

```bash
# プラグイン単体でテスト
claude --plugin-dir ./plugins/{プラグイン名}

# マーケットプレイス全体でテスト
claude
/plugin marketplace add ./
/plugin install {プラグイン名}@my-plugins   # スコープは Local を選択
```

インストール後、スキルが正しくトリガーされることを確認。テスト完了後はクリーンアップ：

```bash
/plugin uninstall {プラグイン名}@my-plugins
/plugin marketplace remove my-plugins
```

---

## 既存プラグインの更新

### バージョンバンプの規則

| 変更の種類 | バンプ | 例 |
|-----------|--------|---|
| バグ修正・小さな修正 | PATCH（`1.0.0` → `1.0.1`） | コマンドの誤り修正、ロジックのタイポ |
| 新しいセクション・新機能追加 | MINOR（`1.0.0` → `1.1.0`） | ワークフローのセクション追加 |
| 完全な書き直し・破壊的変更 | MAJOR（`1.0.0` → `2.0.0`） | スキル全体のアプローチを刷新 |
