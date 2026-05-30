<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# Markdown 編集 — フロントマターの配置

> ファイルに YAML フロントマター（`---` ブロック）がない場合は、このリファレンスを無視してください。

英語版: `references/markdown-editing.md`

---

## ルール

YAML フロントマターを持つ Markdown ファイルでは、**開き `---` より前に何も置いてはならない**。

```
✅ 正しい
---
title: My Doc
---
<!-- 警告コメントやその他のコンテンツはここに -->

❌ 間違い — 開き --- の上にコメントを置いている
<!-- This file is a Japanese mirror. ... -->
---
title: My Doc
---
```

**理由**: GitHub・Obsidian 等の多くの Markdown レンダラーは、`---` がファイルの最初の行にある場合のみ YAML ブロックとして認識する。その上に何かあるとフロントマターが本文として描画されてしまう。

## 修正方法

HTML コメントやその他のコンテンツは、**閉じ `---` の直後**に移動すること。
