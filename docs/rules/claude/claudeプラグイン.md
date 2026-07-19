# Claude プラグインルール

## テンプレートフォルダ

- プラグイン内のスキルなどで共通する出力形式や、重複している記載はテンプレート形式を用いる
  - {プラグインフォルダ}/templates/{日本語名}.md
- スキル内ではcatで展開する

```
<!-- 任意のスキルファイル -->
!`cat xxx/xxx.md`
```


## フックフォルダの定義
- フォルダ構成は以下とする
  - {CLAUDE_PLUGIN_ROOT}/hooks/hooks.json
  - {CLAUDE_PLUGIN_ROOT}/hooks/{フック名}/{任意のスクリプトやj2, mdファイル}
    - 例: hooks/pre-tool-use/xxx.py

## 定数管理ルール

- プラグイン作成時は必ず `{CLAUDE_PLUGIN_ROOT}/scripts/constants.sh` を用意する
- `constants.sh` には以下のルールを適用すること
  - `#!/usr/bin/env bash` で始める
  - 定数名にはプラグイン名をアッパースネークケースで付与する（例: `GH_KIT_LABEL_WIP`）
  - 各変数は `echo "export VAR=VALUE" >> "$CLAUDE_ENV_FILE"` で `$CLAUDE_ENV_FILE` に追記する
    - **`export VAR=VALUE` だけでは不可**: サブシェルで実行されるため、親プロセス（Claude Code）に環境変数が伝わらない
    - `$CLAUDE_ENV_FILE` への追記により Claude Code がセッション開始時に環境変数として読み込む
- `hooks/hooks.json` の `SessionStart` フックで `constants.sh` を自動実行する

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "_description": "{プラグイン名} 定数をセッション内に展開する",
            "type": "command",
            "command": "bash",
            "args": [
              "${CLAUDE_PLUGIN_ROOT}/scripts/constants.sh"
            ]
          }
        ]
      }
    ]
  }
}
```

- スキル・エージェントファイル内では手動 `source` を呼ばない（Session Start で展開済みのため不要）
