# PR94 — generator-metadata

## 概要

creator スキル群が生成するファイル（SKILL.md / SKILL.jp.md / ルール / CLAUDE.md / hook / plugin.json など）に、
**出自メタデータ**（生成元プラグイン名・スキル名・プラグインバージョン）を HTML コメント形式で埋め込む機能を全 creator スキルに追加する。
JP ミラーには加えて「これは日本語ミラーです。SKILL.md を編集したら同期してください」という警告コメントを必ず付与する。
既存の全生成物にも遡及的にメタデータを書き込む。
さらに、プラグインのバージョン更新時に関連する生成物を完全自動で同期するスキルを claude-kit に新規追加する。

### 背景

- プラグインのバージョンが上がったときに、そのプラグインで生成された他プラグインの生成物（スキル、ルールなど）にも変更を反映したい
- そのためには「どの生成物が、どのプラグインの、どのバージョンで作られたか」が分かる必要がある
- メタデータはコメント形式とし、AI に強い意味を持たれにくい形にする（frontmatter は避ける）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR94/QA.md` |
| 済 | 仕様メモを作成（メタデータ記法、警告文言、対象範囲、同期スキルの仕様） | - `.work/notes/generator-metadata.md` |
| 済 | 仕様メモを `mark-generated` スキル切り出し方針に更新 | - `.work/notes/generator-metadata.md` |
| - | `mark-generated` スキルを新規作成（ファイル種別ごとのメタデータ書式・JPミラー警告文言を提供） | - `plugins/claude-kit/skills/mark-generated/SKILL.md` `SKILL.jp.md` |
| - | claude-kit/skill-creator に「生成前に /claude-kit:mark-generated を起動して書式取得→埋め込み」ステップ追加 | - `plugins/claude-kit/skills/skill-creator/SKILL.md` |
| - | claude-kit/hook-creator に同上ステップ追加 | - `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| - | claude-kit/rule-creator に同上ステップ追加 | - `plugins/claude-kit/skills/rule-creator/SKILL.md` |
| - | claude-kit/claude-creator に同上ステップ追加 | - `plugins/claude-kit/skills/claude-creator/SKILL.md` |
| - | claude-kit/plugin-creator に同上ステップ追加（changelogs/ への適用） | - `plugins/claude-kit/skills/plugin-creator/SKILL.md` |
| - | 全プラグインの固定生成物を作るスキルを洗い出し（creator 系以外も対象: work-start / pr-handoff / conversation-to-claude / setup スクリプト等） | - 全プラグイン横断調査 |
| - | work-kit/work-start に mark-generated 呼び出しステップ追加（TODO.md / QA.md / spec / notes 生成時） | - `plugins/work-kit/skills/work-start/SKILL.md` |
| - | work-kit/pr-handoff に同上ステップ追加（次PR テンプレ生成時） | - `plugins/work-kit/skills/pr-handoff/SKILL.md` |
| - | conversation-to-claude に同上ステップ追加（rule/skill/claude.md 生成時。creator 呼び出し済みなら二重適用しない） | - `plugins/work-kit/skills/conversation-to-claude/SKILL.md` |
| - | work-kit:setup などスクリプト系の生成物にもメタデータが入るよう手当て | - `plugins/work-kit/skills/setup/**` |
| - | 他プラグインで該当スキルが見つかった場合 mark-generated 呼び出しを追加 | - `plugins/{worktree-kit,dev-kit,guard-kit,ui-kit}/**/SKILL.md` |
| - | claude-kit に version-sync スキルを新規追加（完全自動: 生成物検出→差分反映→コミット） | - `plugins/claude-kit/skills/version-sync/SKILL.md` |
| - | 既存生成物（全プラグイン）に遡及的にメタデータを書く | - `plugins/{claude-kit,work-kit,worktree-kit,dev-kit,guard-kit,ui-kit}/**` |
| - | claude-kit のバージョンを bump（MINOR: 機能追加） | - `plugins/claude-kit/.claude-plugin/plugin.json` |
| - | claude-kit の changelogs に PR94 エントリを追加 | - `plugins/claude-kit/changelogs/` |
| - | work-kit のバージョンを bump（mark-generated 呼び出し追加分） | - `plugins/work-kit/.claude-plugin/plugin.json` |
| - | marketplace.json のバージョン同期 | - `.claude-plugin/marketplace.json` |
| - | ルール更新: creator-skill-dispatch.md（mark-generated 必須呼び出しを明記） | - `.claude/rules/feature/creator-skill-dispatch.md` |
| - | ルール更新: skill-jp-mirror-sync.md（JPミラー警告コメント必須化） | - `.claude/rules/feature/skill-jp-mirror-sync.md` |
| - | glossary に新用語追加（mark-generated / 出自メタデータ / version-sync スキル） | - `.claude/rules/core/glossary.md` |
| - | SKILL.jp.md ミラーを同期 | - 各 `SKILL.jp.md` |

## 参考ドキュメント

- `.work/notes/generator-metadata.md`: メタデータ記法・対象範囲・version-sync スキル仕様
- `plugins/claude-kit/changelogs/`: 既存の changelog 構造
- `.claude/rules/feature/creator-skill-dispatch.md`: 既存の creator スキル振り分けルール

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | （現時点で次PR候補なし。version-sync スキルの実運用で課題が出たら追記） |
