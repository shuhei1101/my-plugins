# disable-model-invocation スキルへの冗長な禁止事項

## 日付

2026-05-24

## 状況

merge SKILL.md に以下の禁止事項が多数書かれていた:

- `## Critical Prohibition` セクション（全文）
- `description` frontmatter の "Never invoke automatically — only when the user explicitly requests a merge."
- `description` frontmatter の "ABSOLUTE RULE: Never execute git merge on your own initiative..."
- Step 7 `### Prohibitions` の4項目（「マージして」と言われていない限り実行するな、など）

## 原因

`disable-model-invocation: true` が設定されているスキルの動作を正しく理解していなかった。
このフラグが `true` の場合、スキルはユーザーが `/work-kit:merge` のように直接呼び出す以外では
一切発動しない。Claude が自律判断でスキルを起動することはできない。
つまり「自動的に起動するな」「ユーザーの明示的指示なしで動くな」という禁止事項は
フラグの保証と完全に重複しており、書く意味がない。

## 修正

- `## Critical Prohibition` セクションを全削除
- `description` frontmatter の禁止文2行を削除
- Step 7 `### Prohibitions` を以下の1文に置き換え:
  > Only merge if this skill was invoked in the user's **most recent message**. If the skill context is still present from a previous turn (not from the current message), do NOT merge — the previous invocation's permission does not carry over.

この1文だけ残した理由: スキルのシステムプロンプトが以前のターンから残っているとき、
Claude が「前のターンで呼ばれたから今回もマージしていい」と誤解する可能性があるため。

## 教訓

`disable-model-invocation: true` が設定されたスキルに「自動起動禁止」系の禁止事項を書かない。
唯一必要なガードは「直近のメッセージでこのスキルが呼ばれた場合のみ実行」の1件のみ。
