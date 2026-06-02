# ISSUE-144: plugin-migrate SKILL.md Step 4 に自己参照バグ（「Step 4 のサマリーを表示」）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/skills/plugin-migrate/SKILL.md` の Step 4 冒頭に誤ったステップ参照がある。

```
### Step 4: Apply updates (with user confirmation)
...
1. Show the per-consumer summary from Step 4.
```

Step 4 がまだ実行中なのに「Step 4 のサマリーを表示」と自己参照している。正しくは Step 3（Compare mechanism files and report）で生成されたサマリーを参照するべきで、「Show the per-consumer summary from Step **3**.」が正しい。

同様のバグが `.jp.md` ミラー（`SKILL.jp.md`）の「ステップ4: 更新を適用（ユーザー確認あり）」内「1. ステップ4 のコンシューマーごとのサマリーを表示する。」にも存在する。

## 対応方針

- `SKILL.md` の `1. Show the per-consumer summary from Step 4.` → `1. Show the per-consumer summary from Step 3.` に修正
- `SKILL.jp.md` の `1. ステップ4 のコンシューマーごとのサマリーを表示する。` → `1. ステップ3 のコンシューマーごとのサマリーを表示する。` に修正

## 対象ファイル

- `plugins/ref-inject/skills/plugin-migrate/SKILL.md`: 対象行のステップ番号を修正
- `plugins/ref-inject/skills/plugin-migrate/SKILL.jp.md`: 対応箇所を修正
