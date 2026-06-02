# ISSUE-186: work の plugin.json description がチェンジログ全文を含み 7500 文字超に肥大化

**作成日**: 2026-06-02

## 問題

`plugins/work/.claude-plugin/plugin.json` の `description` フィールドが 7546 文字に達しており、v2.47.0 から v2.74.0 まで全バージョンのチェンジログを含む巨大なテキストになっている。

`description` は本来「プラグインの概要を説明する 1 行」を想定したフィールド。他プラグインの description 文字数：

| プラグイン | description 文字数 |
|---|---|
| claude-kit | 94 |
| ref-inject | 486 |
| dev-kit | 481 |
| **work** | **7,546** |

チェンジログの本体は `plugins/work/CLAUDE.md` の `## Changelog` テーブルが source of truth であり、description にまで全文を複製すると二重管理・乖離（ISSUE-184 の version drift も同根）・可読性低下を招く。

## 対応方針

`plugin.json` の description を他プラグインと同様の「機能概要のみの短い説明文（1〜3 文）」に削減し、チェンジログは CLAUDE.md の `## Changelog` テーブルのみで管理する。marketplace.json の work エントリ description も同様に肥大化しているため同時に整合させる。

## 対象ファイル

- `plugins/work/.claude-plugin/plugin.json`: description を機能概要のみに削減
- `.claude-plugin/marketplace.json`: work エントリ description を同期

## QA

### QA-1: どの案で進めるか

A) description を機能概要のみに書き直す（changelog は CLAUDE.md のみ） / B) 直近数バージョンのサフィックス付き概要に縮小（dev-kit 方式）

**推奨**: A — 二重管理を完全に解消でき、CLAUDE.md の Changelog テーブルが唯一の changelog ソースになる

**回答**: <!-- A / B -->

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
