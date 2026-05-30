# claude-kit リファレンス構造整理メモ — PR223

## 概要

claude-kit の `references/` は現在フラット構成（20+ ファイルが 1 ディレクトリ）。
dev-kit のようにトピック別サブフォルダに整理する。

## 現在のファイル一覧とグルーピング案

### plugin/ サブフォルダ候補

| ファイル | 内容 |
|---|---|
| `plugin-structure.md` | プラグイン作成・更新ガイド（version sync チェックリスト含む） |
| `plugin-claude-md.md` | プラグインの CLAUDE.md 執筆ガイド |
| `plugin-config.md` | config スキル設計ガイド |
| `setup-wizard.md` | セットアップウィザードリファレンス |

### skill/ サブフォルダ候補

| ファイル | 内容 |
|---|---|
| `skills.md` | スキル執筆ガイド |

### hook/ サブフォルダ候補

| ファイル | 内容 |
|---|---|
| `hooks.md` | フック執筆ガイド |
| `kit-hooks-sync.md` | -kit 間フック構造同期ガイド |

### claude-md/ サブフォルダ候補

| ファイル | 内容 |
|---|---|
| `claude-md.md` | CLAUDE.md 執筆ガイド（汎用） |
| `rules.md` | ルール執筆ガイド |

### common/ サブフォルダ候補（複数カテゴリに横断）

| ファイル | 内容 |
|---|---|
| `common.md` | 共通ガイド（全クリエータースキルが読む） |
| `environment.md` | 環境変数ガイド |
| `subagents.md` | サブエージェントガイド |
| `references-sync.md` | references 同期ガイド |

### ルートに残すもの（メタファイル）

| ファイル | 内容 |
|---|---|
| `CLAUDE.md` / `CLAUDE.jp.md` | このリファレンスディレクトリ自体の説明 |
| `_index.yaml` / `_index.jp.yaml` | インデックス |
| `_injection_rules.yaml` | 注入ルール |

## plugin バージョン同期チェック

現状: `plugin-structure.md` の Step 4 に「三点セット同期チェックリスト」が埋め込まれている。

改善案:
- `plugin/version-sync.md` として独立ファイルに分離
- `plugins/*/CLAUDE.md` を編集したときに `version-sync.md` を optional 注入

injection rule 追加案:
```yaml
- pattern: "plugins/*/CLAUDE{.jp,}.md"
  required:
    - plugin-claude-md.md   # 既存
  optional:
    - environment.md        # 既存
    - plugin/version-sync.md  # 追加: version triple を揃えるリマインダー
```

## 注意事項

- JP ミラー（*.jp.md）も同じサブフォルダに移動する
- 移動後は _index.yaml / _injection_rules.yaml の全パスを更新する
- claude-kit の inject_references.py は相対パスでリファレンスを読むため、パス更新が必須
