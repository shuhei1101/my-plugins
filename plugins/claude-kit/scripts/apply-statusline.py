"""~/.claude/settings.json に定義済みの statusLine 設定を適用する。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

STATUS_LINE = {
    "type": "command",
    "command": (
        'python -c "'
        'import sys,json,os,datetime;'
        'd=json.load(sys.stdin);'
        "m=(d.get('model') or {}).get('display_name','?').split(' (')[0];"
        'ml=m.lower();'
        "m_color='\\033[31m' if 'opus' in ml else ('\\033[33m' if 'sonnet' in ml else '');"
        "m_reset='\\033[0m' if m_color else '';"
        'mr_str=m_color+m+m_reset;'
        "proj=(d.get('workspace') or {}).get('project_dir','') or '';"
        "ws=(os.path.basename(proj) or '?')+'/';cw=d.get('context_window') or {};"
        "rl=d.get('rate_limits') or {};r5=rl.get('five_hour') or {};r7=rl.get('seven_day') or {};"
        "tt=lambda e,f: datetime.datetime.fromtimestamp(e).strftime(f) if e else '';"
        "fmtn=lambda n: '?' if n is None else (str(round(n/1000000,1)).rstrip('0').rstrip('.')+'M' if n>=1000000 else str(round(n/1000))+'k' if n>=1000 else str(round(n)));"
        "up=cw.get('used_percentage');cu=cw.get('total_input_tokens');cm=cw.get('context_window_size');"
        "ctx_color='\\033[31m' if up is not None and up>=70 else ('\\033[33m' if up is not None and up>=50 else ('\\033[32m' if up is not None else ''));"
        "ctx_reset='\\033[0m' if ctx_color else '';"
        "ctx_str=ctx_color+'ctx '+str(round(up))+'%'+ctx_reset+((' ('+fmtn(cu)+'/'+fmtn(cm)+')') if cu is not None or cm is not None else '') if up is not None else '';"
        "p5=r5.get('used_percentage');p7=r7.get('used_percentage');"
        "p5_color='\\033[31m' if p5 is not None and p5>=70 else ('\\033[33m' if p5 is not None and p5>=50 else '');"
        "p5_reset='\\033[0m' if p5_color else '';"
        "p7_color='\\033[31m' if p7 is not None and p7>=70 else ('\\033[33m' if p7 is not None and p7>=50 else '');"
        "p7_reset='\\033[0m' if p7_color else '';"
        'parts2=[];'
        "p5 is not None and parts2.append(p5_color+'5h '+str(round(p5))+'%'+p5_reset+(' (~'+tt(r5.get('resets_at'),'%H:%M')+')' if r5.get('resets_at') else ''));"
        "p7 is not None and parts2.append(p7_color+'7d '+str(round(p7))+'%'+p7_reset+(' (~'+tt(r7.get('resets_at'),'%m/%d')+')' if r7.get('resets_at') else ''));"
        "print(ws+' | '+mr_str+(' | '+ctx_str if ctx_str else ''));print(' | '.join(parts2))"
        '"'
    ),
    "padding": 1,
}


def main() -> int:
    if not SETTINGS_PATH.exists():
        print(f"エラー: {SETTINGS_PATH} が見つかりません。", file=sys.stderr)
        return 1

    with open(SETTINGS_PATH, encoding="utf-8") as f:
        settings = json.load(f)

    settings["statusLine"] = STATUS_LINE

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"statusLine を {SETTINGS_PATH} に適用しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
