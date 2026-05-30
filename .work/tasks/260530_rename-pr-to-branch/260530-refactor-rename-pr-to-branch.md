# refactor/rename-pr-to-branch

> 内部 ID: 230（index.yaml 採番用 — クロスリファレンス目的）

## 概要

work プラグインのスキル名とスキル内説明に残っている「PR」「プルリクエスト」概念を
「ブランチ」に統一するリファクタリング。

- `pr-handoff` スキルディレクトリ → `branch-reserve` にリネーム
- `pr-show` スキルディレクトリ → `branch-show` にリネーム
- 各 SKILL.md / SKILL.jp.md の `name:` フィールド、タイトル、説明を更新
- merge / config / references など参照箇所も更新

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `## QA` に未決定事項を記録する |
| 2 | 済 | `.work/notes/` のノートを更新する |
| 3 | 済 | `skills/pr-handoff` → `skills/branch-reserve` にリネームし SKILL.md / SKILL.jp.md を更新 |
| 4 | 済 | `skills/pr-show` → `skills/branch-show` にリネームし SKILL.md / SKILL.jp.md を更新 |
| 5 | 済 | `merge/SKILL.md` / `merge/SKILL.jp.md` 内の参照を更新 |
| 6 | 済 | `config/SKILL.md` / `config/SKILL.jp.md` 内の参照を更新 |
| 7 | 済 | `references/work-dot-work-dir.md` / `.jp.md` 内の参照を更新 |
| 8 | 済 | `references/work-todo-template-sync.md` / `.jp.md` 内の参照を更新 |
| 9 | 済 | ルール / CLAUDE.md を更新する |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/branch-reserve/SKILL.md` | 編集 | pr-handoff からリネーム、name・タイトル・説明を更新 | git mv |
| 2 | `plugins/work/skills/branch-reserve/SKILL.jp.md` | 編集 | 〃 | git mv |
| 3 | `plugins/work/skills/branch-show/SKILL.md` | 編集 | pr-show からリネーム、name・タイトル・説明を更新 | git mv |
| 4 | `plugins/work/skills/branch-show/SKILL.jp.md` | 編集 | 〃 | git mv |
| 5 | `plugins/work/skills/merge/SKILL.md` | 編集 | branch-reserve / branch-show への参照更新 | - |
| 6 | `plugins/work/skills/merge/SKILL.jp.md` | 編集 | 〃 | - |
| 7 | `plugins/work/skills/config/SKILL.md` | 編集 | WORK_MERGE_AUTO_HANDOFF 説明の参照更新 | - |
| 8 | `plugins/work/skills/config/SKILL.jp.md` | 編集 | 〃 | - |
| 9 | `plugins/work/references/work-dot-work-dir.md` | 編集 | /work:pr-handoff → /work:branch-reserve | - |
| 10 | `plugins/work/references/work-dot-work-dir.jp.md` | 編集 | 〃 | - |
| 11 | `plugins/work/references/work-todo-template-sync.md` | 編集 | pr-handoff → branch-reserve、次PR候補 → 次ブランチ候補 | - |
| 12 | `plugins/work/references/work-todo-template-sync.jp.md` | 編集 | 〃 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

未決定事項なし

## 参考ドキュメント

- `.work/notes/PR用語廃止・ブランチ用語統一.md`: PR 用語廃止の経緯と変更方針
- `.work/notes/work-kitスキル群.md`: work プラグインのスキル一覧と設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
