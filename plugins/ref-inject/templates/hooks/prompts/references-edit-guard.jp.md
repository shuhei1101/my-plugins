<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
このプラグインの `references/` 配下にあるリファレンスファイルを **これから** 編集または作成しようとしています。編集を実行する前に、下記の登録漏れがないか確認してください:

## 確認事項

1. **新規ファイルを追加しようとしている場合**
   - 作成前（または直後）に、`references/_index.yaml` と `references/_index.jp.yaml` に `path` と `description` を登録する
   - 自動注入が必要なリファレンスなら、`references/_injection_rules.yaml` の対応する `pattern` に `required` または `optional` として登録する

2. **ファイル名・パスを変更しようとしている場合**
   - 同じ作業の中で `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` 内の旧パスをすべて新パスへ更新する

3. **既存リファレンスの中身だけを編集する場合**
   - 登録情報の更新は不要 — このまま編集を進めて OK

## 推奨アクション

(1) または (2) の場合は、編集を実行する前にまず `_index.yaml` と `_injection_rules.yaml` を `Read` で開いて、登録するエントリのイメージを掴んでから一連の編集を行う。これにより `references/` 本体と登録ファイルが乖離するのを防げる。

このリマインダーはセッション内 1 回だけ出ます。
