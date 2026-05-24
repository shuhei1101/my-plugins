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
| - | QA.md に未決定事項を記録する | - `.work/tasks/.../PR94/QA.md` |
| - | 仕様メモを作成（メタデータ記法、警告文言、対象範囲、同期スキルの仕様） | - `.work/notes/generator-metadata.md` |
| - | claude-kit/skill-creator を更新（生成 SKILL.md / SKILL.jp.md に出自メタデータ＋JPミラー警告） | - `plugins/claude-kit/skills/skill-creator/SKILL.md` |
| - | claude-kit/hook-creator を更新（生成 hook にメタデータ） | - `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| - | claude-kit/rule-creator を更新（生成ルールにメタデータ） | - `plugins/claude-kit/skills/rule-creator/SKILL.md` |
| - | claude-kit/claude-creator を更新（生成 CLAUDE.md にメタデータ） | - `plugins/claude-kit/skills/claude-creator/SKILL.md` |
| - | claude-kit/plugin-creator を更新（生成テンプレートにメタデータ） | - `plugins/claude-kit/skills/plugin-creator/SKILL.md` |
| - | 共有 references の判定知識を更新（メタデータ書式ガイド追加） | - `plugins/claude-kit/references/` |
| - | claude-kit に version-sync スキルを新規追加（完全自動: 生成物検出→差分提示→更新→コミット） | - `plugins/claude-kit/skills/version-sync/SKILL.md` |
| - | 既存生成物（全プラグイン）に遡及的にメタデータを書く | - `plugins/{claude-kit,work-kit,worktree-kit,dev-kit,guard-kit,ui-kit}/**` |
| - | claude-kit のバージョンを bump（MINOR: 機能追加） | - `plugins/claude-kit/.claude-plugin/plugin.json` |
| - | claude-kit の changelogs に PR94 エントリを追加 | - `plugins/claude-kit/changelogs/` |
| - | marketplace.json のバージョン同期 | - `.claude-plugin/marketplace.json` |
| - | ルール更新: creator-skill-dispatch.md（出自メタデータ強制ルール追記） | - `.claude/rules/feature/creator-skill-dispatch.md` |
| - | ルール更新: skill-jp-mirror-sync.md（JPミラー警告コメント必須化） | - `.claude/rules/feature/skill-jp-mirror-sync.md` |
| - | glossary に新用語追加（出自メタデータ / version-sync スキル） | - `.claude/rules/core/glossary.md` |
| - | SKILL.jp.md ミラーを同期 | - 各 `SKILL.jp.md` |

## 参考ドキュメント

- `.work/notes/generator-metadata.md`: メタデータ記法・対象範囲・version-sync スキル仕様
- `plugins/claude-kit/changelogs/`: 既存の changelog 構造
- `.claude/rules/feature/creator-skill-dispatch.md`: 既存の creator スキル振り分けルール

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | （現時点で次PR候補なし。version-sync スキルの実運用で課題が出たら追記） |
