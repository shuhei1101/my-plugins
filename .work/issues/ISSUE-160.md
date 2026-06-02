# ISSUE-160: work/CLAUDE.md の環境変数表が WORKSPACE_ プレフィックスを誤用（実装は WORK_ プレフィックス）

**作成日**: 2026-06-02

## 問題

`plugins/work/CLAUDE.md` の Environment Variables テーブルでは以下の変数名を掲載している：

- `${WORKSPACE_STOP_REMINDER}`
- `${WORKSPACE_MERGE_PROPOSAL}`

しかし実際のフックスクリプト `plugins/work/hooks/scripts/stop.py` では `WORK_STOP_REMINDER` / `WORK_MERGE_PROPOSAL`（`WORK_` プレフィックス）を使用している。`work:plugin-config/SKILL.md` も `WORK_` プレフィックスを参照しており、実装と SKILL.md は一致している。

ドキュメント（CLAUDE.md）だけが `WORKSPACE_` プレフィックスのまま残っており、ユーザーが CLAUDE.md を参照して `WORKSPACE_STOP_REMINDER=false` を設定しても、実際のフックは `WORK_STOP_REMINDER` を読むため**設定が効かない**。

関連: ISSUE-151（work:plugin-config SKILL.md 側のトグル名乖離）と合わせて対応することが望ましい。

## 対応方針

`plugins/work/CLAUDE.md` の Environment Variables テーブルの変数名を実装に合わせて修正する：

| 誤（現状） | 正（実装） |
|---|---|
| `${WORKSPACE_STOP_REMINDER}` | `${WORK_STOP_REMINDER}` |
| `${WORKSPACE_MERGE_PROPOSAL}` | `${WORK_MERGE_PROPOSAL}` |

## 対象ファイル

- `plugins/work/CLAUDE.md`: 変数名を `WORK_STOP_REMINDER` / `WORK_MERGE_PROPOSAL` に修正

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
