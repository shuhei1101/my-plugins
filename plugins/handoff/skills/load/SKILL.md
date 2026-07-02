---
name: handoff:load
description: 過去のハンドオフ Markdownを手動で読み込んで現セッションのコンテキストに取り込む
argument-hint: "[session-id]"
arguments: "session_id"
disable-model-invocation: true
---

# load

過去のハンドオフを Read で読み込み、続きの作業に取りかかれるようにする。

## 入力

- `$session_id`: 復元したいハンドオフの session_id。必須。

## ステップ 1: 引数の有無を確認する

- `$session_id` が指定されていないなら、以下の案内をユーザーに返してスキルを終了する

  > session_id を指定してください。ハンドオフファイルは `$HANDOFF_DIR` 配下に `<session_id>.md` の形で保存されています。
  > 一覧を確認するには `ls $HANDOFF_DIR` を実行してください。復元したいファイル名から `.md` を除いた文字列が session_id です。

## ステップ 2: 対象ファイルを特定する

- 対象: `${HANDOFF_DIR}/${session_id}.md`
- ファイルが存在しなければユーザーに「対象ファイルが見つからない」旨を報告して終了する

## ステップ 3: ハンドオフを Read で全文読み込む

- Read ツールでファイル全文を取り込む
- 大きい場合も `limit`/`offset` で分割せず、全文を読む前提（ハンドオフは全体で 1 つのコンテキストを構成するため）

## ステップ 4: サマリを提示して次の一手を促す

- 読み込んだハンドオフの `## タスク一覧` を短く要約してユーザーに提示する
- 続けて何から着手するかをユーザーに確認する（進行中タスクの再開 / 未着手タスクの着手 / 別の指示）

## 補足

- `HANDOFF_DIR` が未設定なら SessionStart フックが走っていない状態。Claude Code の再起動をユーザーに促す
