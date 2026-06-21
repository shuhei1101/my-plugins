[work] このプロンプトの作業に着手する前に、Claude Code タスクが登録されているか必ず確認すること。

判断手順:

1. `TaskList` で現在のタスクを確認する
2. 今からやる作業に該当する `pending` / `in_progress` タスクが**ない**なら、まず `TaskCreate` で登録する（質問・調査・1 ステップで終わる雑用は除く）
3. 該当タスクがあるなら、そのタスクを `TaskUpdate status=in_progress` にしてから作業を始める
4. ユーザーがスコープ変更・タスク中止を示唆したら、`TaskUpdate`（subject/description 変更 or `status=deleted`）で必ず追従する

タスク登録漏れに気付いたら、その時点で `TaskCreate` してから作業を続けること。「タスクなしで進めていいか」をユーザーに確認せず勝手に省略しないこと。
