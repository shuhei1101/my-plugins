# PR117 — pr-show-disable-model-invocation

## 概要

pr-show スキルが "PRやって" や "PR対応して" などの汎用的な発言で誤起動してしまう問題を修正する。
`disable-model-invocation: true` を frontmatter に追加し、description を最小化することで、
スキルから呼び出された場合またはユーザーが直接 `/work-kit:pr-show` を実行した場合のみ発動するようにする。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #113 | disable-model-invocation の冗長禁止事項削除 |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.md に `disable-model-invocation: true` を追加、description を最小化 | - `plugins/work-kit/skills/pr-show/SKILL.md` |
| 済 | SKILL.jp.md を同期 | - `plugins/work-kit/skills/pr-show/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンを更新 | - `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/pr-show/SKILL.md`: 対象スキル

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
