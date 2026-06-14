# hooksルール配置構成

## 概要

work・dev-kit プラグインの hooks ディレクトリ構成を整理した。
スクリプト類と .md ルールファイルを明確に分離し、管理しやすくした。

## 変更後の構成

```
plugins/{work,dev-kit}/
  hooks/
    hooks.json            # フック設定
    inject_rules.py       # ルール注入スクリプト（旧: hooks/rules/）
    inject_message.j2     # 注入メッセージテンプレート（旧: hooks/rules/）
    clear_session_token.py # トークン削除スクリプト（旧: hooks/rules/）
    *.py                  # その他スクリプト類
  rules/                  # 旧: hooks/rules/（plugin 直下に移動）
    {カテゴリ}/
      *.md
```

## inject_rules.py の重要な変更点

- `RULES_DIR`: `parent` から `parent.parent / "rules"` に変更
  - `__file__` は `hooks/inject_rules.py` → `parent.parent` は plugin 直下
- `FileSystemLoader`: `RULES_DIR`（rules/）から `_hooks_dir`（hooks/）に変更
  - `inject_message.j2` が `hooks/` 直下に移動したため

## 背景

以前は `hooks/rules/` にスクリプト（`.py`、`.j2`）と `.md` ルールファイルが混在していた。
今回の整理で責務を明確に分離した:
- `hooks/`: 実行可能なスクリプト類
- `rules/`: Claude が参照するルール `.md` ファイル群
