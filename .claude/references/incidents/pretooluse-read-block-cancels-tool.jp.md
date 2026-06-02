<!-- This file is a Japanese mirror of pretooluse-read-block-cancels-tool.md. When updating the English original, update this file too. -->

# pretooluse-read-block-cancels-tool

英語オリジナル: `.claude/references/incidents/pretooluse-read-block-cancels-tool.md`

## 何が起きたか

`inject_references.py` は `Edit`/`Write`/`MultiEdit`/`Read` の 4 種すべてに対して
`{"decision": "block", "reason": "..."}` を返していた。`Edit`/`Write`/`MultiEdit` では
意図通り — フックがツール呼び出しをキャンセルしてリファレンスコンテキストを注入し、
Claude が再試行する。

`Read` に対しても同じ出力を返した結果、Read がキャンセルされて Claude がファイル内容を
受け取れなくなった。Claude は代替として `Bash` + `sed` でファイルを読み込んだ。

## 根本原因

`decision: "block"` は `UserPromptSubmit` / `Stop` / `PostToolUse` などのイベント向け
フック出力フォーマット。`PreToolUse` フックで使うと「ツール呼び出しをキャンセルする」
という動作になり、Edit/Write では正しいが Read では意図に反する。

**Read をキャンセルせずにコンテキストを注入する**には `PreToolUse` 専用フォーマットを使う:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "additionalContext": "..."
  }
}
```

## 防止策

`PreToolUse` フックスクリプト内で `tool_name` に応じて分岐する:

```python
if tool_name == "Read":
    sys.stdout.buffer.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": reason,
        }
    }, ensure_ascii=False).encode("utf-8"))
else:
    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
    )
```

`additionalContext` の内容はツール結果と並んで `system-reminder` として Claude に表示される。
リファレンスコンテキストが注入されつつ、ファイル内容も届く。
