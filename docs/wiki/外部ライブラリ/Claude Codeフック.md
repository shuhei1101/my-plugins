---
template_version: 1.0.0
---

# Claude Code フック

Claude Code のライフサイクル上の各時点で外部コマンドを実行し、その結果で挙動を制御する仕組み。

ツール実行の許可 / 拒否、コンテキストへのテキスト追加、セッション開始時の環境変数設定などを、Claude 本体に手を入れずに差し込める。
設定は JSON で宣言し、フック側は標準入出力の JSON で会話する。

## 現在のバージョン情報

| 項目 | 内容 | 補足 |
| --- | --- | --- |
| バージョン | Claude Code `v2.1.199` 時点の仕様 | 2026-07-25 時点最新 |
| ライセンス | - | Claude Code 本体の機能 |
| 公式 URL | https://code.claude.com/docs/ja/hooks | - |
| 公式ドキュメント | https://code.claude.com/docs/ja/hooks | - |

## インストール手順

インストールは不要。
設定ファイルにフックを宣言すると有効になる。

宣言できる場所は 4 つあり、下にいくほどスコープが狭い。

| 置き場所 | スコープ | git 共有 |
| --- | --- | --- |
| `~/.claude/settings.json` | 全プロジェクト | 不可 |
| `.claude/settings.json` | 単一プロジェクト | 可 |
| `.claude/settings.local.json` | 単一プロジェクト | 不可 |
| プラグインの `hooks/hooks.json` | プラグイン有効時 | 可（プラグイン同梱） |

スキル / エージェントの YAML フロントマターにも同じ書式で宣言でき、そのコンポーネントが動いている間だけ有効になる。

## API 一覧

バージョン: `v2.1.199`

| 種別 | 名前 | 用途 | 補足 |
| --- | --- | --- | --- |
| 設定 | [`hooks`](#hooks) | イベント名 → マッチャー → フック定義の 3 階層 | 設定ファイルのルート |
| 設定 | [`matcher`](#matcher) | イベントを絞り込む条件 | ツール名・トリガー種別などイベントごとに対象が違う |
| 設定 | [`type: "command"`](#type-command) | 外部コマンドを実行するフック | 最も基本的な型 |
| イベント | [`SessionStart`](#sessionstart) | セッション開始・再開時 | 環境変数の設定に使える唯一のタイミング群の 1 つ |
| イベント | [`PreToolUse`](#pretooluse) | ツール実行の直前 | 許可 / 拒否・入力書き換え・コンテキスト追加 |
| イベント | [`PostToolUse`](#posttooluse) | ツール成功後 | 出力の書き換え・コンテキスト追加 |
| イベント | [`UserPromptSubmit`](#userpromptsubmit) | ユーザーのプロンプト送信前 | プロンプトのブロック・コンテキスト追加 |
| イベント | [`PreCompact`](#precompact) | コンテキスト圧縮の前 | 圧縮前の後始末 |
| イベント | [`Stop`](#stop) | Claude の応答完了時 | 応答を続行させることもできる |
| 入出力 | [`共通入力フィールド`](#共通入力フィールド) | 全イベントに渡る標準入力の JSON | - |
| 入出力 | [`共通出力フィールド`](#共通出力フィールド) | 全イベント共通の標準出力の JSON | - |
| 入出力 | [`終了コード`](#終了コード) | JSON を使わずに制御する方法 | `2` がブロック |
| 変数 | [`パスプレースホルダー`](#パスプレースホルダー) | 設定内で使える置換変数 | `${CLAUDE_PLUGIN_ROOT}` 等 |
| 変数 | [`環境変数`](#環境変数) | フックプロセスに渡る環境変数 | `OTEL_*` は削除される |

### `hooks`

設定ファイルのルートに置くオブジェクト。
イベント名 → マッチャーの配列 → フック定義の配列、の 3 階層で書く。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `hooks` | `dict[str, object[]]` | 必須 | - | イベント名をキーにしたマッチャー配列 | キーは `PreToolUse` などのイベント名 |
| `hooks.{event}[].matcher` | `str` | 任意 | 全マッチ | イベントを絞り込む条件 | 詳細は [`matcher`](#matcher) |
| `hooks.{event}[].hooks` | `object[]` | 必須 | - | 実行するフックの定義 | 上から順に全て実行される |
| `hooks.{event}[].hooks[].type` | `'command' or 'http' or 'mcp_tool' or 'prompt' or 'agent'` | 必須 | - | フックの実行方式 | command=外部コマンド / http=HTTP POST / mcp_tool=MCP ツール呼び出し |
| `hooks.{event}[].hooks[].timeout` | `int` | 任意 | 600（command / http / mcp_tool）| タイムアウト秒数 | `UserPromptSubmit` は既定 30 秒、`MessageDisplay` は 10 秒 |
| `hooks.{event}[].hooks[].if` | `str` | 任意 | なし | 権限ルール構文での追加フィルタ | ツール呼び出し系イベントのみ。例: `Bash(git *)` |
| `hooks.{event}[].hooks[].statusMessage` | `str` | 任意 | なし | 実行中に表示する文言 | - |
| `disableAllHooks` | `bool` | 任意 | `false` | 全フックの無効化 | ルート直下に置く |

パラメータ例:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Read",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/inject-rules/injector.py"]
          }
        ]
      }
    ]
  }
}
```

### `matcher`

イベントを絞り込む条件。
文字構成によって完全一致か正規表現かが自動で切り替わる。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `matcher` | `str` | 任意 | 全マッチ | 絞り込み条件 | `"*"` / `""` / 省略で全マッチ |

判定規則:

| 値の構成 | 評価方法 | 例 |
| --- | --- | --- |
| 英数字・`_`・`-`・空白・`,`・`\|` のみ | 完全一致または `\|` 区切りのリスト | `Bash` / `Edit\|Write` |
| それ以外の文字を含む | JavaScript 正規表現 | `^Notebook` / `mcp__memory__.*` |

マッチ対象はイベントごとに異なる。

| イベント | マッチ対象 | 値の例 |
| --- | --- | --- |
| `PreToolUse` / `PostToolUse` | ツール名 | `Bash` / `Edit\|Write` / `mcp__memory__.*` |
| `SessionStart` | 開始方法 | `startup` / `resume` / `clear` / `compact` |
| `PreCompact` / `PostCompact` | 圧縮の契機 | `manual` / `auto` |
| `SessionEnd` | 終了理由 | `clear` / `resume` / `logout` / `other` |
| `SubagentStart` / `SubagentStop` | エージェント名 | `Explore` / カスタム名 |

MCP ツールは `mcp__{サーバー名}__{ツール名}` の形でツール名として現れる。

パラメータ例:

```json
{ "matcher": "Edit|Write|Read" }
```

### `type: "command"`

外部コマンドを実行するフック。
標準入力に JSON が渡り、標準出力の JSON と終了コードで結果を返す。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `command` | `str` | 必須 | - | 実行するコマンド | `args` の有無で解釈が変わる |
| `args` | `str[]` | 任意 | なし | コマンドの引数 | 指定すると exec 形式、省略するとシェル形式 |
| `async` | `bool` | 任意 | `false` | バックグラウンド実行 | 結果を待たない |
| `asyncRewake` | `bool` | 任意 | `false` | バックグラウンド実行し、終了コード 2 で Claude を起こす | - |
| `shell` | `'bash' or 'powershell'` | 任意 | `bash` | シェル形式で使うシェル | Windows は PowerShell が既定 |

形式の違い:

| 形式 | 条件 | 挙動 |
| --- | --- | --- |
| exec 形式 | `args` あり | `command` を実行ファイルとして直接起動。パイプ・リダイレクトは使えない。パスにスペースがあっても引用符不要 |
| シェル形式 | `args` なし | `command` 文字列をシェルで解釈。パイプ・`&&`・変数展開が使える |

パラメータ例:

```json
{
  "type": "command",
  "command": "python",
  "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/inject-rules/injector.py"],
  "timeout": 30
}
```

### `SessionStart`

セッションの開始・再開時に 1 回発火する。
環境変数をセッション全体へ渡せる数少ないイベントの 1 つ。

#### パラメータ

標準入力に渡るイベント固有フィールド。

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `source` | `'startup' or 'resume' or 'clear' or 'compact'` | 必須 | - | セッションの開始方法 | matcher の対象 |
| `model` | `str` | 任意 | - | 使用モデル | 例: `claude-sonnet-5` |
| `session_title` | `str` | 任意 | - | セッション名 | - |

パラメータ例:

```json
{ "session_id": "abc123", "hook_event_name": "SessionStart", "source": "startup", "model": "claude-sonnet-5" }
```

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `hookSpecificOutput.additionalContext` | `str` | 会話の冒頭に差し込むテキスト | - |
| `hookSpecificOutput.initialUserMessage` | `str` | 最初のユーザー発話として扱うテキスト | - |
| `hookSpecificOutput.sessionTitle` | `str` | セッション名の設定 | - |
| `hookSpecificOutput.watchPaths` | `str[]` | 変更監視するパス | `FileChanged` の対象になる |
| `hookSpecificOutput.reloadSkills` | `bool` | スキルの再スキャン | - |

戻り値例:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "環境の準備ができました"
  }
}
```

環境変数の受け渡しは戻り値ではなく `CLAUDE_ENV_FILE` への追記で行う（[環境変数](#環境変数) 参照）。

### `PreToolUse`

ツール呼び出しの直前に、呼び出しごとに発火する。
許可 / 拒否の決定、入力の書き換え、コンテキストの追加ができる。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `tool_name` | `str` | 必須 | - | 実行しようとしているツール名 | matcher の対象 |
| `tool_input` | `dict` | 必須 | - | ツールへの入力 | 中身はツールごとに異なる |
| `tool_use_id` | `str` | 必須 | - | ツール呼び出しの識別子 | `PostToolUse` と対応づく |

主なツールの `tool_input`:

| ツール | 主なフィールド |
| --- | --- |
| `Edit` | `file_path` / `old_string` / `new_string` / `replace_all` |
| `Write` | `file_path` / `content` |
| `Read` | `file_path` / `offset` / `limit` |
| `Bash` | `command` / `description` / `timeout` / `run_in_background` |
| `Grep` | `pattern` / `path` / `glob` / `output_mode` |
| `WebFetch` | `url` / `prompt` |

パラメータ例:

```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": { "file_path": "/repo/docs/wiki/テンプレート/結合.md", "old_string": "a", "new_string": "b" },
  "tool_use_id": "tool_use_abc123"
}
```

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `hookSpecificOutput.permissionDecision` | `'allow' or 'deny' or 'ask' or 'defer'` | ツール実行の可否 | allow=許可 / deny=拒否 / ask=ユーザーに確認 / defer=通常の権限フローに委ねる |
| `hookSpecificOutput.permissionDecisionReason` | `str` | 判断の理由 | ユーザーに表示される |
| `hookSpecificOutput.additionalContext` | `str` | ツール結果の横に差し込むテキスト | - |
| `hookSpecificOutput.updatedInput` | `dict` | 書き換えた `tool_input` | 指定したフィールドだけ差し替わる |

戻り値例:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "additionalContext": "このファイルには次の規約が適用されます: ..."
  }
}
```

`deny` はエラーではない。
ツールを実行せずに Claude へ制御が戻るため、コンテキストを追加してから再試行させる用途に使える。

### `PostToolUse`

ツール呼び出しが成功した後に発火する。
既に実行済みのためブロックはできないが、出力の書き換えとコンテキスト追加ができる。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `tool_name` | `str` | 必須 | - | 実行されたツール名 | - |
| `tool_input` | `dict` | 必須 | - | ツールへの入力 | - |
| `tool_response` | `str` | 必須 | - | ツールの出力 | - |
| `tool_use_id` | `str` | 必須 | - | ツール呼び出しの識別子 | - |

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `hookSpecificOutput.additionalContext` | `str` | ツール結果の横に差し込むテキスト | - |
| `hookSpecificOutput.updatedToolOutput` | `str` | 差し替える出力テキスト | - |
| `decision` | `'block'` | Claude に差し戻す | トップレベルに置く。`reason` と併用 |

### `UserPromptSubmit`

ユーザーがプロンプトを送信した直後、Claude が処理する前に発火する。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `prompt` | `str` | 必須 | - | ユーザーの入力テキスト | - |

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `hookSpecificOutput.additionalContext` | `str` | プロンプトの横に差し込むテキスト | - |
| `hookSpecificOutput.sessionTitle` | `str` | セッション名の設定 | - |
| `hookSpecificOutput.suppressOriginalPrompt` | `bool` | 元のプロンプトを隠す | - |
| `decision` | `'block'` | プロンプトの処理を中止する | トップレベルに置く。`reason` と併用 |

### `PreCompact`

コンテキスト圧縮の直前に発火する。
圧縮でコンテキストが失われる前の後始末に使う。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `trigger` | `'manual' or 'auto'` | 必須 | - | 圧縮の契機 | matcher の対象 |

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `decision` | `'block'` | 圧縮を中止する | トップレベルに置く。`reason` と併用 |

### `Stop`

Claude が応答を終えたときに発火する。
`decision: "block"` を返すと停止せずに会話を続けさせられる。

#### パラメータ

| パラメータ | 型 | 必須 | 既定 | 説明 | 補足 |
| --- | --- | --- | --- | --- | --- |
| `last_assistant_message` | `str` | 必須 | - | Claude の最終応答テキスト | - |
| `turn_id` | `str` | 必須 | - | ターンの識別子 | - |
| `tool_calls_made` | `int` | 必須 | - | そのターンのツール呼び出し回数 | - |

#### 戻り値

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `hookSpecificOutput.additionalContext` | `str` | ターン終了時に差し込むテキスト | Claude が応答できる |
| `decision` | `'block'` | 停止させず会話を続行する | トップレベルに置く。`reason` と併用 |

### `共通入力フィールド`

全イベントの標準入力に含まれるフィールド。

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `session_id` | `str` | セッション識別子 | セッション単位の状態保存のキーに使える |
| `prompt_id` | `str` | プロンプトの UUID | 最初のプロンプトまでは存在しない |
| `transcript_path` | `str` | 会話ログ（JSONL）のパス | - |
| `cwd` | `str` | フック実行時の作業ディレクトリ | - |
| `permission_mode` | `str` | 権限モード | `default` / `plan` / `acceptEdits` / `bypassPermissions` 等 |
| `hook_event_name` | `str` | 発火したイベント名 | - |
| `agent_id` | `str` | サブエージェントの識別子 | サブエージェント内でのみ存在 |
| `agent_type` | `str` | エージェント種別 | サブエージェント内 / `--agent` 指定時 |

### `共通出力フィールド`

全イベントの標準出力で使えるフィールド。

| フィールド | 型 | 説明 | 補足 |
| --- | --- | --- | --- |
| `continue` | `bool` | `false` で Claude を完全に停止する | - |
| `stopReason` | `str` | 停止理由 | `continue: false` のときユーザーに表示 |
| `suppressOutput` | `bool` | デバッグログに出さない | - |
| `systemMessage` | `str` | ユーザーの端末に出す文言 | 進捗表示などに使う |
| `hookSpecificOutput.hookEventName` | `str` | イベント名 | イベント固有フィールドとセットで必須 |

標準出力が空の場合は「何もしない」を意味し、処理はそのまま続行する。

### `終了コード`

JSON を出力せずに終了コードだけで制御することもできる。

| 終了コード | 意味 | 標準出力の扱い | 動作 |
| --- | --- | --- | --- |
| `0` | 成功 | JSON として解釈する | イベントごとの通常処理 |
| `2` | ブロッキングエラー | 無視する | イベントごとにアクションを止める |
| その他 | 非ブロッキングエラー | 無視する | 標準エラーを表示して続行 |

終了コード `2` でブロックできる主なイベント:

| イベント | ブロック時の動作 |
| --- | --- |
| `PreToolUse` | ツール呼び出しを止める |
| `UserPromptSubmit` | プロンプトの処理を止めて入力を消す |
| `Stop` | Claude を停止させず会話を続ける |
| `PreCompact` | 圧縮を止める |

`PostToolUse` / `SessionStart` / `SessionEnd` などはブロックできず、標準エラーが表示されるだけになる。

### `パスプレースホルダー`

設定ファイル内で使える置換変数。

| プレースホルダー | 説明 | 補足 |
| --- | --- | --- |
| `${CLAUDE_PROJECT_DIR}` | プロジェクトのルート | - |
| `${CLAUDE_PLUGIN_ROOT}` | プラグインのインストール先 | プラグインのフックから自分のファイルを指すのに使う |
| `${CLAUDE_PLUGIN_DATA}` | プラグインの永続データ置き場 | - |

exec 形式（`args` あり）ではプレーンな文字列置換になるため、パスにスペースがあっても引用符は不要。
シェル形式ではシェル変数展開が起きるため引用符が必要になる。

### `環境変数`

フックプロセスに渡る環境変数。

| 変数 | 説明 | 渡るイベント | 補足 |
| --- | --- | --- | --- |
| `CLAUDE_PROJECT_DIR` | プロジェクトのルート | 全イベント | - |
| `CLAUDE_PLUGIN_ROOT` | プラグインのインストール先 | 全イベント（プラグインのフック） | - |
| `CLAUDE_PLUGIN_DATA` | プラグインの永続データ置き場 | 全イベント（プラグインのフック） | - |
| `CLAUDE_ENV_FILE` | セッションへ環境変数を渡すためのファイル | `SessionStart` / `Setup` / `CwdChanged` / `FileChanged` | このファイルに `export KEY=value` を追記するとセッション全体に反映される |
| `CLAUDE_CODE_REMOTE` | リモート環境かどうか | 全イベント | ローカルでは未設定 |
| `CLAUDE_PLUGIN_OPTION_{KEY}` | プラグイン設定の値 | 全イベント（プラグインのフック） | - |

`OTEL_` で始まる変数は Claude Code が全てのサブプロセスから削除するため、フックには届かない。
観測基盤の送信先などをフックへ渡す場合は別の名前を使う。

パラメータ例:

```bash
# SessionStart フックからセッション全体へ環境変数を渡す
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export INJECT_RULES_INDEXES=https://example.com/rules.yaml' >> "$CLAUDE_ENV_FILE"
fi
```
