# AGENTS.md — my-plugins 開発者ガイド

> このファイルは AGENTS.md を正として管理されます。
> CLAUDE.md は AGENTS.md へのシンボリックリンクです（WSL2 前提。`core.symlinks=true` で動作）。
> Claude Code も OpenAI Codex も同一の指示ファイル（AGENTS.md）を参照します。

---

このリポジトリは Claude Code のプラグインマーケットプレイスです。スキルをプラグインとして配布・管理し、`/plugin` コマンドでインストールできます。

---

## OpenAI Codex 対応

このリポジトリは Claude Code と OpenAI Codex の両方で利用可能です。

### 仕様差異マトリクス

| 要素 | Claude Code | OpenAI Codex | 共存方針 |
|---|---|---|---|
| 指示ファイル | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` を正とし `CLAUDE.md` はシンボリックリンク（WSL2 前提。`core.symlinks=true` で動作） |
| フック設定 | `hooks/hooks.json`（プラグイン内） | `.codex/hooks.json` or `~/.codex/hooks.json` | ライフサイクルイベント名は共通。設定配置先が異なる |
| スキル | `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` | 完全共通（フロントマターも同一） |
| プラグインマニフェスト | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` | 両方を並置 |
| MCP | `.mcp.json` | `.mcp.json` | 同一形式 |
| rules 相当 | `rules/` + hooks injection | なし | Claude の自作フック injection で代替済み |
| マーケットプレイス | `.claude-plugin/marketplace.json` | `.codex-plugin/marketplace.json` | 両方を並置 |

### hooks の Codex 対応手順

各プラグインの `hooks/hooks.json` は Claude Code 向けに管理されています。
Codex で同等のフックを利用するには以下の手順で配置してください。

#### 1. 設定ファイルの配置先

```
~/.codex/hooks.json        # ユーザーグローバル設定
<repo>/.codex/hooks.json   # プロジェクト設定
```

#### 2. ライフサイクルイベント名（Claude Code / Codex 共通）

以下のイベント名は両ツールで完全に共通です:

- `SessionStart` — セッション開始時
- `PreToolUse` — ツール実行前
- `PostToolUse` — ツール実行後
- `UserPromptSubmit` — プロンプト送信時
- `Stop` — セッション終了時
- `PreCompact` / `PostCompact` — 会話圧縮時
- `SubagentStart` / `SubagentStop` — サブエージェント実行時

#### 3. 移行手順

```bash
# 1. .codex ディレクトリ作成
mkdir -p ~/.codex

# 2. 各プラグインの hooks.json を統合コピー
# ※ ${CLAUDE_PLUGIN_ROOT} を実際のプラグインインストールパスに書き換えること
# 例: ~/.claude/plugins/cache/mentaiko-claude-plugins/guard-kit/1.0
PLUGIN_ROOT="$HOME/.claude/plugins/cache/mentaiko-claude-plugins"

# 複数プラグインの hooks.json を jq で統合する場合:
# 例: guard-kit と gh-kit の hooks を ~/.codex/hooks.json にマージ
jq -s '.[0].hooks + .[1].hooks | {hooks: .}' \
  "$PLUGIN_ROOT/guard-kit/1.0/hooks/hooks.json" \
  "$PLUGIN_ROOT/gh-kit/0.45/hooks/hooks.json" \
  > ~/.codex/hooks.json

# プラグインが 1 つだけの場合はそのままコピーでも可:
# cp "$PLUGIN_ROOT/guard-kit/1.0/hooks/hooks.json" ~/.codex/hooks.json
```

#### 4. `${CLAUDE_PLUGIN_ROOT}` 変数の置き換え

Codex は `${CLAUDE_PLUGIN_ROOT}` 環境変数を自動設定しません。
インストール済みプラグインの実パスに手動で書き換えるか、
`CLAUDE_PLUGIN_ROOT` を Codex の環境設定で定義してください。

### rules injection の Codex 対応

Codex には Claude Code の `rules/` 機能に相当する仕組みはありませんが、
このリポジトリでは **自作 hooks（`PreToolUse`）による rules injection** を実装済みです。
hooks が正しく配置されていれば Codex でも同等の rules injection が動作します。

### Codex 両対応移行スキル

プロジェクト配下の `CLAUDE.md` を `AGENTS.md` + シンボリックリンクに変換するスキルがあります:

```
/util:codex-compat
```

詳細は `plugins/util/skills/codex-compat/SKILL.md` を参照してください。

---

## 優先度:急ぎ ラベルの仕様

`優先度:急ぎ`（`GH_KIT_LABEL_PRIORITY_URGENT`）ラベルは **処理順序を先頭に並べる目的のみ** に使用されます。

### 効果

- 各 auto スキル（`issue-review-auto`・`pr-implement-auto`・`pr-review-auto`・`pr-merger-auto`）のキュー形成時、`優先度:急ぎ` が付いた Issue/PR を先頭にソートする。
- 他の全ての処理はラベルなし Items と同一の手順で実行される。

### 効果がないこと（仕様上の禁止事項）

| 誤解されやすい動作 | 実際の挙動 |
|---|---|
| ユーザー確認をスキップする | しない。assignees の有無と verdict で独立して制御される |
| 自動マージを許可する | しない。assignees が設定されている PR は AI が単独マージしない（pr-review スキル 制約 No.3） |
| レビューを省略する | しない。通常と同じレビュー・マージフローを通る |

### 実装の根拠

各 auto スキルの jq ソートは以下の形式であり、優先度ラベルに基づく **条件分岐（スキップ・自動マージ）は一切存在しない**:

```bash
# 優先度ラベルは処理順序のみを制御する。ユーザー確認スキップ・自動マージのトリガーにはならない。
jq 'sort_by(if 優先度:急ぎ then 0 elif 優先度:いつでも then 1 else 2 end, .number)'
```
