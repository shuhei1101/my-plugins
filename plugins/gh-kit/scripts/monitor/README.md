# gh-kit Monitor Daemons

`*-auto` 系スキルのポーリング・キック処理をシェルデーモン化したスクリプト群。
Claude のメインセッションを占有せずに、`claude -p` ヘッドレス呼び出しで AI 処理を実行する。

## スクリプト一覧

| スクリプト | 対応ラベル | 呼び出すスキル |
|---|---|---|
| `issue-review-daemon.sh` | `確認:issue-reviewer` | `/gh-kit:issue-review` |

## 動機

従来の `*-auto` スキルは Claude の `Monitor` ツールでポーリングしていたため:
- ポーリングごとに context 展開コストがかかる（prompt cache miss）
- メインセッションが占有されユーザーが他の作業をできない
- `flock` などの機械的な排他制御がなく、並列禁止はプロンプト記述頼みだった

シェルデーモン + `claude -p` に移行することで、これらの問題を解消する。

## issue-review-daemon.sh

`確認:issue-reviewer` ラベル付き Issue を 30 秒ポーリングし、`claude -p` でヘッドレス実行する。

### 必須環境変数

| 変数 | 説明 |
|---|---|
| `GH_KIT_PLUGIN_DIR` | gh-kit プラグインのディレクトリパス |
| `MCP_CONFIG_PATH` | MCP 設定ファイル（JSON）のパス |

### オプション環境変数

| 変数 | デフォルト | 説明 |
|---|---|---|
| `AI_TOOL` | `claude` | 使用する AI CLI ツール（`claude` / `codex`） |
| `POLL_INTERVAL` | `30` | ポーリング間隔（秒） |
| `MAX_TURNS` | `50` | `claude -p` の最大ターン数 |
| `MAX_BUDGET_USD` | `2.00` | `claude -p` の最大予算（USD） |
| `LOCK_FILE` | `/tmp/gh-kit-issue-review.lock` | flock ロックファイルパス |

### claude -p 呼び出しフラグ

```bash
claude -p "/gh-kit:issue-review $ISSUE_NUMBER" \
  --plugin-dir "$GH_KIT_PLUGIN_DIR" \
  --mcp-config "$MCP_CONFIG_PATH" \
  --strict-mcp-config \
  --permission-mode dontAsk \
  --allowedTools "Bash,Read,Edit,Write,WebFetch" \
  --max-turns 50 \
  --max-budget-usd 2.00 \
  --output-format json \
  --no-session-persistence
```

- `--plugin-dir`: gh-kit プラグインをこのセッションにロード（スキル展開が有効）
- `--strict-mcp-config` + `--mcp-config`: 指定した MCP サーバーのみ使用
- `--permission-mode dontAsk`: 権限プロンプトを出さずに許可済みツールのみ実行
- `--max-turns` + `--max-budget-usd`: 暴走防止の二重セーフティ
- `--output-format json`: 結果を JSON で受け取り `jq` でハンドリング
- `--no-session-persistence`: 履歴ファイルの肥大化を防止

### AI ツール切り替え（Codex 対応）

`AI_TOOL` 環境変数で `claude` / `codex` を切り替え可能。
フェーズ 1 では `claude` のみ実装。Codex 対応は Issue #244 参照。

```bash
AI_TOOL=codex \
  GH_KIT_PLUGIN_DIR=/path/to/gh-kit \
  MCP_CONFIG_PATH=/path/to/mcp-config.json \
  ./issue-review-daemon.sh
```

---

## 常駐起動方法

### 1. tmux（推奨: 開発環境）

```bash
# セッション作成して起動
tmux new-session -d -s issue-review-daemon \
  "GH_KIT_PLUGIN_DIR=/path/to/gh-kit \
   MCP_CONFIG_PATH=/path/to/mcp-config.json \
   /path/to/issue-review-daemon.sh 2>&1 | tee /tmp/issue-review-daemon.log"

# ログ確認
tmux attach -t issue-review-daemon
# または
tail -f /tmp/issue-review-daemon.log

# 停止
tmux kill-session -t issue-review-daemon
```

### 2. nohup（推奨: サーバー簡易常駐）

```bash
export GH_KIT_PLUGIN_DIR=/path/to/gh-kit
export MCP_CONFIG_PATH=/path/to/mcp-config.json

nohup /path/to/issue-review-daemon.sh \
  >> /var/log/issue-review-daemon.log 2>&1 &

echo "PID: $!"
```

ログは `/var/log/issue-review-daemon.log` に追記される。

### 3. systemd（推奨: Linux サーバー本格運用）

`/etc/systemd/system/gh-kit-issue-review.service` を作成:

```ini
[Unit]
Description=gh-kit Issue Review Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USER
Environment=GH_KIT_PLUGIN_DIR=/path/to/gh-kit
Environment=MCP_CONFIG_PATH=/path/to/mcp-config.json
Environment=ANTHROPIC_API_KEY=your-api-key
ExecStart=/path/to/issue-review-daemon.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
# 有効化・起動
sudo systemctl daemon-reload
sudo systemctl enable gh-kit-issue-review
sudo systemctl start gh-kit-issue-review

# 状態確認
sudo systemctl status gh-kit-issue-review

# ログ確認
journalctl -u gh-kit-issue-review -f

# 停止
sudo systemctl stop gh-kit-issue-review
```

---

## 認証

`--permission-mode dontAsk` を使う場合、`ANTHROPIC_API_KEY` 環境変数が必要。

```bash
# API キーで認証
export ANTHROPIC_API_KEY=sk-ant-...

# または claude setup-token で長寿命 OAuth トークンを設定
claude setup-token
```

---

## アーキテクチャ

```
issue-review-daemon.sh
  ├── while true (30s ポーリング)
  │     ├── gh issue list → 対象 Issue を優先度順で取得
  │     └── Issue あり → flock 取得 → claude -p /gh-kit:issue-review {N}
  │                          │
  │                          └── /gh-kit:issue-review スキルが実行
  │                                ├── Issue レビュー（AI）
  │                                ├── コメント投稿
  │                                └── ラベル付け替え（確認: 除去、処理中: 除去など）
  └── sleep POLL_INTERVAL

flock /tmp/gh-kit-issue-review.lock
  └── 同時実行を機械的に 1 並列に制限（複数デーモン起動時も安全）
```

## 関連

- Issue #243: 設計・方針
- Issue #244: Codex 対応（AI_TOOL 切り替え）
- `plugins/gh-kit/skills/issue-review-auto/SKILL.md`: 旧実装（Monitor ベース）
- `plugins/gh-kit/skills/issue-review/SKILL.md`: レビュー実体スキル
