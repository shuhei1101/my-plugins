---
paths:
  - "**/ws/**/*.{ts,js}"
---

# WebSocket

`class WsClient extends EventTarget` で実装し、購読側は `addEventListener` で受ける。再接続は指数バックオフ。URL は `createWsUrl()` 経由（ハードコードしない）。

接続断・パース失敗は握りつぶさず、適切にイベントで通知する（core/エラーは握りつぶさない と整合）。
