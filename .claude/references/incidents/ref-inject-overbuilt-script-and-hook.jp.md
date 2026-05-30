<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# ref-inject で生成スクリプトと PreCompact フックを過剰実装した

## 何が起きたか

`ref-inject` プラグインの構築中（PR156）、AI は次の2つの仕組みを追加したが、ユーザーがいずれも削除した:

1. テンプレートをコピーし、プレースホルダを置換し、`marketplace.json` に登録する決定論的な
   `scripts/generate.py`。ユーザーは削除を指示 — **Claude がテンプレートを読んで自分で書く**方式を
   望んだ。そのほうが生成がコンテキストに残り、プラグインごとに調整しやすいため。
2. `/compact` 後にセッショントークンを削除して即再注入させる `PreCompact` フック
   （`refresh_on_compact.py`）。**TTL トークンが期限経過で再注入する**ため、compact 専用フックは
   無駄と判断され削除された。

## なぜ問題か

どちらも、より単純な既存の経路（Claude 主導コピー / TTL 期限切れ）で既に賄える挙動のための
余計な仕組みだった。それぞれ、得るものが無いのに保守対象ファイルを増やした。

## 教訓

- このリポジトリでのプラグイン／ファイル生成は、決定論的スクリプトより **Claude 主導の
  コピー + 置換**を優先する — 作業がコンテキストに残り、調整しやすい。
- 既存の仕組み（ここでは TTL トークン）が既に提供する挙動のために、専用フックを追加しない。
- 最小の仕組みをデフォルトにし、単純な経路が明確に不足する場合にだけインフラを足す。

## 関連

- PR156: ref-inject を作成。generate.py と refresh_on_compact.py を両方追加後に削除
- 同系の教訓: [[premature-cross-plugin-centralization]]、[[session-kit-removed-after-premise-change]]
