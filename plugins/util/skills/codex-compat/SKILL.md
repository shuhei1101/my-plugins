---
name: util:codex-compat
description: 指定プロジェクト配下を再帰的にスキャンし、CLAUDE.md と AGENTS.md を AGENTS.md に統合してシンボリックリンクを作成する。Claude Code と OpenAI Codex の両方で同一の指示ファイルを参照できるようにする。「Codex 対応して」「codex-compat を実行」「Claude と Codex を両対応にして」と言われたら起動。
---

# codex-compat

指定プロジェクト配下を再帰的にスキャンして `CLAUDE.md` と `AGENTS.md` を統合し、
`AGENTS.md` を正として `CLAUDE.md` → `AGENTS.md` のシンボリックリンクを作成する。

Claude Code と OpenAI Codex が同一の指示ファイルを参照できる状態にする。

---

## 前提知識: Claude Code vs Codex の仕様差異

| 要素 | Claude Code | OpenAI Codex | 共存方針 |
|---|---|---|---|
| 指示ファイル | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` を正とし `CLAUDE.md` はシンボリックリンク |
| フック設定 | `hooks/hooks.json`（`${CLAUDE_PLUGIN_ROOT}` 変数） | `.codex/hooks.json` or `~/.codex/hooks.json`（同形式） | ライフサイクルイベント名は共通。配置先が異なる |
| スキル | `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` | 完全共通（フロントマターも同一） |
| プラグインマニフェスト | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` | 両方を並置 |
| MCP | `.mcp.json` | `.mcp.json` | 同一形式 |
| rules 相当 | `rules/` + hooks injection | なし | Claude の自作フック injection で代替済み |
| マーケットプレイス | `.claude-plugin/marketplace.json` | 公式 Plugin Directory（近日公開） | 公開マーケットプレイス利用 |

---

## 実行手順

### ステップ 1: 対象プロジェクトルートを確認

スキル実行前に対象プロジェクトルートを確認する。
引数で指定された場合はそちらを、指定がない場合は現在の作業ディレクトリを対象とする。

```bash
TARGET_DIR="${1:-$(pwd)}"
echo "対象ディレクトリ: $TARGET_DIR"
```

### ステップ 2: CLAUDE.md と AGENTS.md の一覧取得

```bash
# CLAUDE.md の検索（.git、node_modules、.claude/worktrees を除外）
find "$TARGET_DIR" \
  -name "CLAUDE.md" \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/.claude/worktrees/*" \
  | sort

# AGENTS.md の検索（同除外）
find "$TARGET_DIR" \
  -name "AGENTS.md" \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/.claude/worktrees/*" \
  | sort
```

### ステップ 3: 各ディレクトリで統合処理

発見した各 `CLAUDE.md` ディレクトリに対して以下を実行する:

#### 3-a: AGENTS.md が存在しない場合（CLAUDE.md のみ）

```bash
DIR="$(dirname "$CLAUDE_MD_PATH")"

# CLAUDE.md の内容を AGENTS.md にコピー
cp "$DIR/CLAUDE.md" "$DIR/AGENTS.md"

# CLAUDE.md をシンボリックリンクに置き換え
rm "$DIR/CLAUDE.md"
ln -s "AGENTS.md" "$DIR/CLAUDE.md"

echo "✓ $DIR: CLAUDE.md → AGENTS.md に統合してシンボリックリンク作成"
```

#### 3-b: AGENTS.md が既に存在する場合（両方ある）

```bash
DIR="$(dirname "$CLAUDE_MD_PATH")"

# 内容が異なる場合は AGENTS.md に CLAUDE.md の内容を追記してマージ
# 内容が同一の場合は CLAUDE.md を削除してシンボリックリンク化
if diff -q "$DIR/CLAUDE.md" "$DIR/AGENTS.md" > /dev/null 2>&1; then
  # 内容が同一 → CLAUDE.md を削除してシンボリックリンク化
  rm "$DIR/CLAUDE.md"
  ln -s "AGENTS.md" "$DIR/CLAUDE.md"
  echo "✓ $DIR: 内容が同一 → CLAUDE.md をシンボリックリンクに変換"
else
  # 内容が異なる → AGENTS.md に CLAUDE.md 内容をマージ（冪等性: 既にマージ済みならスキップ）
  if grep -q "<!-- CLAUDE.md からのマージ内容 -->" "$DIR/AGENTS.md" 2>/dev/null; then
    # マーカーが既に存在する → マージ済みのためスキップ
    rm "$DIR/CLAUDE.md"
    ln -s "AGENTS.md" "$DIR/CLAUDE.md"
    echo "✓ $DIR: マージ済み（マーカー検出）→ CLAUDE.md をシンボリックリンクに変換"
  else
    echo "" >> "$DIR/AGENTS.md"
    echo "<!-- CLAUDE.md からのマージ内容 -->" >> "$DIR/AGENTS.md"
    cat "$DIR/CLAUDE.md" >> "$DIR/AGENTS.md"
    rm "$DIR/CLAUDE.md"
    ln -s "AGENTS.md" "$DIR/CLAUDE.md"
    echo "✓ $DIR: CLAUDE.md の内容を AGENTS.md にマージしてシンボリックリンク作成"
  fi
fi
```

#### 3-c: CLAUDE.md が既にシンボリックリンクの場合

```bash
if [ -L "$DIR/CLAUDE.md" ]; then
  echo "✓ $DIR: CLAUDE.md は既にシンボリックリンク → スキップ"
fi
```

### ステップ 4: シンボリックリンクの動作確認

```bash
# 作成したシンボリックリンクを確認
find "$TARGET_DIR" \
  -name "CLAUDE.md" \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/.claude/worktrees/*" \
  | while read -r f; do
    if [ -L "$f" ]; then
      target=$(readlink "$f")
      echo "✓ シンボリックリンク: $f -> $target"
    else
      echo "⚠ 通常ファイル（未変換）: $f"
    fi
  done
```

### ステップ 5: 設定ファイル系の対応案内

スクリプトによる自動移行が難しい設定ファイルについては、以下の指示に従って手動対応する:

#### hooks の Codex 対応

Claude Code の hooks は `plugins/<name>/hooks/hooks.json` で管理されているが、
Codex では `.codex/hooks.json` または `~/.codex/hooks.json` に配置が必要。

ライフサイクルイベント名（`SessionStart`、`PreToolUse`、`PostToolUse`、`Stop` など）は
Claude Code と Codex で共通のため、設定ファイルの中身は流用可能。

**対応方法**: 各プラグインの `hooks/hooks.json` の内容を `~/.codex/hooks.json` にコピーし、
`${CLAUDE_PLUGIN_ROOT}` 変数を実際のプラグインパスに書き換える。

#### MCP の Codex 対応

`.mcp.json` は Claude Code と Codex で同一形式のため、そのまま利用可能。

---

## 注意事項

- WSL2 環境ではシンボリックリンクが `ln -s` で作成可能（Windows 側からは見えない場合あり）
- `.gitignore` にシンボリックリンクが除外されていないことを確認すること
- Git はシンボリックリンクをトラッキングできる（`git config core.symlinks true` が必要な場合あり）
- Codex がシンボリックリンクを解釈できるかは実行環境依存。解釈できない場合は 3-a/3-b でコピー運用に切り替える
