---
paths:
  - "plugins/**"
  - ".claude-plugin/**"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/plugin-work.md` も同時に更新してください。

# プラグイン作業ルール

## 概要

このリポジトリのプラグイン作成・更新に関するルール。`plugins/**` または `.claude-plugin/**` 配下のファイルを読み書きするときに自動ロードされる。

## 新規作成時に使うスキル

プラグイン作業で新しいファイルを作成する場合は、以下のスキルを使うこと。

| 作成するもの | 使うスキル |
|---|---|
| フック | `/hook-creator` |
| ルール | `/rule-creator` |
| スキル | `/skill-creator` |
| CLAUDE.md | `/claude-creator` |

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

## ファイル名・スキル名を変更したとき

スキル名・ファイル名・フォルダ名を変更した場合、同プラグイン内の他のファイルから参照されている可能性がある。変更後は必ず以下を実施すること:

1. 変更前の名前でプラグインディレクトリ全体を検索する
2. ヒットした箇所をすべて新しい名前に更新する
3. 更新漏れがないことを確認してからコミットする

> スキルは SKILL.md 内の `trigger` や他スキルの手順から参照・呼び出しされることがある。ファイルシステム上のリネームだけでは不十分。

## スキルからスクリプトを参照するとき

スキル（SKILL.md）内でスクリプトを呼び出す場合、`plugins/{name}/scripts/` という相対パスは
**`my-plugins` リポジトリ内でしか動作しない**。他プロジェクトにインストールされた場合は
スクリプトがプラグインキャッシュにあるため、必ず `${CLAUDE_PLUGIN_ROOT}/scripts/` を使うこと。

```bash
# NG — my-plugins 以外では動かない
python plugins/work-kit/scripts/index-tool.py next-id ...

# OK — どのプロジェクトでも動く
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" next-id ...
```

`${CLAUDE_PLUGIN_ROOT}` は `skills/{skill-name}/` の2階層上（プラグインルート）を指す。

---

## バージョンバンプの規則

| 変更の種類 | バンプ | 例 |
|---|---|---|
| バグ修正・小さな修正 | PATCH（`1.0.0` → `1.0.1`） | コマンドの誤り修正、ロジックのタイポ |
| 新しいセクション・新機能追加 | MINOR（`1.0.0` → `1.1.0`） | ワークフローのセクション追加 |
| 完全な書き直し・破壊的変更 | MAJOR（`1.0.0` → `2.0.0`） | スキル全体のアプローチを刷新 |
