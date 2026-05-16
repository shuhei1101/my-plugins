> このファイルは `stop.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `stop.md` にも反映してください。

[work-kit] 応答を完了する前に確認すること:

1. `.work/tasks/index.yaml` を読んで `completed: false` の PR を特定する
2. 該当する `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` を更新し、完了したタスクを `- [x]` にチェックする
3. 全項目が `- [x]` になっていれば `/work-kit:merge` を提案する
   （merge スキルが `.work/tasks/index.yaml` の `completed: true` 更新とクリーンアップを担う）
