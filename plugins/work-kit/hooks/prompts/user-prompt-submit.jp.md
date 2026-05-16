> このファイルは `user-prompt-submit.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `user-prompt-submit.md` にも反映してください。

[work-kit] プロンプトを処理する前に現在の作業コンテキストを確認すること:

1. `.work/tasks/index.yaml` を読んで `completed: false` の PR を確認する
2. 進行中の PR がある場合:
   a. `.work/tasks/{YYYYMMDD}_{title}/PR{N}/QA.md` を読む
   b. 未解決の QA エントリがあれば、TODO より先にユーザーへの回答を促す（QA が残っている間は作業を進めない）
   c. QA が全て解決済み（またはファイルが空）なら `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` を読んで作業を継続する
3. 進行中の PR がない場合 → `/work-kit:work-start` を実行してから始める
