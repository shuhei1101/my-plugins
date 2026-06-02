# ISSUE-141: merge Step 11 の WORK_MERGE_AUTO_HANDOFF が CLAUDE.md 環境変数テーブルに未掲載

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する

---

## 概要

`plugins/work/skills/merge/SKILL.md` の Step 11 で参照されている `WORK_MERGE_AUTO_HANDOFF` 環境変数が、`plugins/work/CLAUDE.md` の「Environment Variables」テーブルに掲載されていない。ユーザーはこの変数を知ることができず、branch-reserve の自動呼び出しを無効化する方法がドキュメントから発見できない。

## 背景

CLAUDE.md の Environment Variables テーブルはすべての設定可能な変数の一覧として機能しており、ユーザーが参照する唯一のリファレンスになっている。テーブルに載っていない変数は「存在しない」と同等の扱いになる。

## 現状

`plugins/work/skills/merge/SKILL.md`:
- 行 350: `- `WORK_MERGE_AUTO_HANDOFF` is not `false`/`0`/`no`/`off` (default: enabled); if disabled → skip this step and proceed to Step 12`

`plugins/work/CLAUDE.md` Environment Variables テーブル（全 14 行）に `WORK_MERGE_AUTO_HANDOFF` の記載なし。

また `work:plugin-config` スキルの Managed Toggles テーブルにも `WORK_MERGE_AUTO_HANDOFF` は含まれていない。

## 期待される状態

- `plugins/work/CLAUDE.md` の Environment Variables テーブルに `${WORK_MERGE_AUTO_HANDOFF}` を追加する（説明: `work:merge` での `work:branch-reserve` 自動呼び出し、デフォルト true）
- 必要に応じて `work:plugin-config` の Managed Toggles にも追加する

## 対応案

`plugins/work/CLAUDE.md` の Environment Variables テーブルに以下の行を追加する:
```
| `${WORK_MERGE_AUTO_HANDOFF}` | `work:merge` 後に `work:branch-reserve` を自動呼び出し | - **true**<br>- false |
```

変更対象: `plugins/work/CLAUDE.md`（+ JP ミラー）。`plugin-config` への追加は別途検討。
