"""セッション状態の永続化。"""
from __future__ import annotations

import json
from pathlib import Path

from inject_rules.features.session.types import SessionState
from inject_rules.shared.logger import emit_log
from inject_rules.shared.settings import Settings


def load_state(session_id: str, *, base_dir: Path) -> SessionState:
    """セッション ID に対応するファイルからセッション状態を復元する。"""
    path = base_dir / f"{session_id}.json"
    if not path.exists():
        return SessionState()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        # 壊れた記録は捨てて作り直す（再注入が 1 度余分に走るだけで済む）
        emit_log(
            "WARNING",
            "セッション状態を復元できませんでした",
            {"session_id": session_id, "error": str(error)},
            endpoint=Settings.from_env().otlp_endpoint,
        )
        return SessionState()

    injected = data.get("injected") if isinstance(data, dict) else None
    offsets = data.get("offsets") if isinstance(data, dict) else None
    notified = data.get("notified") if isinstance(data, dict) else None
    return SessionState(
        injected=set(injected) if isinstance(injected, list) else set(),
        offsets=dict(offsets) if isinstance(offsets, dict) else {},
        notified=set(notified) if isinstance(notified, list) else set(),
    )


def save_state(session_id: str, state: SessionState, *, base_dir: Path) -> None:
    """セッション状態をファイルへ書き出す。"""
    payload = {
        "injected": sorted(state.injected),
        "offsets": state.offsets,
        "notified": sorted(state.notified),
    }
    try:
        base_dir.mkdir(parents=True, exist_ok=True)
        (base_dir / f"{session_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
    except OSError as error:
        # 保存できなくても次回の注入で再送出になるだけなので処理を止めない
        emit_log(
            "WARNING",
            "セッション状態を保存できませんでした",
            {"session_id": session_id, "error": str(error)},
            endpoint=Settings.from_env().otlp_endpoint,
        )


def clear_state(session_id: str, *, base_dir: Path) -> None:
    """セッションの保存ファイルを削除する。"""
    (base_dir / f"{session_id}.json").unlink(missing_ok=True)
