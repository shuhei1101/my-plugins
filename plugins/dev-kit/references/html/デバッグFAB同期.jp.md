<!-- This file is a Japanese mirror of デバッグFAB同期.md. When updating the English original, update this file too. -->
# debug-fab テンプレート同期ルール

`plugins/dev-kit/skills/html-debug-fab/templates/` 配下のファイルを編集したら、
以下のファイルも**必ず同じコミットで更新する**。
英語原文: `references/html/デバッグFAB同期.md`

---

## 同期が必要なファイル

| 編集したファイル | 必ず同時に更新するファイル |
|---|---|
| `uidev.js`（動作変更） | `SKILL.md` — Operation flow セクション |
| `uidev.js`（動作変更） | `templates/CLAUDE.md` — Operations テーブル |
| `uidev.css`（新 UI 要素） | `templates/CLAUDE.md` — Operations テーブル |
| テンプレートファイル全般 | `plugins/dev-kit/.claude-plugin/plugin.json` — バージョンバンプ |
| テンプレートファイル全般 | `.claude-plugin/marketplace.json` — バージョンバンプ |

## バージョンバンプのルール

| 変更の種類 | バンプ |
|---|---|
| バグ修正 / 軽微な修正 | PATCH (`1.x.y` → `1.x.y+1`) |
| 新 UI 要素または動作変更 | MINOR (`1.x.0` → `1.x+1.0`) |
| 完全な再設計 | MAJOR (`1.0.0` → `2.0.0`) |

## コミット前チェックリスト

- [ ] `SKILL.md` の Operation flow が現在の動作を反映している
- [ ] `templates/CLAUDE.md` の Operations テーブルが正確
- [ ] `example.html` が現在のウィジェットを正しく示している
- [ ] `plugin.json` と `marketplace.json` のバージョンがバンプされている
