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
- `Stop` フック: stdout テキスト → Claude のコンテキストへ注入して作業を継続させる
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

2. `Stop` または `PreToolUse` ブロック用の場合: `stop_hook_active` チェックが必要であることをユーザーに説明する

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
stdout にプロンプトテキストを書き出すと Claude のコンテキストへ注入される（UserPromptSubmit と同じ方式）。

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
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else None",
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
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else None",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

#### [プロジェクト用] PreToolUse — ツール実行前にブロック

`matcher` でツールを絞り込める。

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
