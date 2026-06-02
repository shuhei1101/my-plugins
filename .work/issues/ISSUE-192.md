# ISSUE-192: dev-kit changelog にバージョン 4.12.x の記録が欠落

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/CLAUDE.md` と `CLAUDE.jp.md` の `## Changelog` で `4.13.0`（2026-06-01）の次が `4.11.1`（2026-05-31）に飛んでおり、`4.12.x` の記録が一切存在しない。`plugin.json` の現行バージョンは `4.15.0` でバージョン体系は正常。`4.11.0` changelog には `DEV_KIT_MARKDOWN_CHECK` トグルが追加されたと記録されているが、現在の env 変数テーブルにこの変数はなく、`4.12.x` で削除された可能性がある（ISSUE-170 参照）。

## 対応方針

git 履歴を調査して `4.12.x` で行われた変更（`DEV_KIT_MARKDOWN_CHECK` 削除等）を特定し changelog に追記する。スキップなら注記を入れる。

## 対象ファイル

- `plugins/dev-kit/CLAUDE.md`: `4.11.1` と `4.13.0` の間にエントリを追加
- `plugins/dev-kit/CLAUDE.jp.md`: JP ミラー同期

## QA

### QA-1: 対応案の選択

A) git 履歴調査して実変更を記録 / B) スキップ注記のみ

**推奨**: A — `DEV_KIT_MARKDOWN_CHECK` 削除の事実が残るなら env テーブルとの整合性確認も兼ねられる

**回答**: <!-- A / B -->
