[work] このプロジェクトでは work プラグインが有効です。実装作業の流れと、Claude Code タスク機能の使い方を以下にまとめます。

## 作業フロー（再掲）

1. 実装・修正の依頼を受けたら `/work:start` でブランチ + ワークツリーを作成する（質問・調査のみなら不要）
2. ワークツリー内で実装する。`git -C {ワークツリーパス}` で操作する
3. 完了したら `/work:merge` を提案し、ユーザー承認後にマージする

## タスク管理（Claude Code TaskCreate / TaskList / TaskUpdate）

新しい作業を始める前にタスクが未登録なら必ず `TaskCreate` で登録する（複数ステップの作業は特に）。ユーザーがスコープを変えた・不要になったと言った場合は `TaskUpdate` で必ず追従する。

| ツール | 用途 |
|---|---|
| `TaskCreate` | 新規タスクを `pending` で作成。`subject`（命令形の短い件名）と `description`（何をやるか）を必ず書く。`activeForm`（進行形の短文）も入れるとスピナー表示が分かりやすい |
| `TaskList` | 全タスクの一覧（id / subject / status / owner / blockedBy）。次に着手するタスクを選ぶときに使う。ID の小さいものから着手するのが基本 |
| `TaskGet` | 1 タスクの詳細（description / コメント / 履歴） |
| `TaskUpdate` | status 変更（`pending` → `in_progress` → `completed`、削除は `deleted`）、subject/description/activeForm の修正、owner 割当、`addBlockedBy` / `addBlocks` で依存関係を設定 |

### 典型ユースケース

| 状況 | 対応 |
|---|---|
| 新しい作業に着手 | `TaskCreate` で登録 → `TaskUpdate status=in_progress` |
| 1 タスク完了 | `TaskUpdate status=completed` → `TaskList` で次を確認 |
| ユーザーが「やっぱ A もやって」 | `TaskCreate` で追加（既存タスクとの依存があれば `addBlockedBy`） |
| ユーザーが「タスク B の範囲を変えて」 | `TaskGet` で現状確認 → `TaskUpdate subject/description` |
| ユーザーが「タスク C はやめる」 | `TaskUpdate status=deleted`（履歴から消える、復元不可） |
| ブロッカー発生で完了不能 | `in_progress` のまま保持し、解消が必要な内容で新規 `TaskCreate` → `addBlockedBy` で依存を張る |

タスクを跨いだ作業の途中では、完了直後に `TaskList` を読んで次の `pending` タスクを選ぶこと。

保護フック（master 直接コミット阻止など）の規約は guard-kit プラグインの session_start で別途注入されます。
