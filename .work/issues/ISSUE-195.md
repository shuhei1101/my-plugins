# ISSUE-195: work/CLAUDE.md に WORK_INJECTION_{TTL,DISABLE,LANG} が未掲載

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/work/hooks/scripts/inject_references.py` は `ENV_PREFIX = "WORK"` を使い、以下の 3 変数を実行時に読み取る：

| 変数名 | 用途 | デフォルト |
|---|---|---|
| `WORK_INJECTION_TTL` | TTL（秒）でパターン/リファレンスキャッシュを制御 | 3600 |
| `WORK_INJECTION_DISABLE` | 注入機構全体のキルスイッチ（truthy で停止） | false |
| `WORK_INJECTION_LANG` | 注入言語（`jp` で日本語版に切替） | en |

しかし `plugins/work/CLAUDE.md` の `## Environment Variables` テーブルには、この 3 変数がいずれも掲載されていない。同じ `ref-inject` テンプレートを使う `claude-kit` と `dev-kit` はそれぞれ `*_INJECTION_*` 3 変数をすべて CLAUDE.md に掲載しており、`work` だけが漏れている。

## 対応方針

`plugins/work/CLAUDE.md` の `## Environment Variables` テーブルに 3 行（`${WORK_INJECTION_TTL}` / `${WORK_INJECTION_DISABLE}` / `${WORK_INJECTION_LANG}`）を追加し、claude-kit / dev-kit との記載レベルを揃える。JP ミラーも同期する。

## 対象ファイル

- `plugins/work/CLAUDE.md`: `## Environment Variables` テーブルに 3 行を追加
- `plugins/work/CLAUDE.jp.md`: JP ミラー同期
