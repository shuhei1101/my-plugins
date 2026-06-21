---
paths: 
  - "**/skills/*.md"
---

# AgentSkills関連の知識

## 公式コンテキスト
- `https://code.claude.com/docs/en/skills.md`

## ルール
- 環境変数を読ませるときは必ず、以下インラインコード形式で展開すること

### NG
```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```
- これはclaude codeがコードを実行する手間が発生してしまう。

### OK
```md
!`${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh`
```


## スキル内のインラインコードの書き方
動的コンテキストを注入する
!`<command>` 構文はスキルコンテンツが Claude に送信される前にシェルコマンドを実行します。コマンド出力はプレースホルダーを置き換えるため、Claude はコマンド自体ではなく実際のデータを受け取ります。
このスキルは GitHub CLI でライブ PR データを取得することで、プルリクエストを要約します。!`gh pr diff` および他のコマンドが最初に実行され、その出力がプロンプトに挿入されます：
```
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...

```
このスキルが実行されるとき：
各 !`<command>` が直ちに実行されます（Claude が何かを見る前に）
出力はスキルコンテンツのプレースホルダーを置き換えます
Claude は実際の PR データを含む完全にレンダリングされたプロンプトを受け取ります
これは前処理であり、Claude が実行するものではありません。Claude は最終結果のみを見ます。
置換は元のファイルに対して 1 回実行されます。コマンド出力はプレーンテキストとして挿入され、さらに !`<command>` プレースホルダーについて再スキャンされないため、コマンドは後のパスで展開するプレースホルダーを発行することはできません。
インラインフォームは、! が行の開始時または空白の直後に表示される場合にのみ認識されます。! が別の文字の後に続く場合（KEY=!`cmd` など）、プレースホルダーはリテラルテキストとして残され、コマンドは実行されません。
複数行のコマンドの場合、インラインフォームの代わりに、```! で開かれたフェンスコードブロックを使用します：
```

## Environment
```!
node --version
npm --version
git status --short
```

```
ユーザー、プロジェクト、プラグイン、または追加ディレクトリソースからのスキルとカスタムコマンドについて、この動作を無効にするには、設定で "disableSkillShellExecution": true を設定します。各コマンドは [shell command execution disabled by policy] に置き換えられます。バンドルされたスキルと管理スキルは影響を受けません。この設定は管理設定で最も有用です。ユーザーはそれをオーバーライドできません。
