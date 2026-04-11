# Claude Plugins

Claude Code プラグインのマーケットプレイスです。
スキル・エージェント・フックなどをプラグインとして配布・管理します。

- [1. マーケットプレイスとは](#1-マーケットプレイスとは)
- [1.1. 構築手順](#11-構築手順)
- [2. ディレクトリ構成](#2-ディレクトリ構成)
- [3. 【利用者向け】プラグインのインストール・管理](#3-利用者向けプラグインのインストール管理)
- [3.1. Git の認証設定](#31-git-の認証設定)
- [3.2. マーケットプレイスの追加](#32-マーケットプレイスの追加)
- [3.3. プラグイン一覧の確認](#33-プラグイン一覧の確認)
- [3.4. プラグインのインストール](#34-プラグインのインストール)
- [3.5. プラグインの管理](#35-プラグインの管理)
- [3.6. プロジェクトへの自動設定（チーム利用）](#36-プロジェクトへの自動設定チーム利用)
- [4. 【開発者向け】プラグインの作成・編集・公開](#4-開発者向けプラグインの作成編集公開)
- [4.1. 編集対象チェックリスト](#41-編集対象チェックリスト)
- [4.2. リポジトリのクローン](#42-リポジトリのクローン)
- [4.3. 開発ブランチの作成](#43-開発ブランチの作成)
- [4.4. 新しいプラグインの作成・動作確認](#44-新しいプラグインの作成動作確認)
- [4.5. プラグインで利用可能なコンポーネント](#45-プラグインで利用可能なコンポーネント)
- [4.6. 変更の公開](#46-変更の公開)
- [5. 参考リンク（公式ドキュメント）](#5-参考リンク公式ドキュメント)


## 1. マーケットプレイスとは

Claude Code のプラグイン配布基盤です。Git リポジトリに `marketplace.json` とプラグインを配置し、 CLI からインストール・更新できる仕組みです。

### 1.1. 構築手順

1. マーケットプレイス用のリモートリポジトリを作成
2. `marketplace.json` を作成し、プラグイン（スキル等）を配置
3. 各メンバーがマーケットプレイスを追加: `/plugin` → `Add Marketplace` → リポジトリURLを入力
4. 必要なプラグインをインストール: `/plugin` → `Marketplaces` → 指定のマーケットプレイスを選択 → `Browse plugin` → いずれかのプラグインを選択しインストール

> **補足**
> - マーケットプレイスやプラグインのインストールは対話ベース以外に shell コマンドからも可能
> - マーケットプレイスの追加はプロジェクト配下の `.claude/settings.json` に記載することでクローン時に自動で追加が可能

---

## 2. ディレクトリ構成

```
my-plugins/
├── .claude-plugin/
│ └── marketplace.json # プラグインカタログ（プラグイン一覧）
├── plugins/
│ ├── <plugin-name>/ # 各プラグイン
│ │ ├── .claude-plugin/
│ │ │ └── plugin.json # プラグインのマニフェスト
│ │ ├── skills/
│ │ │ └── <skill-name>/
│ │ │ └── SKILL.md # スキル定義
│ │ ├── agents/
│ │ │ └── <agent-name>.md # エージェント定義
│ │ ├── hooks/
│ │ │ └── hooks.json # フック設定
│ │ └── .mcp.json # MCP サーバー設定
│ └── ...
└── README.md
```

---

## 3. 【利用者向け】プラグインのインストール・管理

### 3.1. マーケットプレイスの追加

このマーケットプレイスを利用するには、まず Claude Code にマーケットプレイスを登録します。

#### コマンドベースの場合

```bash
# Git URL で追加
/plugin marketplace add https://github.com/shuhei1101/my-plugins.git

# 特定のブランチを指定して追加（#ブランチ名）
/plugin marketplace add https://github.com/shuhei1101/my-plugins.git#feat/xxx/test_branch

# ローカルにクローン済みの場合はパスで追加
/plugin marketplace add ./my-plugins
```

#### CLI 対話形式の場合

1. Claude Code のセッション内で `/plugin` と入力
2. **Marketplaces** タブに移動
3. **Add marketplace** を選択
4. リポジトリURL `https://github.com/shuhei1101/my-plugins.git` を入力

### 3.2. プラグイン一覧の確認

マーケットプレイスの追加後、利用可能なプラグインを確認できます。

#### コマンドベース

```bash
/plugin marketplace list
```

#### CLI 対話形式

1. `/plugin` と入力
2. **Discover** タブに移動 — マーケットプレイスに登録されているプラグイン一覧が表示されます

### 3.3. プラグインのインストール

一覧から必要なプラグインを選んでインストールします。

#### コマンドベースの場合

```bash
# プラグインをインストール（ユーザースコープ：全プロジェクトで有効）
/plugin install sample-plugin@my-plugins

# プロジェクトスコープでインストール（チーム全員に共有）
claude plugin install sample-plugin@my-plugins --scope project
```

インストール後、変更を反映するために以下を実行します:

```bash
/reload-plugins
```
- うまく行かない場合は、セッションを再起動してください。

#### CLI 対話形式の場合

1. Claude Code のセッション内で `/plugin` と入力
2. **Discover** タブに移動
3. インストールしたいプラグインを選択
4. スコープを選択:
- **User scope** — 自分の全プロジェクトで有効（`~/.claude/settings.json` に追加される）
- **Project scope** — このリポジトリの全コラボレーターに共有（`.claude/settings.json` に追加される）
- **Local scope** — 自分のみ、このリポジトリでのみ有効（`.claude/settings.local.json` に追加される）

### 3.4. プラグインの管理

```bash
# インストール済みプラグインの確認
/plugin # Installed タブで確認

# プラグインの無効化
/plugin disable sample-plugin@my-plugins

# プラグインの再有効化
/plugin enable sample-plugin@my-plugins

# プラグインのアンインストール
/plugin uninstall sample-plugin@my-plugins

# マーケットプレイスの更新（最新のプラグイン一覧を取得）
/plugin marketplace update my-plugins
```

### 3.5. プロジェクトへの自動設定（チーム利用）

プロジェクトの `.claude/settings.json` に以下を追加すると、チームメンバーがリポジトリを信頼した際に自動でマーケットプレイスが提案されます:

```json
{
"extraKnownMarketplaces": {
"claude-plugins": {
"source": {
"source": "url",
"url": "https://github.com/shuhei1101/my-plugins.git"
}
}
},
"enabledPlugins": {
"sample-plugin@my-plugins": true
}
}
```

---

## 4. 【開発者向け】プラグインの作成・編集・公開

### 4.1. 編集対象チェックリスト

プラグインの新規作成・編集時に必要な作業:

- [ ] `.claude-plugin/marketplace.json` — プラグインの追加・削除・バージョン更新
- [ ] `plugins/<name>/.claude-plugin/plugin.json` — プラグインのメタデータ変更
- [ ] `plugins/<name>/` 配下のコンポーネント — プラグインの内容変更（スキル・エージェント・フック・MCP 等）

### 4.2. リポジトリのクローン

```bash
git clone https://github.com/shuhei1101/my-plugins.git
cd my-plugins
```

### 4.3. 開発ブランチの作成

ブランチ命名規則: `feat/{自身の名前}/{作業概要}`

```bash
# 例: 新規プラグイン作成
git checkout -b feat/name/create_my-new-plugin

# 例: 既存プラグイン更新
git checkout -b feat/name/update_sample-plugin
```

### 4.4. 新しいプラグインの作成・動作確認

#### 1. プラグインディレクトリの作成

```bash
mkdir -p plugins/<plugin-name>/.claude-plugin
mkdir -p plugins/<plugin-name>/skills/<skill-name>
```

#### 2. プラグインマニフェストの作成

`plugins/<plugin-name>/.claude-plugin/plugin.json` を作成します。

例: `code-reviewer` というプラグインを作る場合 → `plugins/code-reviewer/.claude-plugin/plugin.json`

```json
{
"name": "code-reviewer",
"description": "PRのコードレビューを支援するプラグイン",
"version": "1.0.0",
"author": {
"name": "{作成者名}"
}
}
```

| フィールド | 必須 | 説明 |
| ------------- | ---- | -------------------------------------------------------------- |
| `name` | Yes | プラグインの識別子（kebab-case）。スキルの名前空間にも使われる |
| `description` | Yes | プラグインの説明 |
| `version` | Yes | セマンティックバージョニング（例: `1.0.0`） |
| `author` | No | 作成者情報 |

#### 3. スキルの作成

`plugins/<plugin-name>/skills/<skill-name>/SKILL.md` を作成します。

例: `code-reviewer` プラグインに `review` スキルを追加 → `plugins/code-reviewer/skills/review/SKILL.md`

```markdown
---
name: review
description: PRの差分をレビューし、バグ・セキュリティ・パフォーマンスの問題を指摘する。
disable-model-invocation: true
---

# コードレビュー

以下の観点でコードをレビューしてください:

1. バグや境界値の見落とし
2. セキュリティ上の懸念
3. パフォーマンスの問題

指摘は簡潔かつ具体的に。
```

呼び出し方: `/code-reviewer:review`

主要なフロントマターフィールド:

| フィールド                 | 説明                                                     |
| -------------------------- | -------------------------------------------------------- |
| `name`                     | スキル名（省略時はディレクトリ名）                       |
| `description`              | スキルの説明（Claude の自動判定に使用）                  |
| `disable-model-invocation` | `true` にすると手動起動のみ（`/plugin-name:skill-name`） |
| `allowed-tools`            | スキル実行時に使用可能なツール（例: `Read, Grep, Bash`） |
| `context`                  | `fork` を指定するとサブエージェントで実行                |

#### 4. マーケットプレイスへの登録

`.claude-plugin/marketplace.json` の `plugins` 配列に新しいプラグインのエントリを追加します。

```json
{
"plugins": [
...
# 以下を追加する
{
"name": "code-reviewer",
"source": "./plugins/code-reviewer",
"description": "PRのコードレビューを支援するプラグイン",
"version": "1.0.0"
}
]
}
```

#### 5. ローカルでのテスト

**プラグイン単体のテスト**
```bash
# クローンしたリポジトリのルートに移動
cd my-plugins

# プラグイン単体のインストール
claude --plugin-dir ./plugins/<plugin-name>

# スキルの実行テスト（例: code-reviewer プラグインの review スキル）
/<skill-name>

# その他、mcpやhookがあれば同様に動作確認を行う。
```

**マーケットプレイス全体のテスト**
```bash
# クローンしたリポジトリのルートに移動
cd my-plugins

# Claude Codeを起動
claude

# マーケットプレイスの追加、プラグインのインストールを行う（対話形式でも可）
/plugin marketplace add ./
/plugin install <plugin-name>@my-plugins
# ※ スコープ選択では Local を選ぶ（テスト用のため、チーム設定に影響させない）

# プラグインを適用するためClaude Codeセッションを再起動
ctrl + c
claude

# スキルの実行テスト
/<skill-name>

# その他、mcpやhookがあれば同様に動作確認を行う。
```

#### （必要に応じて）クリーンアップ

```bash
# テスト用にインストールしたプラグインの削除
/plugin uninstall <plugin-name>@my-plugins

# テスト用に追加したマーケットプレイスの削除
/plugin marketplace remove my-plugins
```

### 4.5. プラグインで利用可能なコンポーネント

スキル以外にも、以下のコンポーネントをプラグインに含めることができます:

```
plugins/<plugin-name>/
├── .claude-plugin/
│ └── plugin.json # マニフェスト（必須）
├── skills/ # スキル（SKILL.md）
├── agents/ # カスタムエージェント定義
├── hooks/
│ └── hooks.json # フック設定
├── .mcp.json # MCP サーバー設定
├── .lsp.json # LSP サーバー設定
└── settings.json # デフォルト設定
```

### 4.6. 変更の公開

1. 変更をコミット・プッシュする
2. PR を作成し、master にマージ

---

## 5. 参考リンク（公式ドキュメント）

| トピック                             | URL                                                 |
| ------------------------------------ | --------------------------------------------------- |
| スキルの作成・設定                   | https://code.claude.com/docs/ja/skills              |
| プラグインの作成                     | https://code.claude.com/docs/ja/plugins             |
| プラグインのインストール・管理       | https://code.claude.com/docs/ja/discover-plugins    |
| マーケットプレイスの作成・配布       | https://code.claude.com/docs/ja/plugin-marketplaces |
| プラグインリファレンス（スキーマ等） | https://code.claude.com/docs/ja/plugins-reference   |
| サブエージェント                     | https://code.claude.com/docs/ja/sub-agents          |
| フック                               | https://code.claude.com/docs/ja/hooks               |
| MCP サーバー                         | https://code.claude.com/docs/ja/mcp                 |
