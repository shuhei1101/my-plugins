# inject-task-rule — Task ツール活用ルールの UserPromptSubmit 注入

dev-kit プラグイン v1.11 で追加。複数ステップ作業を依頼されたときに Claude が Task ツール
（TaskCreate / TaskGet / TaskList / TaskUpdate / TaskStop / TaskOutput）でタスク管理するのを
忘れないよう、ユーザープロンプト送信のたびに利用ルール表を `additionalContext` として注入する。

## 構成

| No | ファイル | 役割 |
|---|---|---|
| 1 | `plugins/dev-kit/hooks/user-prompt-submit/inject_task_rule.py` | UserPromptSubmit エントリ。固定文字列の Markdown を `additionalContext` で返す |
| 2 | `plugins/dev-kit/hooks/hooks.json` の `UserPromptSubmit` 登録 | 上記スクリプトを起動 |

## 注入内容

- Task ツール 6 種類の用途・タイミング表
- 守るべきこと 4 箇条（作業開始時に必ず TaskCreate / 着手時に in_progress / 完了時に completed / 不要時は削除 / 進捗不明時は TaskList）

## 設計判断

- SessionStart ではなく UserPromptSubmit を選択。複数ターンにまたがる長セッションで毎ターン
  ルールが想起されるようにするため。ユーザー要望ベース。
- Jinja2 を使わず Python 文字列直書き。注入内容に動的部分がないため。
- セッション初回のみ注入する仕組みは持たない（毎ターン 1KB 程度なので影響軽微）。

## 参考リンク

- `plugins/dev-kit/hooks/user-prompt-submit/inject_task_rule.py`: 本体
- `plugins/dev-kit/hooks/hooks.json`: フック登録
