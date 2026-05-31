# PR32 — fix-cp932-encoding

## 概要

Windows の CP932 コードページ環境で `index-tool.py` が em dash（—）を含む
PR タイトルを print しようとすると UnicodeEncodeError が発生する問題を修正する。
stdout を UTF-8 に明示的に設定することで解消する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | index-tool.py の stdout を UTF-8 に固定 | - `plugins/work-kit/scripts/index-tool.py` |
| 済 | trim-index.py の stdout を UTF-8 に固定 | - `plugins/work-kit/scripts/trim-index.py` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## QA

なし
