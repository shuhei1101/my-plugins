"""テンプレートによる注入テキストの組み立て。"""
from __future__ import annotations

from functools import cache
from pathlib import Path
from string import Template

from inject_rules.features.injection.types import InjectionBlock

HEADER_TEMPLATE = "ヘッダー.txt"
BLOCK_TEMPLATE = "ブロック.txt"
LOADING_TEMPLATE = "読み込み中.txt"
COMPLETED_TEMPLATE = "完了.txt"
PATTERN_SEPARATOR = "、"


@cache
def _load_template(name: str, *, template_dir: Path) -> Template:
    """テンプレートファイルを読んで Template にする。"""
    return Template((template_dir / name).read_text(encoding="utf-8"))


def render_block(block: InjectionBlock, *, template_dir: Path) -> str:
    """注入ブロック 1 件をテキストにする。"""
    template = _load_template(BLOCK_TEMPLATE, template_dir=template_dir)
    patterns = PATTERN_SEPARATOR.join(f"`{pattern}`" for pattern in block.patterns)
    return template.substitute(url=block.url, patterns=patterns, body=block.body)


def render_message(
    blocks: list[InjectionBlock],
    *,
    remaining: int,
    loaded: int,
    total: int,
    template_dir: Path,
) -> str:
    """ブロック群と進捗から注入テキスト全体を組み立てる。"""
    parts = [_load_template(HEADER_TEMPLATE, template_dir=template_dir).template]
    parts.extend(render_block(block, template_dir=template_dir) for block in blocks)
    # 未送信が残っているなら再実行を促す末尾に切り替える
    footer_name = LOADING_TEMPLATE if remaining else COMPLETED_TEMPLATE
    footer = _load_template(footer_name, template_dir=template_dir)
    parts.append(footer.safe_substitute(loaded=loaded, total=total, remaining=remaining))
    return "".join(parts)
