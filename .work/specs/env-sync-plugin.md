---
created_at: 2026-05-19
updates:
  - 2026-05-19 — 初版作成
related_specs: []
related_prs:
  - PR56
---

# env-sync — WSL ↔ Windows 間 Claude Code 設定同期スキル

## 概要

WSL 環境と Windows 環境でそれぞれ Claude Code を使う場合、
`~/.claude/` 配下の設定ファイルが分離してしまう。
このスキルは両環境の差分を検出し、ユーザーの確認のもとでファイルをコピーする。

## 配置先

`claude-kit` プラグインの新スキルとして追加する。

- `plugins/claude-kit/skills/env-sync/SKILL.md`

## スキルの役割分担

スキルは 1 つ（`env-sync`）で双方向をカバーする。

| 実行環境 | 動作 |
|---|---|
| WSL | Windows 側 (`/mnt/c/Users/<user>/.claude/`) との差分を検出・提案 |
| Windows (Git Bash 等) | WSL 側 (`\\wsl$\<distro>\home\<user>\.claude\`) との差分を検出・提案 |

## 同期対象ファイル

スキル実行時に `~/.claude/` 配下をスキャンし、以下を対象候補として表示する：

| ファイル / ディレクトリ | 説明 |
|---|---|
| `settings.json` | フック・権限・ステータスライン設定 |
| `CLAUDE.md` | グローバル AI 指示 |
| `CLAUDE.jp.md` | 日本語ミラー |
| `skills/` | ユーザースキル |
| `keybindings.json` | キーバインド設定 |
| `rules/` | パススコープルール |

プラグインキャッシュ（`plugins/cache/`）はコピー対象外とする。

## パス自動検出

### WSL から Windows を参照

```bash
WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r\n')
WIN_CLAUDE="/mnt/c/Users/${WIN_USER}/.claude"
```

### 現在の環境判定

```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  ENV=wsl
else
  ENV=windows
fi
```

## スキルの流れ

1. 実行環境（WSL / Windows）を自動判定
2. 対向側のパスを自動検出
3. 両環境の `~/.claude/` をスキャン
4. ファイルごとに差分を検出（存在の有無 + 更新日時）
5. AI がコピー推奨ファイルを提案（理由付き）
6. ユーザーが確認・選択
7. 選択されたファイルをコピー
8. 結果をレポート

## トリガー文言

- `WSL と Windows の設定を同期して`
- `env-sync して`
- `Claude Code の設定をコピーしたい`
- `/claude-kit:env-sync`
