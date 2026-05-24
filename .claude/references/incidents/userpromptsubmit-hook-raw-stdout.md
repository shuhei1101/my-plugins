# UserPromptSubmit フックが生の stdout を出力していた

## 日付

2026-05-24

## 何が起きたか

ui-kit プラグインの UserPromptSubmit フックを実装した際、プロンプトファイルの内容を `sys.stdout.buffer.write(p.read_bytes())` でそのまま stdout に出力した。
これは従来の hook-creator SKILL.md のパターン（旧 `[Plugin] UserPromptSubmit`）に従ったものだったが、複数行のテキストが `<system-reminder>` として毎回注入されセッションを圧迫していた。

## 原因

hook-creator SKILL.md の UserPromptSubmit パターンが Stop フックと異なる方式を使っていた。
Stop フックはすでに `"Read and follow: /path"` の1行参照方式を採用していたが、UserPromptSubmit パターンだけ旧方式のままだった。

## 修正

- UserPromptSubmit フックの inline Python を以下に変更:
  ```
  sys.stdout.buffer.write(('Read and follow: '+str(p)+'\n').encode()) if p.exists() else None
  ```
- hook-creator SKILL.md の UserPromptSubmit パターンを "Read and follow" 形式に統一（PR106）

## 教訓

**すべてのプロンプト注入フック（UserPromptSubmit / Stop / PreToolUse）は `"Read and follow: /path"` の1行出力に統一する。**
フックの stdout / `reason` は1行のみとし、Claude 自身がファイルを読む方式にすること。
複数行の内容を直接注入すると会話セッションが汚染され、ユーザーにも見えてしまう。
