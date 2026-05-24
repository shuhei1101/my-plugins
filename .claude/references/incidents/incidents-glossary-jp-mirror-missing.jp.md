<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# incidents-glossary-jp-mirror-missing — incidents/glossary JP ミラー未更新

## 何が起きたか

`incidents.md` や `glossary.md` を編集した後、`rules-jp/core/` 配下の対応する JP ミラーファイルが更新されず、英語版と日本語版の内容が長期間乖離していた。

## 原因

`incidents.md` や `glossary.md` を編集した際に JP ミラーの同時更新を強制するルールが存在しなかった。既存の `skill-jp-mirror-sync.md`、`hook-prompts-jp-mirror-sync.md`、`claude-md-jp-mirror-sync.md` ルールは `rules/core/incidents.md` と `rules/core/glossary.md` をカバーしていなかった。

## 修正（PR112）

`incidents-glossary-jp-mirror-sync.md` ルールを追加し、英語版を変更する際に必ず同じコミットで `rules-jp/core/incidents.md` と `rules-jp/core/glossary.md` を更新するよう強制するようにした。

## 教訓

JP ミラー同期ルールを新しく作る際は、同じディレクトリの他のファイルも同様の「JP ミラー同時更新」パターンが必要かどうかを確認し、最初からカテゴリごとに明示的なルールを設ける。
