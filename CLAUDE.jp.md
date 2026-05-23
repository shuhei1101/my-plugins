# CLAUDE.jp.md — my-plugins 開発者ガイド（日本語訳）

> このファイルは `CLAUDE.md` の日本語翻訳です。Claude Code には自動読み込みされません。内容を確認するための参照用ファイルです。
> 変更を加える場合は、まずこのファイルを更新し、その後 `CLAUDE.md`（本体）にも同じ変更を反映してください。

---

このリポジトリは Claude Code のプラグインマーケットプレイスです。スキルをプラグインとして配布・管理し、`/plugin` コマンドでインストールできます。

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
│       ├── references/        # 任意：スキルが参照する共有資料
│       │   ├── {トピック}.md     # 参照内容（英語・スキルから明示的に読み込み）
│       │   └── {トピック}.jp.md  # 日本語訳（参照用）
│       └── skills/
│           └── {スキル名}/
│               ├── SKILL.md      # スキル定義（英語・自動読み込み）
│               └── SKILL.jp.md   # 日本語翻訳（参照用）
├── CLAUDE.md      # このファイルの英語本体（自動読み込み）
└── CLAUDE.jp.md   # このファイルの日本語翻訳（参照用）
```

---

## プラグイン作成・更新のルール

このリポジトリで新しいプラグインを作成するとき、または既存のプラグインを更新するときは、**必ず `/claude-kit:plugin-creator` スキルを起動してから作業すること**。

- スキルがディレクトリ構造・`plugin.json`・`changelogs/`・`marketplace.json` を一括でガイドする
- `changelogs/v{X.Y.Z}.md` の作成とバージョンバンプはスキルの手順に従い必ず実施する
- スキルを使わずに直接ファイルを作成・編集してはならない

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
