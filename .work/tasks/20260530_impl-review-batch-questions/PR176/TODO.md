# PR176 — impl-review-batch-questions

## 概要

`/work-kit:impl-review` の Step 4「Interactive review loop」を、AskUserQuestion を 1 件ずつ呼ぶ
代わりに **最大 4 件まとめて投げるバッチ方式** に変更する。モバイル / SSH 経由でレビューする
ときの確認往復回数を減らす目的。AskUserQuestion は 1 回に最大 4 件まで質問できるため、
変更領域が 4 件以下なら 1 回、それ以上なら 4 + 4 など複数バッチで投げる。

PR166 で実際にこのバッチ方式が有効と確認された（8 項目を 4 + 4 で投げてレビュー完了）。
そのときユーザーから「この指示内容を impl-review スキル側にも入れて」と要望があり、別 PR
（このPR）に切り出して対応する流れとなった。

### 関連背景（PR166 から）

- 旧 Step 4: 1 件ずつ `AskUserQuestion(questions=[...1件...])` を呼ぶ → 確認往復が多い
- 新 Step 4: 1 件ずつではなく、配列にまとめて `AskUserQuestion(questions=[1,2,3,4])` で 1 回で投げる
- AskUserQuestion 制約: 1 〜 4 questions per call、`multiSelect: false` のとき preview 可
- もっと詳しく / 問題あり が選ばれた場合の deep-dive ループは個別呼び出しになるが、それは現状維持
- 仕様改訂が必要な箇所:
  - `plugins/work-kit/skills/impl-review/SKILL.md` Step 4 とその ja ミラー
  - 例の文言や「2-8 items」の文脈も合わせて更新

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #166 | バッチ方式の検証元 PR（py-kit/html-kit/next-kit → dev-kit 統合）|
| #172 | work-kit → workspace リネーム（このPRが触る SKILL.md のパスが変わる可能性あり） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| ✓ | QA.md に未決定事項を記録する（未決定事項なし） | - `.work/tasks/.../PR176/QA.md` |
| ✓ | impl-review SKILL.md の Step 4 をバッチ方式に書き換える | - `plugins/workspace/skills/impl-review/SKILL.md` |
| ✓ | impl-review SKILL.jp.md の同箇所も更新 | - `plugins/workspace/skills/impl-review/SKILL.jp.md` |
| ✓ | バージョンバンプ + changelog | - `plugins/workspace/.claude-plugin/plugin.json` / `changelogs/v2.40.0.md` / `marketplace.json` |

## 参考ドキュメント

- `.work/tasks/20260530_merge-language-plugins-into-dev-kit/PR166/TODO.md`: バッチ方式の起点となった PR166 の TODO

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
