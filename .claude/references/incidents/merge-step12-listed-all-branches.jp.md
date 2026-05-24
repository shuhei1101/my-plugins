<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# インシデント: merge Step 12 が次PR候補ではなく全ブランチを列挙していた

## まとめ

merge スキルの Step 12 が `git branch --list 'PR*'` で**全 PR ブランチ**を列挙していた。
今マージした PR の `## 次PR候補` と無関係な他セッションのブランチも表示され、混乱の原因になっていた。

## 何が起きたか

PR104 のマージ後に Step 12 が以下の出力を表示した：

```
PR108/feat/md-jp-mirror-hook: 1
PR109/feat/pr-show-skill: 1
PR74/feat/branch-index-cleanup-skill: 1
PR75/feat/branch-index-sync-rule: 1
```

これらはすべて PR104 の `## 次PR候補` に記載されていないブランチであり、Step 12 の本来の目的（今マージした PR に連動する次候補を提示する）とは無関係だった。

## 根本原因

Step 12 の実装がデータソースとして `git branch --list 'PR*'` を使っており、リポジトリ内の全 PR ブランチを返していた。Step 12 の趣旨は「今マージした PR の次候補を提示する」であり、全ブランチ列挙は過剰だった。

## 修正内容

PR111 で Step 12 を修正した：

- **旧**: `git branch --list 'PR*' --format='%(refname:short)'` で全ブランチを列挙
- **新**: マージした PR の `## 次PR候補` テーブルをデータソースにし、各候補のタイトルでブランチ検索

```bash
# 候補タイトルに一致するブランチを検索（例: "md-jp-mirror-hook"）
git branch --list "*{candidate-title}*"
```

- 実施条件が他候補依存の場合はブランチ検索をスキップし、「条件あり」として表示

## 再発防止

Step 12 でブランチリストを扱うときは、グローバルな `git branch --list 'PR*'` ではなく、
必ず直前マージ PR の `## 次PR候補` テーブルをデータソースとして使うこと。
