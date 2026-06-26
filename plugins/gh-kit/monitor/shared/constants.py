"""計算済みの不変値（パス・業務固定値）。実行時可変な値は settings.py へ。"""

from __future__ import annotations

from pathlib import Path

# gh-kit プラグインルート（このファイルから 2 階層上が monitor/、その親が gh-kit/）
PLUGIN_ROOT: Path = Path(__file__).resolve().parents[2]

# ラベル名など定数群の SoT。SessionStart フックでも、Python 側からもこのパスを読む。
CONSTANTS_SH_PATH: Path = PLUGIN_ROOT / "scripts" / "constants.sh"
