# pre-merge master取り込みチェックガード実装

## 概要

破壊マージ防止のため、`git merge` コマンド実行前に2段階チェックを行うフックを workプラグインに実装する。

## 背景

2026-06-14 の事故（masterのtreeが縮小）を受けて、「masterを取り込まずにマージ」または「コンフリクト解消で大量削除」を実行しても被害が出ない仕組みを作る。

## 作業内容

| 完了 | 作業 |
| --- | --- |
| 済 | 案B: masterが対象ブランチの祖先かチェックするフック作成 |
| 済 | dry-run: コンフリクト有無を事前確認するチェックを同フックに追加 |
| 済 | hooks.json にフックエントリを追加 |
| 済 | プロンプトMDファイル作成 |
| 済 | バージョンバンプ（marketplace.json / plugin.json） |

## 実装詳細

### チェック1（案B）: master取り込み確認

`git merge-base --is-ancestor master <branch>` でmasterがブランチの祖先か確認。
そうでなければ「先にmasterをブランチに取り込んでください」とブロック。

### チェック2: dry-runマージ

`git merge --no-commit --no-ff <branch>` でコンフリクトを事前検証。
コンフリクトがあれば `git merge --abort` してブロック、なければ `git merge --abort` して通過。

### 適用除外

- `git merge master` / `git merge main`（上流取り込み）は対象外
- `WORK_GUARD=false` で無効化可能

## 参考ドキュメント

- [pre-merge-check ノート](../../notes/hooks/pre-merge-check.md)

## QA

なし
