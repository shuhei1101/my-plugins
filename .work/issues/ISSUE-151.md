# ISSUE-151: work:plugin-config の管理トグル名が CLAUDE.md 環境変数表と乖離している

**作成日**: 2026-06-02

## 問題

`work:plugin-config` スキルが管理するトグル名と、`plugins/work/CLAUDE.md` の `## Environment Variables` 表に記載されている名前が複数箇所で一致していない。スキルが存在しない変数を設定したり、CLAUDE.md に記載された変数がスキルで管理されないという矛盾が生じている。

| plugin-config SKILL.md | work/CLAUDE.md env 表 | 問題 |
|---|---|---|
| `WORK_STOP_REMINDER` | `${WORKSPACE_STOP_REMINDER}` | プレフィックスが `WORK_` vs `WORKSPACE_` |
| `${WORK_MERGE_PROPOSAL}` | `${WORKSPACE_MERGE_PROPOSAL}` | プレフィックスが `WORK_` vs `WORKSPACE_` |
| `WORK_BRANCH_ENFORCEMENT` | （CLAUDE.md に存在しない） | スキルにあるが CLAUDE.md に未記載 |
| `AITUBER_NOTIFY` | （CLAUDE.md に存在しない） | スキルにあるが CLAUDE.md に未記載 |
| （スキルに存在しない） | `${WORK_GUARD}` | CLAUDE.md にあるがスキルで未管理 |

また `WORK_BRANCH_ENFORCEMENT`、`WORK_STOP_REMINDER`、`AITUBER_NOTIFY` は `${}` ラッパーなしで記述されており、`${WORK_USE_WORKTREE}` など他の変数と表記が統一されていない。

## 対応方針

スキルの管理トグル表と CLAUDE.md 環境変数表を照合し、名前の不一致を修正する。どちらの名前を正とするかを決定してから、スキルか CLAUDE.md のいずれかに合わせて統一する。

## 対象ファイル

- `plugins/work/skills/plugin-config/SKILL.md`: 管理トグル表のvar名修正・`${}` ラッパー統一
- `plugins/work/skills/plugin-config/SKILL.jp.md`: JP ミラー同期

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
