# ISSUE-175: work/CLAUDE.md env 変数テーブルに WORK_BRANCH_ENFORCEMENT が未掲載

**作成日**: 2026-06-02

## 問題

`user-prompt-submit.py` が `WORK_BRANCH_ENFORCEMENT` 環境変数でフック全体を無効化できるが、この変数が `plugins/work/CLAUDE.md` の Environment Variables テーブルに存在しない。`work:plugin-config` スキルには記載があるが CLAUDE.md にはない。

ユーザーが work プラグインの設定を調べる際の一次参照は CLAUDE.md の env テーブルであり、掲載漏れがあるとその変数の存在自体が発見できない。

```python
# plugins/work/hooks/scripts/user-prompt-submit.py
if os.environ.get("WORK_BRANCH_ENFORCEMENT", "true").lower() in ("false", "0", "no", "off"):
    return
```

## 対応方針

CLAUDE.md の Environment Variables テーブルに `${WORK_BRANCH_ENFORCEMENT}` 行を追加（Description: UserPromptSubmit のブランチゲート注入を有効化 / Values: **true** / false）し、JP ミラー（`CLAUDE.jp.md`）も同時更新する。ISSUE-160（WORKSPACE_ vs WORK_ 修正）と合わせて対応すると効率的。

## 対象ファイル

- `plugins/work/CLAUDE.md`: env 変数テーブルに `WORK_BRANCH_ENFORCEMENT` を追加
- `plugins/work/CLAUDE.jp.md`: JP ミラー同期

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
