# hooksルール配置変更

## 概要

work/dev-kit プラグインの hooks/rules/ 内スクリプトを hooks/ 直下に移動し、
rules/ フォルダを plugin 直下（hooks/ と同階層）に再配置する。

## 作業内容

| 完了 | 対象 | 内容 |
| ---- | ---- | ---- |
|      | work | hooks/rules/{inject_rules.py,clear_session_token.py,inject_message.j2} を hooks/ 直下に移動 |
|      | work | hooks/rules/work/ を rules/work/ に移動（plugin 直下） |
|      | work | hooks/hooks.json のパス更新 |
|      | work | inject_rules.py の RULES_DIR / FileSystemLoader パス更新 |
|      | dev-kit | hooks/rules/ を rules/ に移動（plugin 直下） |
|      | dev-kit | hooks/inject_rules.py の RULES_DIR / FileSystemLoader パス更新 |
|      | dev-kit | hooks/hooks.json のパス更新 |

## 参考ドキュメント
