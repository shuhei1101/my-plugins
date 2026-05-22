---
description: Auto-loaded when editing files under plugins/ui-kit/skills/debug-fab/templates/
globs:
  - "plugins/ui-kit/skills/debug-fab/templates/**"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/feature/debug-fab-template-sync.md` も同時に更新してください。

# debug-fab テンプレート同期ルール

`uidev.js` または `uidev.css` を編集した場合、同じコミットで以下のファイルも更新すること:

## 必須同期対象

| 編集ファイル | 合わせて更新するもの |
|---|---|
| `uidev.js`（動作変更） | `SKILL.md` — Operation flow セクション |
| `uidev.js`（動作変更） | `templates/CLAUDE.md` — Operations テーブル |
| `uidev.css`（新UI要素） | `templates/CLAUDE.md` — Operations テーブル |
| テンプレートファイル全般 | `plugins/ui-kit/.claude-plugin/plugin.json` — バージョンバンプ |
| テンプレートファイル全般 | `.claude-plugin/marketplace.json` — バージョンバンプ |

## バージョンバンプの規則

| 変更の種類 | バンプ |
|---|---|
| バグ修正・小さな修正 | PATCH（`1.x.y` → `1.x.y+1`） |
| 新UI要素・動作変更 | MINOR（`1.x.0` → `1.x+1.0`） |
| 完全な再設計 | MAJOR（`1.0.0` → `2.0.0`） |

## コミット前チェックリスト

- [ ] `SKILL.md` の Operation flow が現在の動作を反映している
- [ ] `templates/CLAUDE.md` の Operations テーブルが正確
- [ ] `example.html` が現在のウィジェットを正しく示している
- [ ] `plugin.json` と `marketplace.json` のバージョンがバンプされている
