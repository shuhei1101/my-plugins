"""`features/injection/packer.py` の単体テスト。"""
from __future__ import annotations

from inject_rules.features.injection.packer import pack_blocks
from inject_rules.features.injection.types import InjectionBlock

A = "https://example.com/a.md"
B = "https://example.com/b.md"
C = "https://example.com/c.md"

CHAR_LIMIT = 1000
MIN_PARTIAL = 200


def _block(url: str, length: int, *, offset: int = 0) -> InjectionBlock:
    """指定文字数の本文を持つ注入ブロックを組み立てる。"""
    return InjectionBlock(url=url, patterns=("**/*.py",), body="あ" * length, offset=offset)


def test_pack_blocks(tmp_template_dir):
    """全件が収まる（正常系）。"""
    # 準備
    blocks = [_block(A, 100), _block(B, 100)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証
    assert result.completed == [A, B]
    assert result.partial == {}
    assert result.remaining == 0


def test_pack_blocks_when_over_limit(tmp_template_dir):
    """分割して持ち越す（正常系）。"""
    # 準備: 上限を超えるブロック 1 件
    blocks = [_block(A, 20000)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 本文が切り出され、続き位置が記録される
    assert len(result.blocks[0].body) < 20000
    assert result.partial == {A: len(result.blocks[0].body)}
    assert result.completed == []
    assert result.remaining == 1


def test_pack_blocks_when_second_over_limit(tmp_template_dir):
    """2 件目で打ち切る（正常系）。"""
    # 準備: 1 件目は収まり 2 件目が超過
    blocks = [_block(A, 100), _block(B, 20000)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 1 件目が完了・2 件目が持ち越し
    assert result.completed == [A]
    assert result.partial == {B: len(result.blocks[1].body)}


def test_pack_blocks_when_min_partial_not_met(tmp_template_dir):
    """最小量を確保できない（正常系）。"""
    # 準備: 1 件目で上限近くまで埋まり、2 件目に最小分割量が残らない
    blocks = [_block(A, 800), _block(B, 20000)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 当該ブロックを送らず残りに数える
    assert [b.url for b in result.blocks] == [A]
    assert result.partial == {}
    assert result.remaining == 1


def test_pack_blocks_when_first_block_too_large(tmp_template_dir):
    """1 件目から超過（正常系）。"""
    # 準備: 上限が小さく、最小分割量すら確保できない
    blocks = [_block(A, 500)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=100, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 進まなくなるのを防ぐため上限分を強制注入して持ち越す
    assert len(result.blocks[0].body) == 100
    assert result.partial == {A: 100}
    assert result.remaining == 1


def test_pack_blocks_when_offset(tmp_template_dir):
    """続きからの詰め込み（正常系）。"""
    # 準備: 続き位置 100 を持つブロック
    blocks = [_block(A, 20000, offset=100)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 続き位置からの本文が送られる
    assert result.partial == {A: 100 + len(result.blocks[0].body)}


def test_pack_blocks_when_remaining(tmp_template_dir):
    """残り件数の算出（正常系）。"""
    # 準備: 3 件中 1 件だけ収まる
    blocks = [_block(A, 800), _block(B, 20000), _block(C, 100)]
    # 実行
    result = pack_blocks(
        blocks, char_limit=CHAR_LIMIT, min_partial=MIN_PARTIAL, template_dir=tmp_template_dir
    )
    # 検証: 送らなかった分が次回に回る
    assert result.completed == [A]
    assert result.remaining == 2
