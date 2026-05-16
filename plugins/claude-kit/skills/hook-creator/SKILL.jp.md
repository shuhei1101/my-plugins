---
name: hook-creator
description: |
  プロンプト注入フックを作成する。
  「特定のタイミングで Claude に指示を出したい」「フックでプロンプトを差し込みたい」
  「このイベントのときに AI に〜してほしい」と言われたときに起動。
  `/claude-kit:hook-creator` で明示的に呼ぶことも可能。
---

# hook-creator — プロンプト注入フック作成

特定のイベント発火時に、プロンプトテキストを Claude のコンテキストへ注入するフックを作成するスキル。
シェルスクリプトで外部処理を行う「アクション型フック」とは異なり、Claude 自身に追加指示を与える「プロンプト注入型フック」を対象とする。

---

## 概要

Claude Code のフックは、セッション中の特定タイミングで自動発火する仕組み。
大きく2種類ある:

| 種別 | 用途 |
|---|---|
| アクション型 | 通知送信・テスト実行など外部処理 |
| **プロンプト注入型** | stdout にプロンプトを出力して Claude のコンテキストへ注入（このスキルの対象） |

プロンプト注入の仕組み:
- `UserPromptSubmit` フック: stdout テキスト → `<system-reminder>` として Claude に注入
- `Stop` フック: JSON `{"decision":"block","reason":"<プロンプト>"}` を stdout → Claude が作業を継続する
- `PreToolUse` フック: JSON `{"decision":"block","reason":"<プロンプト>"}` を stdout → ツール実行をブロックして指示注入

---

## 作業内容

### ステップ 1: 公式フックドキュメントを確認する

#### 条件

- 常に — 最初に実行

#### 処理内容

1. 公式ドキュメントを取得:
   **https://code.claude.com/docs/ja/hooks**

→ ステップ 2 へ

#### 出力

- フックイベント一覧・JSON スキーマ・返却値仕様を把握した状態

---

### ステップ 2: 要件をヒアリングする

#### 条件

- ステップ 1 完了

#### 入力

- ユーザーの要望

#### 処理内容

1. 以下を確認する:

   | 質問 | 例 |
   |---|---|
   | **どのタイミングで発火させたいか?** | ユーザーが入力を送るたびに / Claude が応答を終えたとき / ツール実行前 |
   | **どんな指示を Claude に渡したいか?** | 「作業完了前に TODO.md を更新しろ」「コミット前に lint を確認しろ」 |
   | **フックの配置場所は?** | プラグイン (`hooks/hooks.json`) / プロジェクト (`.claude/settings.json`) / ユーザー (`~/.claude/settings.json`) |

2. タイミングの発言からイベントを推測して提案する（§参考資料 / イベント対応表 を参照）

→ ステップ 3 へ

#### 出力

- イベント名・プロンプト内容・配置場所が確定

---

### ステップ 3: フックパターンを決定する

#### 条件

- ステップ 2 完了

#### 入力

- イベント名（ステップ 2 の出力）

#### 処理内容

1. イベントに応じたパターンを選択する（§参考資料 / フックパターン一覧 を参照）

2. ブロック系フックのループ防止を確認する（§参考資料 / ループ防止 を参照）:
   - `Stop` フック: `stop_hook_active` チェックで防止
   - `PreToolUse` フック（条件付きブロック）: ワンタイムトークンで防止

→ ステップ 4 へ

#### 出力

- hooks.json スニペット（仮）

---

### ステップ 4: プロンプトファイルを作成する

#### 条件

- ステップ 3 完了

#### 入力

- プロンプト内容（ステップ 2 の出力）
- 配置場所（ステップ 2 の出力）

#### 処理内容

1. プロンプトファイルを作成する:

   | 配置場所 | パス例 |
   |---|---|
   | プラグイン | `plugins/{name}/hooks/prompts/{event-name}.md` |
   | プロジェクト | `.claude/hooks/{event-name}.md` |

2. ファイル内容はユーザーが指定したプロンプトテキストをそのまま記述する

→ ステップ 5 へ

#### 出力

- プロンプトファイルが作成された

#### 補足

##### 注意

- `Stop` フックのプロンプトは「〜せよ」「〜を確認せよ」形式の命令文にする
- **`Stop` フックのプロンプトは極力短くする** — `reason` の内容は stdout 経由でユーザーの画面にそのまま表示されるため、長文を書くと画面が埋め尽くされてしまう
- `UserPromptSubmit` フックのプロンプトは `<system-reminder>` として扱われるため、コンテキスト情報の差し込みに向いている

---

### ステップ 5: hooks.json を作成・更新する

#### 条件

- ステップ 4 完了

#### 入力

- イベント名・フックパターン・プロンプトファイルパス

#### 処理内容

1. 配置場所に応じてファイルを決める:

   | 配置場所 | ファイル | 共有 |
   |---|---|---|
   | プラグイン | `plugins/{name}/hooks/hooks.json` | ✅ プラグインに同梱 |
   | プロジェクト（チーム共有） | `.claude/settings.json` の `hooks` セクション | ✅ git にコミット |
   | プロジェクト（ローカル限定） | `.claude/settings.local.json` の `hooks` セクション | ❌ `.gitignore` 推奨 |

2. §参考資料 / フックパターン一覧 のスニペットを使用する

→ ステップ 6 へ

#### 出力

- `hooks.json` または `settings.json` にフックエントリが追加された

---

### ステップ 6: 確認してユーザーに報告する

#### 条件

- ステップ 5 完了

#### 処理内容

1. 作成・更新したファイルを一覧で報告する
2. フックが正しく動作するかをユーザーに確認するよう促す:
   - Claude Code を再起動してフックが読み込まれることを確認
   - 対象イベントを発火させて `<system-reminder>` が表示されるか確認

#### 出力

- 作成ファイル一覧と動作確認手順

#### 補足

##### チェックリスト

- [ ] プロンプトファイルが存在する
- [ ] hooks.json / settings.json にエントリが追加された
- [ ] パス変数が配置場所に合っている（§参考資料 / パス変数 を参照）

---

## 参考資料

### イベント対応表

| ユーザーの発言 | イベント名 | 注入タイミング |
|---|---|---|
| 「ユーザーが入力するたびに」「プロンプト送信後」 | `UserPromptSubmit` | Claude が処理する前 |
| 「Claude が応答を終えたとき」「作業完了後」「Stop 時」 | `Stop` | Claude が停止したとき |
| 「ツール実行前」「Bash 実行前に確認したい」 | `PreToolUse` | ツール実行前（ブロック可） |
| 「ツール実行後」「ファイル編集後」 | `PostToolUse` | ツール実行後 |
| 「セッション開始時」 | `SessionStart` | セッション起動時 |

### パス変数

| 変数 | 使える場所 | 意味 |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | **プラグインの hooks.json のみ** | プラグインのインストール先ルート |
| `${CLAUDE_PROJECT_DIR}` | settings.json / settings.local.json | プロジェクトルート |
| `${CLAUDE_PLUGIN_DATA}` | プラグインの hooks.json のみ | プラグインの永続データディレクトリ |

> ⚠️ `${CLAUDE_PLUGIN_ROOT}` はプラグインとしてインストールされたときのみ展開される。
> プロジェクト直置きの settings.json では機能しないため、`${CLAUDE_PROJECT_DIR}` を使うこと。

---

### フックパターン一覧

#### [プラグイン用] UserPromptSubmit

プラグインの `hooks/hooks.json` に記述。`${CLAUDE_PLUGIN_ROOT}` が使える。

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else sys.exit(0)",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/user-prompt-submit.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プロジェクト用] UserPromptSubmit

`.claude/settings.json` または `.claude/settings.local.json` の `hooks` セクションに記述。
プロンプトファイルは `.claude/hooks/{name}.md` に置く。

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else sys.exit(0)",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/user-prompt-submit.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プラグイン用] Stop

`stop_hook_active` チェックで無限ループを防止する。
stdout に JSON `{"decision":"block","reason":"<プロンプト>"}` を返すことで Claude に作業を継続させる。

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else None",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プロジェクト用] Stop

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else None",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プロジェクト用] PreToolUse — ツール実行前にブロック（無条件）

`matcher` でツールを絞り込める。**すべての実行をブロック**したい場合はこのパターン。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else sys.exit(0)",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プロジェクト用] PreToolUse — 条件付きブロック＋ループ防止（ワンタイムトークン）

**「毎回確認を求めるが、確認後は1回だけ通す」** パターン。
無条件ブロックのままだとClaude が再試行するたびにブロックされ続ける（無限ループ）ため、ワンタイムトークンで防止する。

仕組み:
1. フックが条件に一致 → トークンなし → **ブロック** + トークンファイルを作成
2. Claude がユーザーに確認 → ユーザーが承認 → Claude が同じコマンドを再実行
3. フックが再び発火 → トークンあり → **トークン削除** + 通過（exit 0）
4. 次回同じコマンド → トークンなし → また**ブロック**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib,re,tempfile; d=json.loads(sys.stdin.read()); cmd=d.get('tool_input',{}).get('command',''); sys.exit(0) if not re.search(r'\\bgit\\s+(push|merge)\\b',cmd) else None; token=pathlib.Path(tempfile.gettempdir())/f'my-guard-token-{d.get(\"session_id\",\"default\")}'; token.unlink() or sys.exit(0) if token.exists() else None; token.touch(); p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else sys.exit(0)",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.md"
            ]
          }
        ]
      }
    ]
  }
}
```

> ⚠️ トークンファイル名はフックごとにユニークな名前にすること。複数のフックが同じ名前を使うとトークンが干渉する。
> ✅ `session_id` をファイル名に含めることで、複数の Claude Code セッションが同時に動いていてもトークンが干渉しない（セッション分離）。`session_id` は stdin JSON の `d.get('session_id', 'default')` で取得できる。

---

### ループ防止

ブロック系フック（`Stop` / `PreToolUse`）は、ブロックに応答した Claude がまた同じ操作をすることで無限ループになる場合がある。

| フック | 問題 | 防止策 |
|---|---|---|
| `Stop` | Claude が作業を続けて → また Stop → フックが発火 → 無限ループ | `stop_hook_active` フラグで2回目以降をスキップ |
| `PreToolUse` | Claude が再試行 → フックがまたブロック → 無限ループ | ワンタイムトークンで「ブロック→通過」を1サイクルに制御 |

#### Stop フックのループ防止

stdin JSON に `stop_hook_active: true` が含まれている場合はフックが再発火中なので `exit(0)` で抜ける。

```python
d = json.loads(sys.stdin.read())
if d.get('stop_hook_active'):
    sys.exit(0)  # 再発火 → スルー
# ↓ 通常の処理
```

#### PreToolUse フックのループ防止（ワンタイムトークン）

`stop_hook_active` は PreToolUse には存在しない。代わりに一時ファイルをトークンとして使う。

```python
import tempfile, pathlib

# session_id でセッションごとにトークンを分離する
session_id = d.get('session_id', 'default')
token = pathlib.Path(tempfile.gettempdir()) / f'my-guard-token-{session_id}'

if token.exists():
    token.unlink()   # トークンを消費
    sys.exit(0)      # 今回は通過

# トークンなし → ブロック + トークン作成
token.touch()
# → ブロック処理へ
```

ポイント:
- ブロック時にトークンを**作成**
- 次回実行時にトークンを**消費**して通過
- その次はまたブロック（毎回確認が必要なフックに適している）
- `session_id` を含めることで **複数セッション間の干渉を防止**（セッション A のトークンをセッション B が消費することがなくなる）
- `session_id` は PreToolUse の stdin JSON に `"session_id": "..."` として含まれている
