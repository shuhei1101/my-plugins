---
paths:
  - "**/frontend/**/api*.{ts,js}"
---

# API 層

通信は api 層の fetch ラッパー（`apiFetch`）に集約する。同一オリジン相対パス（`/api/...`）で叩く（FastAPI と同一オリジン配信のため CORS 不要）。型付き Promise を返す。DOM を触らない。

型は openapi.json から生成して参照する（クライアントは生成せず、型だけ）。UI から `fetch` を直叩きしない。
