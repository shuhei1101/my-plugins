<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 環境変数ガイド

プラグインの**実行されるコード**を環境変数で設定可能にする方法。対象は**フックとスクリプト**
（`hooks/*.py`, `scripts/*.py`, インライン `-c` フックコマンド） — プロセスとして実行され
`os.environ` を読めるのはこれらだけ。Markdown の指示ファイル（`CLAUDE.md`, rule, `SKILL.md`）は
コンテキストに読み込まれるだけで実行されないので env を読めない — プラグインのコードがどの env を
読むかを*記載する*だけ。
英語版: `references/environment.md`

---

## 設定する — `settings.json` の `env` ブロック

Claude Code は `settings.json` の `env` ブロックのキー/値を、すべてのフック・ツールのサブプロセス
環境にエクスポートする。3 つのスコープで有効で、後のスコープが先を上書きする:

| スコープ | ファイル | コミット対象? |
|---|---|---|
| ユーザー | `~/.claude/settings.json` | 個人用 |
| プロジェクト（チーム） | `.claude/settings.json` | ✅ git にコミット |
| プロジェクト（ローカル） | `.claude/settings.local.json` | ❌ gitignore |

```json
{
  "env": {
    "MY_KIT_INJECTION_TTL": "7200",
    "MY_KIT_INJECTION_LANG": "jp"
  }
}
```

---

## 読む — フック/スクリプト内の `os.environ`

適切なデフォルトを用意し検証する。未設定を前提にしない（`env` ブロックは任意）:

```python
import os

raw = os.environ.get("MY_KIT_INJECTION_TTL")        # 未設定なら None
ttl = int(raw) if raw and raw.isdigit() else 3600   # デフォルトにフォールバック

lang = os.environ.get("MY_KIT_INJECTION_LANG", "en").lower()
```

> `env` の値はただの文字列 — 読み取り側で parse/検証する（`int(...)`, `.lower()`, allow-list 等）。

---

## 実例（このリポジトリ）

`*-kit` のリファレンス注入フック（dev-kit / claude-kit の `hooks/scripts/inject_references.py`）は
この方式で調整できる:

| 環境変数 | 効果 | デフォルト |
|---|---|---|
| `{PREFIX}_INJECTION_TTL` | reference が再注入されるまでの秒数 | `3600` |
| `{PREFIX}_INJECTION_LANG` | `jp` → 日本語の description/テンプレを注入 | `en` |

`{PREFIX}` はプラグイン名を大文字化し非英数字を `_` にしたもの（例: `dev-kit` → `DEV_KIT`）。

---

## 慣習

- プラグイン名で**キーを名前空間化**する（`{PREFIX}_...`）。プラグイン同士の衝突を防ぐ。
- 読み取り側で**必ずデフォルトを用意**する — env ブロックは任意。未設定でもコードは動くこと。
- **プラグインが読む env 変数は、そのプラグイン自身の `CLAUDE.md` に記載する**（名前・効果・デフォルト）。
  ソースを読まずとも何が設定可能か分かるように。
- 秘密情報をコミット対象の `.claude/settings.json` に置かない。マシン固有・機微な値は
  `settings.local.json`（gitignore）に置く。
- Markdown（`CLAUDE.md` / rule / `SKILL.md`）は env を読めない — env で挙動を変えたいなら、その変化は
  フックかスクリプトに置き、Markdown はそれを記載するだけにする。

---

## パス変数と env 変数

別々の仕組み。混同しない:

| | どこで設定 | どこで読む |
|---|---|---|
| **env 変数**（`MY_KIT_*`） | `settings.json` の `env` ブロック | フック/スクリプト内の `os.environ` |
| **パス変数**（`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PROJECT_DIR}`） | `hooks.json` / `settings.json` のコマンド引数で Claude Code が展開 | 注入プロンプト本文では展開されない — `hooks.md` 参照 |
