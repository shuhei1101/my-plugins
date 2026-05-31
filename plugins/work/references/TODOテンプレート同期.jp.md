<!-- This file is a Japanese mirror of TODOテンプレート同期.md. When updating the English original, update this file too. -->
# work TODO テンプレート同期

タスクドキュメントのテンプレートを `work-start` SKILL.md の Step 7 記入ガイドと同期させる。
テンプレートのセクション構成が記入ガイドから乖離すると、生成されたタスクドキュメントが
ドキュメント化されたワークフローと一致しなくなる。
英語原文: `references/TODOテンプレート同期.md`

---

## 関連ファイル

| ファイルパス | 役割 |
|---|---|
| `plugins/work/templates/note.md` | work プラグインに同梱されるノートテンプレート |
| `plugins/work/skills/start/SKILL.md` | タスクドキュメントへの記入方法を定義するスキル（Step 7） |
| `plugins/work/skills/branch-reserve/SKILL.md` | タスクドキュメントの `## 次ブランチ候補` を読んで次のブランチを決定するスキル（Step 1） |

## 編集時のチェック

このドメインのいずれかのファイルを変更したとき、他のファイルも確認する:

- [ ] `templates/note.md` のセクション構成が `work-start` SKILL.md Step 7 の記入指示と一致している
- [ ] 新しく追加したセクションに対応する記入指示が SKILL.md Step 7 にある
- [ ] 削除・リネームしたセクションの SKILL.md Step 7 のエントリも削除・更新している
- [ ] `## 次ブランチ候補` のリネーム・削除があった場合、`branch-reserve` SKILL.md Step 1 も更新している
- [ ] `## 次ブランチ候補` のカラムが変わった場合、`branch-reserve` と `work-start` SKILL.md Step 7 の両方を更新している

## コミット前チェックリスト

- [ ] テンプレートと SKILL.md Step 7 の記入ガイドが同期している
- [ ] `branch-reserve` SKILL.md Step 1 が `## 次ブランチ候補` のセクション構造と一致している
