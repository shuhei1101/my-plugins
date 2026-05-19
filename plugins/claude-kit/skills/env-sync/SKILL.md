---
name: env-sync
description: |
  Sync Claude Code configuration files between WSL and Windows environments.
  Scans both sides, shows a diff, and copies selected files after user confirmation.
  Trigger when the user says "WSL と Windows の設定を同期して", "env-sync して",
  "Claude Code の設定をコピーしたい", "設定ファイルを移行したい",
  or invoked explicitly as `/claude-kit:env-sync`.
---

# env-sync — WSL ↔ Windows Claude Code 設定同期

WSL と Windows の `~/.claude/` を比較し、差分を AI が分析してコピー対象を提案する。

---

## Overview

| 実行環境 | 対向パス |
|---|---|
| WSL | `/mnt/c/Users/<WindowsUser>/.claude/` |
| Windows (Git Bash 等) | `\\wsl$\<distro>\home\<user>\.claude\` |

同期対象候補:

| ファイル / フォルダ | 内容 |
|---|---|
| `settings.json` | フック・権限・ステータスライン設定 |
| `CLAUDE.md` / `CLAUDE.jp.md` | グローバル AI 指示 |
| `skills/` | ユーザースキル |
| `keybindings.json` | キーバインド |
| `rules/` | パススコープルール |

プラグインキャッシュ（`plugins/cache/`）はコピー対象外。

---

## Tasks

### Step 1: 実行環境を判定する

#### Condition

- Always — run first

#### Process

Run the following and note the result:

```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  echo "WSL"
else
  echo "Windows"
fi
```

→ Proceed to Step 2

#### Output

- 実行環境（WSL / Windows）が確定している

---

### Step 2: 対向パスを自動検出する

#### Condition

- Step 1 complete

#### Process

**WSL の場合:**

```bash
WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r\n')
WIN_CLAUDE="/mnt/c/Users/${WIN_USER}/.claude"
echo "Windows side: ${WIN_CLAUDE}"
ls "${WIN_CLAUDE}" 2>/dev/null || echo "NOT FOUND"
```

**Windows (Git Bash 等) の場合:**

```bash
DISTRO=$(wsl.exe -l --quiet 2>/dev/null | head -1 | tr -d '\r\n')
WSL_USER=$(wsl.exe -- whoami 2>/dev/null | tr -d '\r\n')
WSL_CLAUDE="//wsl$/${DISTRO}/home/${WSL_USER}/.claude"
echo "WSL side: ${WSL_CLAUDE}"
ls "${WSL_CLAUDE}" 2>/dev/null || echo "NOT FOUND"
```

→ Proceed to Step 3

#### Output

- 対向パスが確定している

#### Notes

##### Branching

- 対向パスが見つからない → ユーザーにパスを手動入力してもらい、確認後 Step 3 へ

---

### Step 3: 両環境のファイルをスキャンして差分を検出する

#### Condition

- Step 2 complete

#### Process

1. ローカルの `~/.claude/` を以下で列挙する（プラグインキャッシュを除く）:

```bash
find ~/.claude -maxdepth 3 \
  -not -path "*/plugins/cache/*" \
  -not -path "*/.git/*" \
  | sort
```

2. 対向側も同様に列挙する（`ls -la` または同等のコマンド）

3. 差分を以下の観点で整理する:
   - **ローカルのみ存在** するファイル
   - **対向のみ存在** するファイル
   - **両方存在するが更新日時が異なる** ファイル（どちらが新しいか）
   - **両方存在して同一** とみられるファイル（スキップ候補）

→ Proceed to Step 4

#### Output

- ファイルごとの差分状況が把握されている

---

### Step 4: AI がコピー推奨内容を提案する

#### Condition

- Step 3 complete

#### Process

スキャン結果を踏まえて、以下の形式でユーザーに提案する:

```
## 同期提案

### コピー推奨（ローカル → 対向）
- settings.json — ローカルが3日新しい（フックや権限設定が含まれる可能性）
- skills/my-skill/ — 対向に存在しない

### コピー推奨（対向 → ローカル）
- CLAUDE.md — 対向が1週間新しい

### 確認が必要
- keybindings.json — 両方に存在、日時が近い（内容確認を推奨）

### スキップ推奨
- plugins/cache/ — プラグインキャッシュのため除外
```

提案理由を添えて、ユーザーに確認を求める。

→ Proceed to Step 5

#### Output

- 提案内容をユーザーが確認している

---

### Step 5: ユーザーの確認を得てコピーを実行する

#### Condition

- Step 4 complete
- ユーザーが実行を承認している

#### Process

1. ユーザーが選択したファイル/フォルダをコピーする

```bash
# 例: ローカル → 対向
cp -r ~/.claude/settings.json "${WIN_CLAUDE}/settings.json"

# フォルダの場合
cp -rp ~/.claude/skills/ "${WIN_CLAUDE}/skills/"
```

2. コピー後に対向側のファイル一覧を確認する

→ Proceed to Step 6

#### Output

- 選択されたファイルがコピーされている

#### Notes

##### Prohibitions

- ユーザーの確認なしにコピーを実行しない
- 対向のファイルを確認なしに上書きしない（特に両方に存在する場合）

---

### Step 6: 結果をレポートする

#### Condition

- Step 5 complete

#### Process

コピー結果をファイルごとに報告する:

```
## env-sync 完了

### コピー済み
- settings.json → /mnt/c/Users/xxx/.claude/settings.json ✓
- skills/my-skill/ → /mnt/c/Users/xxx/.claude/skills/my-skill/ ✓

### スキップ
- CLAUDE.md — ユーザーがスキップを選択

Claude Code を再起動すると設定が反映されます。
```

#### Output

- 同期結果をユーザーが把握している
