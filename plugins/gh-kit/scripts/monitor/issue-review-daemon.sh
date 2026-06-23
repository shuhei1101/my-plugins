#!/usr/bin/env bash
# issue-review-daemon.sh
# 「確認:issue-reviewer」ラベル付き Issue を claude -p で直列処理するシェルデーモン。
#
# 使い方:
#   # 基本起動
#   GH_KIT_PLUGIN_DIR=/path/to/gh-kit \
#   MCP_CONFIG_PATH=/path/to/mcp-config.json \
#   ./issue-review-daemon.sh
#
#   # systemd / tmux / nohup での常駐起動については docs/daemon-setup.md を参照
#
# 環境変数:
#   GH_KIT_PLUGIN_DIR   gh-kit プラグインのディレクトリパス（必須）
#   MCP_CONFIG_PATH     MCP 設定ファイルパス（必須）
#   AI_TOOL             使用する AI CLI ツール (claude / codex) [デフォルト: claude]
#   POLL_INTERVAL       ポーリング間隔（秒）[デフォルト: 30]
#   MAX_BUDGET_USD      claude -p の最大予算（USD）[デフォルト: 2.00]
#   LOCK_FILE           flock に使うロックファイルパス [デフォルト: /tmp/gh-kit-issue-review.lock]

set -euo pipefail

# ─── 設定 ────────────────────────────────────────────────────────────────────

GH_KIT_PLUGIN_DIR="${GH_KIT_PLUGIN_DIR:-}"
MCP_CONFIG_PATH="${MCP_CONFIG_PATH:-}"
AI_TOOL="${AI_TOOL:-claude}"
POLL_INTERVAL="${POLL_INTERVAL:-30}"
MAX_BUDGET_USD="${MAX_BUDGET_USD:-2.00}"
LOCK_FILE="${LOCK_FILE:-${TMPDIR:-/tmp}/gh-kit-issue-review.lock}"

# ラベル定数（constants.sh が source されていない場合のデフォルト値）
GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW="${GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW:-確認:issue-reviewer}"
GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER="${GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER:-処理中:issue-reviewer}"
GH_KIT_LABEL_PRIORITY_URGENT="${GH_KIT_LABEL_PRIORITY_URGENT:-優先度:急ぎ}"
GH_KIT_LABEL_PRIORITY_LOW="${GH_KIT_LABEL_PRIORITY_LOW:-優先度:いつでも}"

# ─── 事前チェック ────────────────────────────────────────────────────────────

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

die() {
  log "ERROR: $*"
  exit 1
}

if [ -z "$GH_KIT_PLUGIN_DIR" ]; then
  die "GH_KIT_PLUGIN_DIR が未設定です。gh-kit プラグインのディレクトリパスを指定してください。"
fi

if [ ! -d "$GH_KIT_PLUGIN_DIR" ]; then
  die "GH_KIT_PLUGIN_DIR='$GH_KIT_PLUGIN_DIR' が存在しません。"
fi

if [ -z "$MCP_CONFIG_PATH" ]; then
  die "MCP_CONFIG_PATH が未設定です。MCP 設定ファイルのパスを指定してください。"
fi

if [ ! -f "$MCP_CONFIG_PATH" ]; then
  die "MCP_CONFIG_PATH='$MCP_CONFIG_PATH' が存在しません。"
fi

if ! command -v "$AI_TOOL" >/dev/null 2>&1; then
  die "AI_TOOL='$AI_TOOL' が見つかりません。インストールされているか確認してください。"
fi

if ! command -v gh >/dev/null 2>&1; then
  die "gh (GitHub CLI) が見つかりません。インストールされているか確認してください。"
fi

if ! command -v jq >/dev/null 2>&1; then
  die "jq が見つかりません。インストールされているか確認してください。"
fi

if ! command -v flock >/dev/null 2>&1; then
  die "flock が見つかりません。インストールされているか確認してください。"
fi

log "issue-review-daemon 起動"
log "  AI_TOOL=${AI_TOOL}"
log "  GH_KIT_PLUGIN_DIR=${GH_KIT_PLUGIN_DIR}"
log "  MCP_CONFIG_PATH=${MCP_CONFIG_PATH}"
log "  POLL_INTERVAL=${POLL_INTERVAL}s"
log "  MAX_BUDGET_USD=${MAX_BUDGET_USD}"
log "  LOCK_FILE=${LOCK_FILE}"

# ─── 対象 Issue 取得（優先度順ソート、処理中除外）───────────────────────────

get_next_issue() {
  gh issue list --state open \
    --label "$GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW" \
    --json number,labels \
    --jq "
      [.[] | select(
        .labels | map(.name) | (map(startswith(\"処理中:\")) | any | not)
      )]
      | sort_by(
          if (.labels | map(.name) | index(\"$GH_KIT_LABEL_PRIORITY_URGENT\")) then 0
          elif (.labels | map(.name) | index(\"$GH_KIT_LABEL_PRIORITY_LOW\")) then 1
          else 2
          end,
          .number
        )
      | .[0].number // empty
    " 2>/dev/null || true
}

# ─── claude -p でヘッドレス実行 ─────────────────────────────────────────────

run_issue_review() {
  local issue_number="$1"

  log "Issue #${issue_number} のレビューを開始します"

  # 処理中ラベルを付与（排他マーカー）
  gh issue edit "$issue_number" --add-label "$GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER" 2>/dev/null || {
    log "WARN: 処理中ラベルの付与に失敗しました（Issue #${issue_number}）"
  }

  # 関数終了時に必ず処理中ラベルを除去する（孤児化防止）
  # issue-review スキルが正常完了した場合も冗長に除去する（二重除去は無害）
  trap "gh issue edit \"$issue_number\" --remove-label \"$GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER\" 2>/dev/null || true" RETURN

  local exit_code=0

  # サブシェル + 専用ロック fd 方式で flock 排他制御
  # exit 200: flock -n でロック取得失敗（別インスタンス実行中）
  # exit 0  : claude -p 正常完了
  # その他  : claude -p 異常終了（タイムアウト / SIGINT / 予算枯渇 / MAX_TURNS など）
  (
    flock -n 9 || exit 200
    "$AI_TOOL" -p "/gh-kit:issue-review $issue_number" \
      --plugin-dir "$GH_KIT_PLUGIN_DIR" \
      --mcp-config "$MCP_CONFIG_PATH" \
      --strict-mcp-config \
      --permission-mode dontAsk \
      --allowedTools "Bash,Read,Edit,Write,WebFetch" \
      --max-budget-usd "$MAX_BUDGET_USD" \
      --output-format json \
      --no-session-persistence \
    2>&1 | tee /dev/stderr
  ) 9>"$LOCK_FILE" || exit_code=$?

  if [ "$exit_code" -eq 200 ]; then
    # flock -n でロック取得失敗（別インスタンス実行中）
    log "SKIP: ロック取得失敗 — 別インスタンスが実行中です（Issue #${issue_number}）"
    # trap RETURN でラベルは除去される
    return
  fi

  if [ "$exit_code" -ne 0 ]; then
    log "ERROR: claude -p が異常終了しました（Issue #${issue_number}, exit_code=${exit_code}）"
    log "  処理中ラベルを除去してキューに戻します"
    # trap RETURN でラベルは除去される
    return
  fi

  log "Issue #${issue_number} のレビューが完了しました（exit_code=${exit_code}）"
  # trap RETURN による処理中ラベル除去は冗長だが無害（issue-review スキルが既に除去済みのケースも想定）
}

# ─── メインループ ────────────────────────────────────────────────────────────

log "ポーリング開始（間隔: ${POLL_INTERVAL}s）"

while true; do
  ISSUE_NUMBER="$(get_next_issue)"

  if [ -n "$ISSUE_NUMBER" ] && [ "$ISSUE_NUMBER" != "null" ]; then
    run_issue_review "$ISSUE_NUMBER"
  else
    log "対象 Issue なし — ${POLL_INTERVAL}s 待機"
  fi

  sleep "$POLL_INTERVAL"
done
