---
paths: "**/plugins/**"
---

# Claude プラグインルール

## テンプレートフォルダ

- プラグイン内のスキルなどで共通する出力形式や、重複している記載はテンプレート形式を用いる
  - {プラグインフォルダ}/templates/{日本語名}.md
- スキル内ではcatで展開する

```
<!-- 任意のスキルファイル -->
!`cat xxx/xxx.md`
```


## フックフォルダの定義
- フォルダ構成は以下とする
  - {CLAUDE_PLUGIN_ROOT}/hooks/hooks.json
  - {CLAUDE_PLUGIN_ROOT}/hooks/{フック名}/{任意のスクリプトやj2, mdファイル}
    - 例: hooks/pre-tool-use/xxx.py
