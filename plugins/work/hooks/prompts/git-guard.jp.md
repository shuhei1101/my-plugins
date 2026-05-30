<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# git-guard.jp.md — git-guard プロンプト（日本語ミラー）

> このファイルは `git-guard.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `git-guard.md` にも反映してください。

---

## プロンプト内容（英語版 `git-guard.md` に反映すること）

**[git-guard] git push / git merge を検知しました。**

今すぐ実行を停止してください。

以下を必ずユーザーに確認してください:

> 「`{コマンド}` を実行しようとしています。実行してよいですか？」

**重要ルール（例外なし）:**

- 過去の会話で「マージしていいよ」「プッシュしていいよ」と言われていても、それは**この操作への許可にはなりません**
- 毎回、この操作の直前に改めて確認を取ること
- ユーザーが「はい」「ok」「いいよ」「やって」など、この操作への明示的な承認を返すまで実行しないこと
