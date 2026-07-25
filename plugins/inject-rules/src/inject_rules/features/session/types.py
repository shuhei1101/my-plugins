"""セッションドメインのデータモデル。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class SessionState:
    """セッション単位で持ち越す状態。"""

    injected: set[str] = field(default_factory=set)  # 全量を注入し終えたルールの URL
    offsets: dict[str, int] = field(default_factory=dict)  # 部分注入したルールの次の開始位置
    notified: set[str] = field(default_factory=set)  # ログを送出済みの事象キー

    def is_injected(self, url: str) -> bool:
        """当該ルールを全量注入し終えているかを返す。"""
        return url in self.injected

    def offset_of(self, url: str) -> int:
        """部分注入の次の開始位置を返す。"""
        return self.offsets.get(url, 0)

    def mark_injected(self, url: str) -> None:
        """当該ルールを注入済みにし、続き位置を消す。"""
        self.injected.add(url)
        self.offsets.pop(url, None)

    def mark_partial(self, url: str, offset: int) -> None:
        """続き位置を記録する。"""
        self.offsets[url] = offset

    def mark_notified(self, key: str) -> bool:
        """事象が未通知なら記録して True を返す。"""
        if key in self.notified:
            return False
        self.notified.add(key)
        return True
