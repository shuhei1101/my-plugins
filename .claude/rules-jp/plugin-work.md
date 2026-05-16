---
paths:
  - "plugins/**"
  - ".claude-plugin/**"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/plugin-work.md` も同時に更新してください。

# プラグイン作業ルール

## 概要

このリポジトリのプラグイン作成・更新に関するルール。`plugins/**` または `.claude-plugin/**` 配下のファイルを読み書きするときに自動ロードされる。

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `plugins/{name}/.claude-plugin/plugin.json` | プラグインマニフェスト（名前・バージョン・説明） |
| `.claude-plugin/marketplace.json` | マーケットプレイスカタログ — plugin.json のバージョンと常に一致させる |
| `plugins/{name}/skills/{skill}/SKILL.md` | スキル定義 |

## 編集時に必ずやること

コミット前に両方を更新する:

- [ ] `plugins/{name}/.claude-plugin/plugin.json` — `version` をバンプ
- [ ] `.claude-plugin/marketplace.json` — 対応するプラグインの `version` をバンプ

## 参考

### plugin.json の形式

```json
{
  "name": "{plugin-name}",
  "description": "{このプラグインが何をするかの短い説明}",
  "version": "1.0.0"
}
```

- `name`: kebab-case 識別子（スキルの名前空間にもなる）
- `version`: セマンティックバージョニング（`MAJOR.MINOR.PATCH`）


### marketplace.json エントリの形式

```json
{
  "name": "{plugin-name}",
  "source": "./plugins/{plugin-name}",
  "description": "{plugin.json の description と同じ}",
  "version": "1.0.0"
}
```

## バージョンバンプの規則

| 変更の種類 | バンプ | 例 |
|---|---|---|
| バグ修正・小さな修正 | PATCH（`1.0.0` → `1.0.1`） | コマンドの誤り修正、ロジックのタイポ |
| 新しいセクション・新機能追加 | MINOR（`1.0.0` → `1.1.0`） | ワークフローのセクション追加 |
| 完全な書き直し・破壊的変更 | MAJOR（`1.0.0` → `2.0.0`） | スキル全体のアプローチを刷新 |
