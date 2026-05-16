> このファイルは `user-prompt-submit.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `user-prompt-submit.md` にも反映してください。

[work-kit] プロンプトを処理する前に現在の作業コンテキストを確認すること:

1. `.work/tasks/` をスキャンして進行中の PR（`PR{N}/` フォルダ）を確認する
2. 進行中の PR があればその `TODO.md` を読む
3. 今回の依頼の種別を判断する:
   - 既存 PR の続き → 該当ワークツリーで作業を継続する
   - 新規作業 → `/work-kit:work-start` を実行してから始める

詳細ルール:
- TODO.md の作成・更新 → `/work-kit:todo`
- QA エントリの記録・クローズ → `/work-kit:qa`
