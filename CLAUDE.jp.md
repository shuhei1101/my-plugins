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
│       └── skills/
│           └── {スキル名}/
│               ├── SKILL.md      # スキル定義（英語・自動読み込み）
│               └── SKILL.jp.md   # 日本語翻訳（参照用）
├── CLAUDE.md      # このファイルの英語本体（自動読み込み）
└── CLAUDE.jp.md   # このファイルの日本語翻訳（参照用）
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
