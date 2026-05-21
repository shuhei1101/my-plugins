# PR62 — debug-fab-simplify

## 概要

debug-fab スキルの UI を簡素化する。モーダルを廃止し、FAB クリックで直接ピッカーモードに入る設計へ変更。上部中央にコピーボタンを追加。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260521_debug-fab-simplify/PR62/QA.md` |
| 済 | uidev.js を書き直す（モーダル削除・FAB直接ピッカー・上部コピーボタン） | `plugins/ui-kit/skills/debug-fab/templates/uidev.js` |
| 済 | uidev.css を書き直す（モーダルスタイル削除・上部バースタイル追加） | `plugins/ui-kit/skills/debug-fab/templates/uidev.css` |
| 済 | SKILL.md の description・操作フローを更新する | `plugins/ui-kit/skills/debug-fab/SKILL.md` |
| 済 | templates/CLAUDE.md の使い方説明を更新する | `plugins/ui-kit/skills/debug-fab/templates/CLAUDE.md` |
| 済 | plugin.json / marketplace.json バージョンバンプ | `plugins/ui-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

| 済 | example.html を新 UI に合わせて更新する | `plugins/ui-kit/skills/debug-fab/templates/example.html` |

| 済 | 上部コピーボタンをピッカーモード中のみ表示に変更 | `uidev.css`, `uidev.js` |
| 済 | 上部コピーボタン押下後にピッカーモードを終了する | `uidev.js` |

## 参考ドキュメント

- なし
