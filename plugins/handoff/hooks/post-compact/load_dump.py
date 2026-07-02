"""PostCompact フック: dump スキルが残した前セッションのハンドオフ Markdown を読み込み、additionalContext に注入する。

Usage:
    # Claude Code が stdin に PostCompact ペイロード（session_id を含む JSON）を渡す
    python load_dump.py
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import traceback

# additionalContext は 10000 文字上限。案内文の分を差し引いた本文の実効上限
INLINE_INJECT_LIMIT = 9500


def _resolve_handoff_file(session_id: str) -> pathlib.Path:
    """session_id から読み込むべきハンドオフファイルのパスを組み立てる。

    HANDOFF_DIR は constants.sh が SessionStart で必ず export する前提。
    フォールバックは意図的に持たない: 未設定は「セットアップが壊れている」ため
    KeyError で明確に落として設定漏れを露見させる。
    """
    return pathlib.Path(os.environ["HANDOFF_DIR"]) / f"{session_id}.md"


def _build_inline_context(content: str, handoff_file: pathlib.Path) -> str:
    """本文を直接埋め込む案内文を組み立てる。

    引き継ぎ本文が上限内に収まる場合に使う。エージェントが本文だけ見て
    続きから作業できるようにするが、ファイルパスも合わせて伝えておく
    （細部を確認したくなったときに手元のファイルを開ける導線を残す）。
    """
    return (
        "# 前セッションからの引き継ぎ\n\n"
        "以下はコンパクト前セッションの状態要約。\n"
        f"原本ファイル: `{handoff_file}`\n\n"
        "参照して続きから作業を再開すること。\n\n"
        f"{content}"
    )


def _build_pointer_context(handoff_file: pathlib.Path) -> str:
    """ファイルパスだけ渡してエージェントに強制的に読ませる案内文を組み立てる。

    引き継ぎ本文が additionalContext 上限を超えるサイズの場合に使う。
    本文の抜粋を送るのではなく Read を強制することで、切り詰めによる情報欠落を避ける。
    """
    return (
        "# 前セッションからの引き継ぎ\n\n"
        f"前セッションの引き継ぎが `{handoff_file}` に残されている。\n"
        "続きの作業に取りかかる前に、必ず Read ツールで上記ファイルを全文読むこと。\n"
        "読まずに作業を始めることは禁止（前セッションのコンテキストを失った状態になる）。"
    )


def _inject_handoff(handoff_file: pathlib.Path) -> None:
    """ハンドオフ Markdown を additionalContext として stdout に出力する。

    Claude Code は stdout の JSON を解釈し、`hookSpecificOutput.additionalContext` の
    文字列を新セッションのシステムメッセージ末尾に差し込む。
    本文サイズで注入方式を切り替える:
      - 上限以下: 本文を直接埋め込む
      - 上限超え: ファイルパスだけ渡して Read を強制させる
    """
    content = handoff_file.read_text(encoding="utf-8")

    # サイズによって「本文埋め込み」か「パス提示のみ」かを切り替える
    if len(content) <= INLINE_INJECT_LIMIT:
        # 上限内: 本文をそのまま注入する
        injected = _build_inline_context(content, handoff_file)
    else:
        # 上限超え: 抜粋を送らずパスだけ提示し、Read で必ず全文読ませる
        injected = _build_pointer_context(handoff_file)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostCompact",
            "additionalContext": injected,
        }
    }
    print(json.dumps(output, ensure_ascii=False))


def main() -> int:
    # stdin から PostCompact ペイロードを受け取る
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # 想定外の入力: PostCompact はブロッキング能力がないため、無害に終了して次に譲る
        return 0

    # session_id が無ければ何もできないので終了
    session_id = payload.get("session_id", "")
    if not session_id:
        return 0

    # このセッション用に残されたハンドオフを探す
    handoff_file = _resolve_handoff_file(session_id)
    if not handoff_file.exists():
        # ユーザーが /handoff:dump を呼ばずに /compact した通常フロー
        return 0

    # 注入だけ行う。削除はしない（ハンドオフはそのまま残す運用）
    try:
        _inject_handoff(handoff_file)
    except OSError:
        # 読み込み失敗時はスタックトレースを stderr に流すが、フック自体は成功で返す
        # （PostCompact は失敗させても再実行されないため、ここで落としても意味がない）
        traceback.print_exc(file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
