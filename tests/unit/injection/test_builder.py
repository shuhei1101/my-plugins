"""`features/injection/builder.py` の単体テスト。"""
from __future__ import annotations

import string

import pytest

from inject_rules.features.injection.builder import _load_template, render_block, render_message
from inject_rules.features.injection.types import InjectionBlock

A = "https://example.com/a.md"
B = "https://example.com/b.md"


def _block(url: str, body: str, *, patterns: tuple[str, ...] = ("**/*.py",)) -> InjectionBlock:
    """テスト用の注入ブロックを組み立てる。"""
    return InjectionBlock(url=url, patterns=patterns, body=body)


# =========================
# _load_template
# =========================


def test_load_template(tmp_template_dir):
    """テンプレートの読み込み（正常系）。"""
    # 実行
    template = _load_template("ヘッダー.txt", template_dir=tmp_template_dir)
    # 検証
    assert isinstance(template, string.Template)
    assert template.template == (tmp_template_dir / "ヘッダー.txt").read_text(encoding="utf-8")


def test_load_template_when_missing(tmp_template_dir):
    """ファイルなし（異常系）。"""
    # 実行・検証
    with pytest.raises(FileNotFoundError):
        _load_template("存在しない.txt", template_dir=tmp_template_dir)


# =========================
# render_block
# =========================


def test_render_block(tmp_template_dir):
    """1 ブロックの描画（正常系）。"""
    # 準備
    block = _block(A, "命名規約の本文")
    # 実行
    text = render_block(block, template_dir=tmp_template_dir)
    # 検証
    assert A in text
    assert "`**/*.py`" in text
    assert "命名規約の本文" in text


def test_render_block_when_multiple_patterns(tmp_template_dir):
    """複数パターンの連結（正常系）。"""
    # 準備
    block = _block(A, "本文", patterns=("**/*.py", "**/*.md"))
    # 実行
    text = render_block(block, template_dir=tmp_template_dir)
    # 検証: 読点区切りで並ぶ
    assert "`**/*.py`、`**/*.md`" in text


# =========================
# render_message
# =========================


def test_render_message(tmp_template_dir):
    """完了時の描画（正常系）。"""
    # 準備
    blocks = [_block(A, "本文 A")]
    # 実行
    message = render_message(
        blocks, remaining=0, loaded=1, total=1, template_dir=tmp_template_dir
    )
    # 検証: ヘッダー + ブロック + 完了表示
    assert message.startswith("[ヘッダー]")
    assert "本文 A" in message
    assert "1/1 ファイル読み込み完了" in message


def test_render_message_when_remaining(tmp_template_dir):
    """未完了時の描画（正常系）。"""
    # 準備
    blocks = [_block(A, "本文 A")]
    # 実行
    message = render_message(
        blocks, remaining=1, loaded=1, total=2, template_dir=tmp_template_dir
    )
    # 検証: 末尾が読み込み中表示になる
    assert "読み込み中（1/2 ファイル）" in message
    assert "残り 1 件" in message


def test_render_message_when_multiple_blocks(tmp_template_dir):
    """複数ブロックの連結（正常系）。"""
    # 準備
    blocks = [_block(A, "本文 A"), _block(B, "本文 B")]
    # 実行
    message = render_message(
        blocks, remaining=0, loaded=2, total=2, template_dir=tmp_template_dir
    )
    # 検証: 2 件が順に並ぶ
    assert message.index("本文 A") < message.index("本文 B")
