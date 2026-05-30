<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# launchers-unix — sh ランチャー

> このファイルは `launchers-unix.md` の日本語ミラーです。

UNIX 系（Linux / macOS / WSL）で Python スクリプトを起動する `.sh` ファイルの規約。

---

## 標準テンプレート

```bash
#!/usr/bin/env bash
set -euo pipefail

# このスクリプトの場所を基準にする
cd "$(dirname "$0")"

# venv 有効化（存在すれば）
if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

# ログ設定
mkdir -p log
TS=$(date +%Y%m%d-%H%M%S)
LOG="log/script-${TS}.log"

# 実行（tee で stdout/stderr を画面にもファイルにも）
python script.py "$@" 2>&1 | tee "$LOG"
EXIT_CODE=${PIPESTATUS[0]}

echo
echo "(log: $LOG)"
echo "(exit: $EXIT_CODE)"
exit "$EXIT_CODE"
```

---

## 必須要素

| 要素 | 理由 |
|---|---|
| `#!/usr/bin/env bash` | bash を明示（sh シンボリックリンクが dash の環境を避ける） |
| `set -euo pipefail` | エラーで即停止、未定義変数を検出、pipe の途中失敗も拾う |
| `cd "$(dirname "$0")"` | スクリプトの置かれた場所を基準にする |
| `.venv/bin/activate`（存在チェック付き） | venv 自動有効化 |
| `mkdir -p log` | ログディレクトリ確保 |
| `date +%Y%m%d-%H%M%S` | locale 非依存のタイムスタンプ |
| `tee "$LOG"` | stdout/stderr を画面とファイルへ同時出力 |
| `${PIPESTATUS[0]}` | pipe 先頭（python）の終了コードを取得 |
| `exit "$EXIT_CODE"` | 呼び出し元に終了コードを伝える |

---

## `set -euo pipefail` の意味

- `-e`: コマンドが失敗（exit code 0 以外）したら即終了
- `-u`: 未定義変数を参照したらエラー
- `-o pipefail`: pipe 全体の終了コードを「最も右の非ゼロ」にする

```bash
# pipefail なし: python が失敗しても tee 成功で全体は 0 になってしまう
python script.py | tee log.txt   # ← exit 0 になる

# pipefail あり: python の失敗が拾える
set -o pipefail
python script.py | tee log.txt   # ← python の exit が返る
```

---

## 引数転送

`"$@"` で引数をクォート付きで Python へ渡す:

```bash
python script.py "$@"
```

`$*` ではなく `"$@"` を使う（空白を含む引数で事故らない）。

---

## 複数バイナリの選択

`uv run` を使うパターン（dev-kit Python プロジェクトの場合 `uv` 推奨）:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# uv ベース（推奨）
uv run python script.py "$@"
```

または明示的にバージョン指定:

```bash
python3.12 script.py "$@"
```

---

## サンプル: FastAPI 起動用 run-server.sh

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

mkdir -p log
TS=$(date +%Y%m%d-%H%M%S)
LOG="log/server-${TS}.log"

echo "Starting FastAPI on http://${HOST}:${PORT} (log: ${LOG})"
uvicorn mypkg.server.app:build_fastapi --factory --host "$HOST" --port "$PORT" 2>&1 | tee "$LOG"
```

`HOST` / `PORT` は環境変数で上書き可能。

---

## 出力メッセージ

bat と同様、**英語** を基本にする（grep / 共有しやすい）:

```bash
echo "(log: $LOG)"         # ✅
echo "（ログ：$LOG）"        # ⚠️ UTF-8 環境なら可
```

ただし UNIX 環境は UTF-8 が標準なので、日本語を入れても通常は問題ない。
プロジェクト方針で揃える。

---

## 実行権限

`chmod +x run.sh` を忘れずに（git 管理時は `git update-index --chmod=+x run.sh` で属性を保存）。

---

## やってはいけないこと

```bash
# ❌ set -e なし → エラーが伝播せず、後続が動いてしまう
#!/usr/bin/env bash
mkdir log
python script.py   # ← 失敗してもスクリプトは継続

# ❌ "$@" でなく $@ → 空白入り引数が壊れる
python script.py $@

# ❌ pipefail なしで tee → 終了コードを失う
python script.py | tee log.txt
```

---

## 関連ファイル

- `scripts/launchers-windows.md` — Windows 側の対応版
- `scripts/python-script.md` — 呼ばれる側の Python スクリプト
- `core/language-rules.md` — シェルスクリプトの出力は英語推奨
