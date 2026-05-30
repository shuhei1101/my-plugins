# PR113 — merge-skill-remove-redundant-prohibitions

## 概要

merge SKILL.md に書かれている「マージしてという発言がない限りマージするな」系の禁止事項は、`disable-model-invocation: true` が設定されているため不要（このスキルはユーザーが直接呼び出す以外では発動しない）。すべての冗長な禁止事項を削除し、代わりに「このスキルが直近の会話で呼ばれた場合のみマージ可」という1つのガードだけ残す。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260524_merge-skill-remove-redundant-prohibitions/PR113/QA.md` |
| 済 | `description` frontmatter の冗長な禁止文を削除する | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | `## Critical Prohibition` セクション全体を削除する | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | Step 7 の `### Prohibitions` を「直近の呼び出しのみマージ可」の1件に差し替える | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | SKILL.jp.md に同じ変更を反映する | - `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンを上げる | - `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: 変更対象

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
