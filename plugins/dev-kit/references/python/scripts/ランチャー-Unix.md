# launchers-unix — sh launcher

Conventions for `.sh` files that launch Python scripts on UNIX-like systems (Linux / macOS / WSL).

---

## Standard template

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

## Required elements

| Element | Reason |
|---|---|
| `#!/usr/bin/env bash` | Make bash explicit (avoid environments where the sh symlink is dash) |
| `set -euo pipefail` | Stop immediately on error, detect undefined variables, catch mid-pipe failures |
| `cd "$(dirname "$0")"` | Use the script's location as the base |
| `.venv/bin/activate` (with existence check) | Auto-activate venv |
| `mkdir -p log` | Ensure log directory |
| `date +%Y%m%d-%H%M%S` | Locale-independent timestamp |
| `tee "$LOG"` | Output stdout/stderr to screen and file simultaneously |
| `${PIPESTATUS[0]}` | Get the exit code of the pipe's first stage (python) |
| `exit "$EXIT_CODE"` | Propagate the exit code to the caller |

---

## Meaning of `set -euo pipefail`

- `-e`: terminate immediately if a command fails (non-zero exit code)
- `-u`: error on reference to an undefined variable
- `-o pipefail`: set the whole pipeline's exit code to "the rightmost non-zero"

```bash
# pipefail なし: python が失敗しても tee 成功で全体は 0 になってしまう
python script.py | tee log.txt   # ← exit 0 になる

# pipefail あり: python の失敗が拾える
set -o pipefail
python script.py | tee log.txt   # ← python の exit が返る
```

---

## Argument forwarding

Pass arguments to Python with quoting via `"$@"`:

```bash
python script.py "$@"
```

Use `"$@"` rather than `$*` (avoids accidents with whitespace-containing arguments).

---

## Choosing among multiple binaries

Pattern using `uv run` (recommended for dev-kit Python projects: use `uv`):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# uv ベース（推奨）
uv run python script.py "$@"
```

Or explicitly specify the version:

```bash
python3.12 script.py "$@"
```

---

## Sample: run-server.sh for launching FastAPI

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

`HOST` / `PORT` can be overridden via environment variables.

---

## Output messages

Like bat, default to **English** (easier to grep / share):

```bash
echo "(log: $LOG)"         # ✅
echo "（ログ：$LOG）"        # ⚠️ UTF-8 環境なら可
```

That said, UNIX environments are UTF-8 by default, so including Japanese is usually fine.
Align with the project's policy.

---

## Execute permission

Don't forget `chmod +x run.sh` (when committing to git, save the attribute with `git update-index --chmod=+x run.sh`).

---

## Things you must not do

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

## Related files

- `scripts/launchers-windows.md` — Windows counterpart
- `scripts/Pythonスクリプト.md` — the Python script that gets called
- `core/言語ルール.md` — shell script output should preferably be English
