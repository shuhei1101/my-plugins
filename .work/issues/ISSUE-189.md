# ISSUE-189: work:impl-review の SKILL.md（英語ソース）が欠落

**作成日**: 2026-06-02

## 問題

`plugins/work/skills/impl-review/` に `SKILL.jp.md` のみ存在し、**`SKILL.md`（英語ソースファイル）が存在しない**。`SKILL.jp.md` の先頭コメントは「Japanese mirror of SKILL.md」と明記しているが、参照先が実在しない。

Claude Code はスキルを呼び出す際に `SKILL.md` を読み込むため、`work:impl-review` が正しく認識・動作しない可能性がある。ISSUE-167（dev-kit:py-project の同種問題）と同じパターン。

## 対応方針

`SKILL.jp.md` の内容を英語に翻訳して `SKILL.md` を新規作成する（または git 履歴から復元する）。`SKILL.md` を source of truth とし、`SKILL.jp.md` をミラーとする標準構造に戻す。

## 対象ファイル

- `plugins/work/skills/impl-review/SKILL.md`: 新規作成（英語ソース）

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
