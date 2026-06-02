---
name: issue-review
description: |
  未レビューのイシューを 1 件ずつ見て、フロントマターの decision（accept/reject）を埋め、
  イシューの QA に回答し、自由記述の対応指示（`instruction` キー）を記録する。スマホ主用途: 各イシューの読みやすい要約を提示し、
  AskUserQuestion（タップ操作）で回答を集めながら、未レビューイシューを 1 度に全件捌く。
  トリガー: 「イシューをレビューして」「イシューを捌きたい」「review issues」「issue-review」、
  または `/work:issue-review` を明示的に呼び出したとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:issue-review — イシューを捌く（スマホ主用途）

`.work/issues/` の未レビュー（`decision: pending`）イシューを上から順に巡り、各イシューについて
**対応する (accept) / 対応しない (reject) / 後で (skip)** をユーザーに選ばせる。あわせてイシューの
`## QA` に回答させ、自由記述の対応指示を残させる。スマホ前提: スマホの SSH ではイシューファイルを開きづらいため、
生のファイル閲覧ではなく、コンパクトな要約を提示し `AskUserQuestion`（タップ）で回答を集める。

結果は各イシューの**フロントマター `decision`**（source of truth）・`## QA` セクション・`instruction`
フロントマターキーに書き込む。後で `work:issue-resolve` がその決定に基づいて動く。

> このスキルでは `AskUserQuestion` の使用を意図的に必須としている（グローバルの AskUserQuestion 制約
> 参照 — 使用を定義したスキルは適用外）。

---

## 概要

- **前提**: `.work/issues/` が存在する（無ければ `/work:setup`）。
- **未レビュー** = フロントマター `decision` が `pending`（または欠落）のイシュー。既に `accept` /
  `reject` のものはスキップ。`closed/` は無視。
- イシューファイルのフォーマット／フロントマターは `work-dir/イシュー.md`（`.work/issues/` 編集時に
  自動注入）が規定する — それに従う。

---

## タスク

### Step 1: 未レビューイシューを収集

#### プロセス

1. `.work/issues/` が無ければ → `/work:setup` を促して停止。
2. `.work/issues/ISSUE-*.md` を glob（`closed/` 除外）。各ファイルのフロントマター `decision` だけを
   読む。`decision` が `pending` または欠落のものを残す。
3. 残ったイシューをイシュー番号の昇順でソート。
4. 1 件も無ければ → 「未レビューのイシューはありません」と報告して停止。

→ Step 2 へ

#### 出力

- 未レビューイシュー ID の順序付きリスト

---

### Step 2: 各イシューをレビュー（上から順にループ）

#### プロセス

未レビューイシューを順に：

1. イシューファイルを読み、**スマホで読みやすいコンパクトな要約**を提示する — 生ファイルを丸ごと
   出さない。含める: `ISSUE-N` + タイトル・`## 概要`・`## 問題点` の要点・`## 修正案` の選択肢
   （推奨案を明示）。短く。
2. `AskUserQuestion` で対応可否を尋ねる：
   - 質問: `ISSUE-N: {title} — どうする?`
   - 選択肢: **対応する** (accept) / **対応しない** (reject) / **後で** (skip / pending のまま)
   - ユーザーは自由入力（「その他」）欄に理由を書いてよい。
3. **後で (skip)** の場合 → イシューは触らず（`decision` は `pending` のまま）次へ。
4. **対応する / 対応しない** の場合：
   a. イシューに未解決の `## QA` があれば、各エントリを（`AskUserQuestion` 1 回あたり最大 4 件まで
      バッチで）QA の選択肢を使って提示し、回答を集める。回答を書き戻す: QA の `回答` を記入し
      `状態: 解決` に、採用案を `## 修正案`（採用案）や該当セクションへ反映。
   b. フロントマター `decision` を `accept` または `reject` に設定。
   c. ユーザーが自由記述の対応指示・理由を述べた場合（対応可否ステップの自由入力または追問で）、
      イシューの `instruction` フロントマターキーに書き込む（無ければ `""` のまま）。
5. 次のイシューへ。

→ 最後のイシュー後、Step 3 へ

#### 注記

- ここでブランチ作成や `status` 変更は**しない** — それは `work:issue-resolve` で行う。
- 各イシューの対話を自己完結させ、途中で止めてもよいようにする（残りは `pending` のまま次回再表示）。

---

### Step 3: レビュー結果をコミット

#### プロセス

1. イシューファイルに変更があればコミットする。イシューファイルは git 管理対象で、このトリアージ
   コミットは現在のブランチ（通常 `master`）で行う。`master-commit-guard` フックが 1 度確認を挟む
   ことがある — イシュートリアージでは想定どおりなので進める。
   ```bash
   git add .work/issues/
   git commit -m "chore: イシューをレビュー（decision/QA を記入）"
   ```
   （メッセージは他の work コミット同様 `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` に従う）
2. `_index.yaml` は git 管理外 — コミットしない。ここで `status` 変更は不要。
3. サマリを報告: accept / reject / skip の件数。

#### 注記

- 決定は**コミット**する必要がある。`work:issue-resolve`（新しいワークツリーで動く）が決定を
  読めるようにするため。未コミットのままだと新しいワークツリーから見えない。
