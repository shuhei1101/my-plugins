from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

# monitor/ の親が gh-kit プラグインルート
GH_KIT_PLUGIN_DIR = str(Path(__file__).resolve().parent.parent)


def _load_env_file(path: Path) -> None:
    """gh_monitor.env が存在すれば os.environ に読み込む（外部 export 済みを優先）。"""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip()


def _load_constants_sh(target: dict[str, object]) -> None:
    """hooks/session-start/constants.sh の export 行を target 名前空間に注入する。

    target には通常 globals() を渡し、constants.sh の定数名（GH_KIT_LABEL_*）
    がそのままモジュールトップレベル変数として参照可能になる。
    定数の再定義（Python 側で名前を付け直す）を不要にし、constants.sh を SoT に統一する。
    既に os.environ に値があれば（外部 export 済み）そちらを優先。
    """
    constants_path = Path(GH_KIT_PLUGIN_DIR) / "hooks" / "session-start" / "constants.sh"
    if not constants_path.is_file():
        # フォールバックは設けない: 必須ファイルが無ければ起動を中止
        raise FileNotFoundError(f"constants.sh が見つかりません: {constants_path}")
    for raw in constants_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        # export VAR=VALUE 形式のみ取り込む（コメント・空行・shebang・その他は無視）
        if not line.startswith("export "):
            continue
        body = line[len("export "):]
        if "=" not in body:
            continue
        key, value = body.split("=", 1)
        # 外部 env を優先し、無ければ constants.sh の値を採用
        target[key] = os.environ.get(key, value)


def log(msg: str) -> None:
    """タイムスタンプ付きで stderr にログ 1 行を出力する。"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def die(msg: str) -> None:
    """エラーログを出力して exit code 1 で終了する。"""
    log(f"ERROR: {msg}")
    sys.exit(1)
