"""注入上限に収めるブロックの詰め込み。"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from inject_rules.features.injection.builder import render_message
from inject_rules.features.injection.types import InjectionBlock, PackResult


def pack_blocks(
    blocks: list[InjectionBlock],
    *,
    char_limit: int,
    min_partial: int,
    template_dir: Path,
) -> PackResult:
    """ブロック群を注入上限に収まるよう詰め、超過分を次回へ持ち越す。"""
    sending: list[InjectionBlock] = []
    completed: list[str] = []
    partial: dict[str, int] = {}
    total = len(blocks)

    for block in blocks:
        candidate = [*sending, block]
        length = len(
            render_message(
                candidate,
                remaining=total - len(candidate),
                loaded=len(candidate),
                total=total,
                template_dir=template_dir,
            )
        )
        if length <= char_limit:
            # 丸ごと収まる: そのまま送って完了扱いにする
            sending.append(block)
            completed.append(block.url)
            continue

        # 本文を空にした状態の描画長が、このブロックに割ける余白の基準になる
        # ここへ来た時点で必ず持ち越しが出るため、末尾は未完了時のテンプレートで測る
        probe = [*sending, replace(block, body="")]
        used = len(
            render_message(
                probe,
                remaining=total - len(completed),
                loaded=len(completed),
                total=total,
                template_dir=template_dir,
            )
        )
        available = char_limit - used
        if available >= min_partial:
            # 読める量を確保できる: 途中まで送って続き位置を残す
            sending.append(replace(block, body=block.body[:available]))
            partial[block.url] = block.offset + available
            break
        if not sending:
            # 1 件目から入らない: 何も送れず進まなくなるので上限分を強制的に切り出す
            sending.append(replace(block, body=block.body[:char_limit]))
            partial[block.url] = block.offset + char_limit
            break
        # 余白が足りず既に送る分もある: このブロックは丸ごと次回へ回す
        break

    return PackResult(
        blocks=sending, completed=completed, partial=partial, remaining=total - len(completed)
    )
