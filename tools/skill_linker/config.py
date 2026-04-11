"""Skill Linker 設定 — デフォルト値を定義し、.env で上書きする。"""

import shutil
from pathlib import Path

_PKG_DIR = Path(__file__).parent
_ENV_FILE = _PKG_DIR / ".env"
_ENV_SAMPLE = _PKG_DIR / ".env.sample"

# ── デフォルト値 ────────────────────────────────────────────
# セミコロン区切りで複数ディレクトリ指定可能
SOURCE_DIRS: list[str] = []
DEST_DIRS: list[str] = []


# ── .env 読み込み ───────────────────────────────────────────
def _ensure_env():
    """初回起動時に .env がなければ .env.sample からコピーして作成する。"""
    if not _ENV_FILE.exists() and _ENV_SAMPLE.exists():
        shutil.copy(_ENV_SAMPLE, _ENV_FILE)


def _load_env():
    """.env を読み込んでモジュール変数を上書きする。"""
    global SOURCE_DIRS, DEST_DIRS
    _ensure_env()
    if not _ENV_FILE.exists():
        return
    for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key == "SOURCE_DIRS" and value:
            SOURCE_DIRS = [d.strip() for d in value.split(";") if d.strip()]
        elif key == "DEST_DIRS" and value:
            DEST_DIRS = [d.strip() for d in value.split(";") if d.strip()]


def save_env(**kwargs: str):
    """.env ファイルのキーを更新する。存在しないキーは追加する。"""
    lines: list[str] = []
    existing_keys: set[str] = set()

    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key = stripped.partition("=")[0].strip()
                if key in kwargs:
                    lines.append(f'{key}={kwargs[key]}')
                    existing_keys.add(key)
                    continue
            lines.append(line)

    for key, value in kwargs.items():
        if key not in existing_keys:
            lines.append(f"{key}={value}")

    _ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


_load_env()
