<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# インシデント: オーファンな dispatch プロンプトは削除ではなくモダン化する

## 何が起きたか

PR153 で `plugins/claude-kit/hooks/prompts/hook-creator-dispatch.{md,jp.md}` と
`plugin-creator-dispatch.{md,jp.md}` が存在するのに `hooks.json` に未配線（オーファン）だった。
git 履歴から、これらは元々 **UserPromptSubmit のキーワード検出**フックで、creator-dispatch を
**PreToolUse のファイルパス**ブロックへ移行した際に取り残されたものと判明した（skill/rule/claude/j2
だけ PreToolUse 版が作られた）。

AI の最初の推奨（QA-001 案A）は、`plugin-creator-dispatch` が `plugins/**` 全体にマッチして広すぎる
ことを理由に、オーファンなプロンプトを**削除**することだった。ユーザーはこれを訂正した: これらは
未移行のまま残った意図された機能であり、正しい対応は**現行の PreToolUse(Edit/Write) 方式に作り変える**
ことであって、削除ではない。

## なぜ削除という発想が誤りだったか

- **旧スタイルの**生成物がオーファン化しているのは、たいてい *意図されたが未移行の機能* であって
  不要物ではない。プロンプトの内容（hook 設定の編集は hook-creator に、plugin の編集は plugin-creator に
  通す）は依然として有用だった。
- 広すぎるという懸念は本物だが、**ルールの順序**（最初にマッチ優先で、広い `plugins/` キャッチオールを
  最後に置き具体ルールを優先させる）で解決でき、削除する必要はなかった。
- これらのフックは claude-kit を導入した *利用側* プロジェクトで発火する。「全部にマッチ」は本マーケット
  プレイス repo の自己適用による現象であって、設計の欠陥ではない。

## 教訓

スタイル/アーキテクチャ移行で取り残されたオーファンな生成物（例: UserPromptSubmit→PreToolUse 移行の
名残プロンプト）を見つけたら、まず**現行パターンへの移行**を既定とし、削除はユーザー確認を取ってから行う。
削除は意図された機能を捨てることになり、移行は前の PR が始めた作業を完了させる。

## 正しい進め方

1. git 履歴（`git log --oneline --all -- {file}`）で、その生成物が存在する理由を確認する。
2. 現行パターンに対応づくなら移行する（本件: `creator_dispatch.py` の `RULES` テーブルに追加、新イベント
   向けにプロンプト文言を書き直し、JP ミラーを同期）。
3. 広さ/重複の懸念は順序付け・スコープ調整で解決し、削除しない。
4. 機能そのものが本当に不要なときだけ削除し、その場合も先に確認する。
