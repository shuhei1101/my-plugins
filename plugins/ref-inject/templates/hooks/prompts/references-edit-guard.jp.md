<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
このプラグインの `references/` 配下にあるリファレンスファイルを編集または作成しました。先に進む前に、下記の登録漏れがないか確認してください:

## 確認事項

1. **新規ファイルを追加した場合**
   - `references/_index.yaml` と `references/_index.jp.yaml` に `path` と `description` を追加したか
   - `references/_injection_rules.yaml` の対応する `pattern` に `required` または `optional` として登録したか（自動注入が必要なリファレンスの場合）

2. **ファイル名・パスを変更した場合**
   - `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` 内の旧パスをすべて新パスへ更新したか

3. **既存リファレンスの中身だけを編集した場合**
   - 登録情報の更新は不要（このリマインダーはスキップして OK）

## 推奨アクション

該当する場合は、`_index.yaml` と `_injection_rules.yaml` を `Read` で開いて、編集／作成したファイルのパスが正しく登録されているか確認してください。登録漏れがあれば修正し、すでに登録済みなら何もしなくて構いません。

このリマインダーはセッション内 1 回だけ出ます。
