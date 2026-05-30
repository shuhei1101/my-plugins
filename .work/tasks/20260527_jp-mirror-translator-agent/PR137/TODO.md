# PR137 — agent-jp-mirror-rule

## 概要

PR133 で work-kit に `jp-mirror-translator` エージェントを追加した。
`plugins/{name}/agents/*.md` ↔ `agents/*.jp.md` の同期を強制するルールがまだ存在しないため、
`skill-jp-mirror-sync.md` / `hook-prompts-jp-mirror-sync.md` と同形式の同期ルールを追加する。

**背景 (PR133 から引き継ぎ):**
- PR133 で agents/*.md を手書き作成した際、`mark-generated` スタンプを省略し frontmatter 前に置くミスが発生した（incidents に記録済み）
- ルールがあれば「agents/*.md を編集した時に .jp.md も確認する」チェックリストが自動挿入され再発を防げる

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #133 | jp-mirror-translator エージェントを作成（このルールのトリガーになったPR） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR137/QA.md` |
| 済 | `.work/notes/` のノートを更新する | - `.work/notes/jp-mirror-policy.md` |
| 済 | エージェントファイル JP ミラー同期ルールを作成する | - `.claude/rules/feature/agent-jp-mirror-sync.md` |
| 済 | JP ミラーを作成する | - `.claude/rules-jp/feature/agent-jp-mirror-sync.md` |
| 済 | `_overview.md` にルールを追記する | - `.claude/rules/feature/_overview.md` |

## 参考ドキュメント

- `.claude/rules/feature/skill-jp-mirror-sync.md`: 同形式のルール参考
- `.work/notes/jp-mirror-policy.md`: JP ミラーポリシーのメモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
