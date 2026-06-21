# inject_rules注入ロジック — PreToolUse フックのルール自動注入動作仕様

## 概要

`inject_rules.py`（work・dev-kit プラグイン共通）は、Edit/Write/Read ツール実行前にマッチするルール `.md` を additionalContext に注入する。
1 回の呼び出しで CHAR_LIMIT（10,000文字）を超えるときは複数回に分割して注入する。

## TOKEN_DIR（プラグイン別）

| プラグイン | TOKEN_DIR |
| ---------- | --------- |
| work | `~/.claude/tokens/work/rules/` |
| dev-kit | `~/.claude/tokens/dev-kit/rules/` |

トークンファイル名は `{session_id}.json`。

## トークンデータ構造

```json
{
  "rules": ["file1.md", "file2.md"],
  "partial": {
    "file3.md": 8000
  }
}
```

- `rules`: 完全読み込み済みのルールファイル（次回以降スキップ）
- `partial`: 部分読み込み中のファイルと読み込み済みオフセット（文字数）

## パックロジック

1. `matched` からセッション内で完全未読のファイルを `to_inject` として抽出
2. `partial` にオフセットがある場合はその続きから body を作成
3. CHAR_LIMIT に収まる分だけ貪欲にパック
   - 収まらない場合は利用可能文字数を計算して部分注入 → `partial` に残りオフセットを保存
   - MIN_PARTIAL_CHARS（200文字）も確保できない場合は打ち切り（前ブロックまでで完了）
   - 最初の1件から溢れる場合は CHAR_LIMIT 分を強制注入（無限ループ防止）
4. 完全読み込みは `rules` に追加、partial は更新してトークン保存

## 進捗表示

- systemMessage・additionalContext ともに完了・未完了を問わず常に件数表示
  - 完了時: `✅ 読み込み完了: N/M ファイル`
  - 未完了時: `⚠️ 読み込み中: N/M ファイル / X/Y 文字 — 残り Z 未完了`
- `remaining_count` が 0 より大きい場合は `deny` を返してツールを再実行させる

## 参考リンク

- `plugins/work/hooks/pre-tool-use/inject_rules.py`: work プラグインのスクリプト
- `plugins/dev-kit/hooks/pre-tool-use/inject_rules.py`: dev-kit プラグインのスクリプト
- `plugins/work/hooks/pre-tool-use/inject_message.j2`: additionalContext のテンプレート（work・dev-kit 共通内容）
