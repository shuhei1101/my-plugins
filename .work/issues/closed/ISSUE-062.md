# ISSUE-062: 英語リファレンスファイルに JP ミラーが存在しない（7件）

**作成日**: 2026-05-31

## 問題

以下の英語ソースファイルには対応する `.jp.md` ミラーが存在しない。リポジトリ規約（CLAUDE.md）では「編集時は先に JP ミラーを更新すること」とされており、ミラーが存在しない場合は規約が機能しない状態になる。

| No | ファイル | 種別 |
|---|---|---|
| 1 | `plugins/claude-kit/references/common/環境変数.md` | リファレンス |
| 2 | `plugins/dev-kit/references/next/backend/DB-ID設計.md` | リファレンス |
| 3 | `plugins/dev-kit/references/next/frontend/空状態.md` | リファレンス |
| 4 | `plugins/dev-kit/references/next/frontend/編集ページ-tsx.md` | リファレンス |
| 5 | `plugins/dev-kit/references/next/frontend/詳細ページ-tsx.md` | リファレンス |
| 6 | `plugins/dev-kit/skills/html-debug-fab/SKILL.md` | スキル定義 |
| 7 | `plugins/ref-inject/templates/references/.ref-injects/CLAUDE.md` | テンプレート |

備考:
- `plugins/claude-kit/references/common/環境変数.md` はファイル内に `Japanese mirror: references/common/環境変数.jp.md` という宣言があるが、その実体ファイルが存在しない。
- `_index.md` ファイルは内部カタログ（日本語コンテンツ）であり、ミラー不要と判断して除外している。
- `plugins/ref-inject/templates/references/example/はじめに.md` および同 `_index.md` はテンプレートのスタブであり優先度は低い。

## 修正案

各ファイルに対して `.jp.md` ミラーを作成する。内容は英語ソースを日本語訳したもので、先頭に標準ヘッダーコメントを付与する:

```
<!-- This file is a Japanese mirror of {source}.md. When updating the English original, update this file too. -->
```

特に `環境変数.md` はファイル内でミラーパスが既に宣言されているため優先度が高い。

## 水平展開

新規リファレンス・スキルファイルを追加する際に JP ミラー作成を漏らすパターンが繰り返し発生している（ISSUE-063 の削除残存と合わせて参照）。ファイル追加チェックリストに「`.jp.md` を同時作成したか」の項目を明示するか、CI でペア検証を行うことを検討すべき。
