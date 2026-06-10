---
paths:
  - "**/frontend/shared/components/**"
---

# shared/components

ドメインをまたいで使う共通 UI を置く。autonomous Custom Element を `{name}.ts` + `{name}.css` のセットで配置する（作法は `components/カスタムエレメント.md`）。

- ヘッダー / サイド / デバッグ FAB の枠は `app-shell` に集約する（`components/共通シェル.md`）。各画面に個別実装しない。
- ここに入れるのは全画面共通のものだけ。ドメイン内なら `pages/{domain}/_shared/`、1 画面なら画面直下（`共通化の判断.md`）。
- ボタン等の素の共通スタイルは `{name}.css` で持ち、トークン参照・セレクタ毎コメントは CSS 共通ルールに従う。
