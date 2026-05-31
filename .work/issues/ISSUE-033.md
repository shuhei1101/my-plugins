# ISSUE-033: 複数プラグインで `plugin-migrate` / `plugin-config` の `name` が重複している

**作成日**: 2026-05-31

## 問題

`plugin-migrate` と `plugin-config` というスキル名が複数のプラグインで重複して使われており、同一の Claude Code 環境にインストールされた場合に名前衝突が起きる可能性がある。

| No | ファイル | `name` 値 | プラグインの呼称（CLAUDE.md） |
|---|---|---|---|
| 1 | `plugins/dev-kit/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `dev-kit:plugin-migrate` |
| 2 | `plugins/work/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `work:plugin-migrate` |
| 3 | `plugins/ref-inject/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `ref-inject:plugin-migrate` |
| 4 | `plugins/dev-kit/skills/plugin-config/SKILL.md` | `plugin-config` | `dev-kit:plugin-config` |
| 5 | `plugins/work/skills/plugin-config/SKILL.md` | `plugin-config` | `work:plugin-config` |
| 6 | `plugins/claude-kit/skills/config/SKILL.md` | `config` | `claude-kit:config` |

`name` フィールドはスキルの一意識別子として機能する。CLAUDE.md やスキルディレクトリ上は `{plugin}:{skill}` という命名で管理されているが、frontmatter の `name` がプレフィックスなしだと、Claude Code がスキルを解決する際にどのプラグインのスキルかが曖昧になる。

特に `plugin-migrate` は3プラグインで重複しており、Claude がどの `plugin-migrate` を呼ぶべきか判断しにくくなる。

## 修正案

各スキルの `name` フィールドをプラグインプレフィックス付きに統一する。各スキルの `SKILL.md` および `SKILL.jp.md` を同時に更新する。

| No | ファイル | 現在の `name` | 修正後の `name` |
|---|---|---|---|
| 1 | `plugins/dev-kit/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `dev-kit:plugin-migrate` |
| 2 | `plugins/work/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `work:plugin-migrate` |
| 3 | `plugins/ref-inject/skills/plugin-migrate/SKILL.md` | `plugin-migrate` | `ref-inject:plugin-migrate` |
| 4 | `plugins/dev-kit/skills/plugin-config/SKILL.md` | `plugin-config` | `dev-kit:plugin-config` |
| 5 | `plugins/work/skills/plugin-config/SKILL.md` | `plugin-config` | `work:plugin-config` |

`claude-kit/config` は既存の `name: config` のままでよいか、`claude-kit:config` に変更するかは別途確認が必要。

## 水平展開

`work`、`claude-kit`、`ref-inject` の全スキルを横断して `name` フィールドの命名規則を一括レビューし、プレフィックスポリシーを統一することを推奨する。
