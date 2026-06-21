"""UserPromptSubmit フック: Task ツール活用ルールを Claude へ毎回注入する。"""
from __future__ import annotations

import json
import sys

CONTEXT = """\
# タスク管理ルール（必読）

実装・修正・調査など複数ステップを伴う作業に取りかかる際は、必ず以下の Task ツール群でタスク管理を行うこと。単発の質問への回答だけなら不要。

| ツール       | 用途                                                       | 使うタイミング                                                     |
| ------------ | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| `TaskCreate` | タスクリストに新しいタスクを作成                           | 作業開始時。複数ステップを最初に洗い出して登録                     |
| `TaskGet`    | 特定タスクの完全な詳細を取得                               | 既存タスクの内容・進捗を確認したいとき                             |
| `TaskList`   | すべてのタスクと現在のステータスを一覧                     | 進行状況を俯瞰したい・次の手を決めたいとき                         |
| `TaskUpdate` | ステータス・依存関係・詳細の更新、またはタスクの削除       | 開始時 → `in_progress`、完了時 → `completed` に即時更新。不要になったタスクは削除 |
| `TaskStop`   | ID で実行中バックグラウンドタスクを終了                    | 不要になったバックグラウンド処理を止めるとき                       |
| `TaskOutput` | （非推奨）バックグラウンドタスクの出力取得                 | 原則使わない。出力ファイルパスを `Read` するほうが推奨             |

## 守ること

- 作業開始時に必ず `TaskCreate` で 1 件以上のタスクを作る（複数ステップなら全部洗い出す）
- ステップ着手時に `TaskUpdate` で `in_progress` に切り替え、終わったら即 `completed` にする（まとめて完了させない）
- ユーザーから「そのタスクは不要」と言われたら `TaskUpdate` の削除でリストから消す
- 進捗を見失ったら `TaskList` で現状を確認してから次の手を決める
"""


def main() -> int:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": CONTEXT,
        }
    }
    sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
