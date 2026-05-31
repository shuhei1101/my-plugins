# env-syncスキル — WSL ↔ Windows 間の Claude Code 設定同期

## 概要

`claude-kit` の単一スキル `env-sync` が、WSL と Windows の `~/.claude/` 配下の設定ファイルを双方向に同期する。両環境の差分を検出し、ユーザー確認のうえで選択ファイルをコピーする。

## スキルの役割

- スキルは 1 つ（`env-sync`）で双方向をカバーする。
- 実行環境が WSL なら Windows 側（`/mnt/c/Users/<user>/.claude/`）との差分を、Windows なら WSL 側（`\\wsl$\<distro>\home\<user>\.claude\`）との差分を検出・提案する。

## 環境判定・対向パス検出

- 環境判定: `/proc/version` に `microsoft` が含まれれば WSL、なければ Windows。
- 対向パス（WSL→Windows）: `cmd.exe /c "echo %USERNAME%"` で Windows ユーザー名を取得し `/mnt/c/Users/${WIN_USER}/.claude` を組み立てる。

## 同期対象

`~/.claude/` 配下をスキャンし、以下を対象候補として表示する。

| ファイル / ディレクトリ | 説明 |
|---|---|
| `settings.json` | フック・権限・ステータスライン設定 |
| `CLAUDE.md` | グローバル AI 指示 |
| `CLAUDE.jp.md` | 日本語ミラー |
| `skills/` | ユーザースキル |
| `keybindings.json` | キーバインド設定 |
| `rules/` | パススコープルール |

- プラグインキャッシュ（`plugins/cache/`）は対象外。

## フロー

1. 実行環境（WSL / Windows）を自動判定
2. 対向側のパスを自動検出
3. 両環境の `~/.claude/` をスキャン
4. ファイルごとに差分を検出（存在の有無 + 更新日時）
5. AI がコピー推奨ファイルを理由付きで提案
6. ユーザーが確認・選択
7. 選択されたファイルをコピー
8. 結果をレポート

## トリガー文言

- `WSL と Windows の設定を同期して`
- `env-sync して`
- `Claude Code の設定をコピーしたい`
- `/claude-kit:env-sync`

## 参考ドキュメント

- `plugins/claude-kit/skills/env-sync/SKILL.md`: スキル本体

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成（specsから統合） | 260531_notes-spec-and-ref-inject |
