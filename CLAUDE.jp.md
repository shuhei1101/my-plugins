# CLAUDE.jp.md — my-plugins 開発者ガイド（日本語訳）

> このファイルは `CLAUDE.md` の日本語翻訳です。Claude Code には自動読み込みされません。内容を確認するための参照用ファイルです。
> 変更を加える場合は、まずこのファイルを更新し、その後 `CLAUDE.md`（本体）にも同じ変更を反映してください。

---

このリポジトリは Claude Code のプラグインマーケットプレイスです。スキルをプラグインとして配布・管理し、`/plugin` コマンドでインストールできます。

---

## 日本語翻訳ファイル（`.jp.md`）について

このリポジトリの英語ドキュメントには、対応する日本語翻訳ファイルがあります。

| 英語（自動読み込み） | 日本語（参照用） |
|---------------------|----------------|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `plugins/*/skills/*/SKILL.md` | `plugins/*/skills/*/SKILL.jp.md` |

**`.jp.md` ファイルは Claude Code に自動読み込みされません。** Claude Code が自動で読み込むのは `CLAUDE.md` と `SKILL.md` という名前のファイルのみです。`.jp.md` は人間が内容を確認するための参照専用ファイルです。

### 更新ワークフロー

ユーザーは `.jp.md` を読んで内容を理解し、日本語で指示します。変更が必要な場合：

1. **まず `.jp.md` を更新する** — 変更内容が日本語で正しく反映されているか確認する
2. **次に英語の本体を更新する** — 同じ変更を本体ファイルに反映する

両ファイルは常に同期を保つこと。片方だけ更新してはいけません。

---

## リポジトリ構成

```
my-plugins/
├── .claude-plugin/
│   └── marketplace.json       # プラグインカタログ（公開プラグインの一覧）
├── plugins/
│   └── {プラグイン名}/
│       ├── .claude-plugin/
│       │   └── plugin.json    # プラグインマニフェスト（名前・説明・バージョン）
│       └── skills/
│           └── {スキル名}/
│               ├── SKILL.md      # スキル定義（英語・自動読み込み）
│               └── SKILL.jp.md   # 日本語翻訳（参照用）
├── CLAUDE.md      # このファイルの英語本体（自動読み込み）
└── CLAUDE.jp.md   # このファイルの日本語翻訳（参照用）
```

---

## スキル設計ルール

このリポジトリのスキルはすべて **自動トリガー型** です（対話形式のウィザードではありません）。SKILL.md を書くときは以下のルールに従います。

- 内容はすべて **英語** で記述する
- **SKILL.md 一ファイルに全内容を入れる** — `references/` 等の外部ファイルは作らない（トリガーのたびに読み込みのレイテンシが発生するため）
- スキル本体に対話形式のステップメニューや選択肢を入れない
- `description` フィールドが自動トリガーの判定に使われる。具体的なコンテキストやユーザーが使いそうなフレーズを明示的に列挙し、少し「積極的」に書く
- SKILL.md は可能であれば 500 行以内に収める

### SKILL.md フロントマター

```yaml
---
name: {スキル名}
description: {いつトリガーするか、何をするか。具体的なコンテキストを書く}
---
```

オプションフィールド：

| フィールド | 説明 |
|-----------|------|
| `disable-model-invocation` | `true` にすると手動起動のみ（`/{プラグイン}:{スキル}`） |
| `allowed-tools` | スキル実行時に使用できるツール（例: `Read, Grep, Bash`） |
| `context` | `fork` を指定するとサブエージェントで実行 |

---

## 現在のプラグイン

| プラグイン | バージョン | 説明 |
|-----------|-----------|------|
| `wiki` | 1.0.0 | Issue 駆動の意思決定追跡を含むプロジェクトドキュメント Wiki 管理 |
| `py` | 1.0.0 | Python プロジェクトのコーディング規約 |
| `wt` | 1.0.1 | Git worktree を使った実装ワークフロー管理 |
| `claude-rule` | 1.0.0 | Claude 指示ファイルの記述規約（英語指示・日本語参照ファイルのペア管理） |
| `yaml-rule` | 1.0.0 | アセット・プロジェクト設定の YAML 管理規約（index.yaml / settings.yaml / 開発者ノート） |

---

## プラグイン作業ルール

プラグインの作成・更新手順（ワークツリーのセットアップ、ステップごとの作成ガイド、バージョンバンプルール）は `.claude/rules/plugin-work.md` に記載されています。このルールファイルは、Claude が `plugins/` や `.claude-plugin/` 配下のファイルを編集するときに自動ロードされます。

---

## プラグインコンポーネント一覧

プラグインにはスキル以外のコンポーネントも含められます：

```
plugins/{プラグイン名}/
├── .claude-plugin/
│   └── plugin.json      # 必須
├── skills/              # 自動トリガー・手動起動スキル
│   └── {スキル名}/
│       └── SKILL.md
├── agents/              # カスタムサブエージェント定義
│   └── {エージェント名}.md
├── hooks/               # フック設定
│   └── hooks.json
├── .mcp.json            # MCP サーバー設定
├── .lsp.json            # LSP サーバー設定
└── settings.json        # デフォルト設定
```

---

## このマーケットプレイスのインストール

### マーケットプレイスを追加

```bash
# URL 経由
/plugin marketplace add https://github.com/shuhei1101/my-plugins.git

# ローカルにクローン済みの場合
/plugin marketplace add ./my-plugins
```

### プラグインをインストール

```bash
/plugin install {プラグイン名}@my-plugins
```

スコープ：
- **User** — 全プロジェクトで有効（`~/.claude/settings.json`）
- **Project** — 全コラボレーターに共有（`.claude/settings.json`）
- **Local** — 自分のこのプロジェクトのみ（`.claude/settings.local.json`）

### 更新・管理

```bash
/plugin marketplace update my-plugins     # プラグイン一覧を最新化
/plugin disable {プラグイン名}@my-plugins
/plugin enable {プラグイン名}@my-plugins
/plugin uninstall {プラグイン名}@my-plugins
```

### チーム向け自動設定

プロジェクトの `.claude/settings.json` に追加：

```json
{
  "extraKnownMarketplaces": {
    "my-plugins": {
      "source": {
        "source": "url",
        "url": "https://github.com/shuhei1101/my-plugins.git"
      }
    }
  },
  "enabledPlugins": {
    "{プラグイン名}@my-plugins": true
  }
}
```

---

## 参考リンク

| トピック | URL |
|---------|-----|
| スキル | https://code.claude.com/docs/ja/skills |
| プラグイン | https://code.claude.com/docs/ja/plugins |
| プラグインのインストール | https://code.claude.com/docs/ja/discover-plugins |
| マーケットプレイス | https://code.claude.com/docs/ja/plugin-marketplaces |
| プラグインリファレンス（スキーマ） | https://code.claude.com/docs/ja/plugins-reference |
| サブエージェント | https://code.claude.com/docs/ja/sub-agents |
| フック | https://code.claude.com/docs/ja/hooks |
| MCP サーバー | https://code.claude.com/docs/ja/mcp |
