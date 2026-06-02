---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-063: 英語オリジナルが削除された JP ミラーが残存（孤立ミラー 4 件）

**作成日**: 2026-05-31

## 問題

以下の `.jp.md` ファイルは、対応する英語オリジナルが削除またはリネームされた後も残存している「孤立ミラー（orphan mirror）」である。これらのファイルは参照先を失っており、メンテナンス対象から外れる。

| No | 孤立 JP ミラー | 状況 |
|---|---|---|
| 1 | `plugins/dev-kit/references/next/frontend/url-state.jp.md` | `url-state.md` が削除済み（`useUrlStateパターン.md` に内容統合と推定） |
| 2 | `plugins/dev-kit/references/python/scripts/launchers-windows.jp.md` | `launchers-windows.md` が削除済み（git 履歴上にのみ存在） |
| 3 | `plugins/dev-kit/skills/py-project/SKILL.jp.md` | `py-project/SKILL.md` が削除済み（git 履歴: `202b9cb7` 時点で削除）。ディレクトリに JP ミラーのみ残存 |
| 4 | `plugins/work/skills/impl-review/SKILL.jp.md` | `impl-review/SKILL.md` が削除済み（git 履歴: `c1e4dcc0` 以降に削除）。ディレクトリに JP ミラーのみ残存 |

## 修正案

孤立ミラーを削除する。削除前に JP ミラー内の情報が他ファイルへの統合に必要か確認すること。

- `url-state.jp.md`: `useUrlStateパターン.jp.md` と内容が重複していないか確認後に削除
- `launchers-windows.jp.md`: 削除（または対応する EN ファイルを復元）
- `py-project/SKILL.jp.md`: 削除（スキル自体が廃止されている場合、ディレクトリごと削除）
- `impl-review/SKILL.jp.md`: 削除（スキル自体が廃止されている場合、ディレクトリごと削除）

## 水平展開

EN ファイルを削除・リネームするリファクタリング時に、対応する JP ミラーの削除・リネームを忘れるパターンが複数件確認された。リファクタリング PR のチェックリストに「JP ミラーの追従削除/リネーム」を追加することを推奨する。
