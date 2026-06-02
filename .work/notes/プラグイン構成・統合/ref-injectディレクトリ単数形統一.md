# ref-inject ディレクトリ命名 — 単数形統一

全プラグインのリファレンス注入設定ディレクトリ名を `.ref-injects`（複数形）から
`.ref-inject`（単数形）に統一した。

## 対象

| # | プラグイン | 旧パス | 新パス |
|---|---|---|---|
| 1 | claude-kit | `references/.ref-injects/` | `references/.ref-inject/` |
| 2 | dev-kit | 〃 | 〃 |
| 3 | ref-inject（テンプレート） | `templates/references/.ref-injects/` | `templates/references/.ref-inject/` |
| 4 | work | `references/.ref-injects/` | `references/.ref-inject/` |

## 変更箇所

- ディレクトリ名: `git mv` でリネーム（全18ファイル）
- `inject_references.py`: `refs_dir / ".ref-injects"` → `refs_dir / ".ref-inject"` に変更（全4スクリプト）
- `claude-kit/_injection_rules.yaml`: パターン内の `.ref-injects` → `.ref-inject` に更新

## 変更履歴

| # | 日付 | 内容 |
|---|---|---|
| 1 | 260602 | `.ref-injects` を `.ref-inject` に単数形リネーム（全4プラグイン） |
