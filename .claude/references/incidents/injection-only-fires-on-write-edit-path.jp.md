<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# リファレンス注入は Write/Edit/Read 経路でしか発火しない

**日付**: 2026-05-29
**分類**: wrong-assumption

## 何が起きたか

PR161 は「AI にスキルを呼ばせるのをやめ、代わりに ref-inject フックが reference を注入する」方針で、
当初は **`mark-generated` スキルを完全削除**し、全呼び出し元（claude-kit / work-kit / html-kit）から
その呼び出しを除去する計画だった。

落とし穴: `claude-kit-references-injection` フックは `PreToolUse(Edit | Write | MultiEdit | Read)`
フックで、**Claude** がそれらのツールでファイルを編集したときだけ、しかも `injection_rules.yaml` に
マッチするパスでしか発火しない。次の2種の呼び出し元はその経路に乗らない:

1. **ヘルパースクリプト出力** — work-kit の `setup-task.py` は Bash の `python` 呼び出しでテンプレから
   `TODO.md` / `QA.md` を書く。Write/Edit ツールを介さないのでフックは発火しない。
2. **非マッチ型** — html-kit の `debug-fab` は `uidev.js` / `uidev.css` / `example.html` を生成する。
   これらは `injection_rules.yaml` に無い（そもそも `.json`/`.js`/`.css` は authoring パターン外）。

完全削除なら、それらのファイルの**出自スタンプが黙って失われていた**（`version-sync` がスタンプに依存）。

## どう回避するか

- AI 呼び出しスキルを「注入 reference だけ」に変える前に、呼び出し元を列挙し、**全対象ファイルが
  Write/Edit 経路にあり**注入ルールにマッチするか確認する。
- そのチェックに通らない呼び出し元（スクリプト生成・非マッチ型）には、スキルを**薄ラッパー**
  （フォールバック）として残し、その*仕様*だけを注入 reference へ移す — ラッパーとフックが
  単一の正本（`references/provenance.md`）を共有する形にする。
- 一般原則: 注入フックは Claude が書くファイルの利便機能であって、他のコード経路が呼ぶスキルの
  万能な置き換えではない。

## コンテキスト

- 注入フックは Claude のツール呼び出しでのみ発火する。`${plugin}/scripts/*.py`（Bash 経由で実行）が
  書くファイルは完全に素通りする。
- PR161 の QA-001 として解決を記録: ハイブリッド — Write/Edit 経路はフック注入、フォールバックは
  薄ラッパー `mark-generated`、work-kit / html-kit の呼び出し元は無変更。
