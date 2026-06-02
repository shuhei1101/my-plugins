# PR148 — fix-py-kit-changelog-read-matcher

## 概要

PR147 の changelog 記述ミスを修正する。`plugins/py-kit/CLAUDE.md` および `CLAUDE.jp.md` の v2.1.1 changelog に「Read matcher removed」とあるが、実際には Read マッチャーは維持しており、変更内容は「path+description のみ注入 + 絶対パス化」が正しい。方針転換前の記述の消し忘れ。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #147 | 注入フックの本文注入削除・絶対パス化（この PR が修正対象の changelog を書いた） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260528_fix-py-kit-changelog-read-matcher/PR148/QA.md` |
| 済 | CLAUDE.md の v2.1.1 changelog 記述を修正 | - `plugins/py-kit/CLAUDE.md` |
| 済 | CLAUDE.jp.md の v2.1.1 changelog 記述を修正 | - `plugins/py-kit/CLAUDE.jp.md` |

## 参考ドキュメント

- `plugins/py-kit/CLAUDE.md:92`: 修正対象の changelog 行

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |

## QA

なし
