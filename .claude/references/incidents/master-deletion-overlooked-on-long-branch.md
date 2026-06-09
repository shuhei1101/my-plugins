<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 長期ブランチで master 側で既に削除されたファイルを編集した

**日付**: 2026-05-28
**PR**: PR135 (review-next-kit-plugin)

## 背景

PR135 は数日にわたる長期ブランチで多数のコミットを持っていた。最終整理フェーズで、AI は `.claude/rules/feature/_overview.md` に新規エントリ (`kit-hooks-index-sync.md`) を追記した。

ユーザーが master を取り込んだとき、`_overview.md` は **master 側で削除済み** (PR141 / `move-jp-mirror-agent-to-claude-kit` 周辺のクリーンアップで) であることが判明。PR135 が master と同期せずに分岐していたためブランチに残っていただけだった。

これで「ghost ファイル」状態が発生: PR135 は master がもはや存在を想定していないファイルを編集し続けていた。解消には、merge 前に master と整合させるためにブランチ側でも `_overview.md` を削除する別コミットが必要になった。

## 根本原因

長期ブランチでは、AI はローカルに見えるファイルをそのまま canonical な集合と仮定していた。それらが分岐後に master 側で削除されていないか確認していなかった。

特に `_overview.md` や `incidents.md` のような **リスト型ファイル** に新規エントリを追記するとき、AI の反射は「開いて append」 — 「`git log master -- {file}` でファイルが上流でまだ生きているコンセプトか確認する」前段は省かれる。

## 教訓

長期ブランチで（特に `.claude/rules/**`、`.claude/references/**`、overview / index ファイル等を）編集する前に、**まず master 上にファイルが残っているか確認** する:

```bash
git log master --oneline -- {file} | head -5
git show master:{file} 2>&1 | head -3   # エラー → master で削除されている
```

master で削除済みなら、行動は以下のいずれか:

1. **触らない** — 内容を他の場所に書く (例: `.claude/rules/feature/{name}.md` を overview に index させずに直接置く)
2. **意図的に復活させる** — 戻す明確な理由がある場合のみ
3. **master の削除に合わせる** — merge 前にブランチ側でも `git rm` する

## 再発防止

- rule / overview / index ファイルを編集する前に明示的にチェック: `git log master..HEAD --oneline -- {file}` と `git log HEAD..master --oneline -- {file}`
- `_overview.md` 型の index ファイルは、そもそも保守しないことを優先する — フォルダのファイル一覧そのものを index とする。PR135 のインシデントは `_overview.md` が段階的に廃止されていたことを裏付けている
- merge 準備中 (work-kit:merge Step 3) に、master 側の削除を明示的にチェックする: `git diff --diff-filter=D --name-only HEAD..master | grep "{この PR で編集したパス}"`

## 関連

- `extract-step-check-master-first.md` (類似教訓: skill のステップを抽出する前に master を確認)
- `unnecessary-jp-mirror-sync-rule-for-agents.md` (PR141 — `_overview.md` クラスタを削除した変更)
- PR135 commit `5c8ad7d` (整合を復元したクリーンアップコミット)
