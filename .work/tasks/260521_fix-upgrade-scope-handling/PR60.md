# PR60 — fix-upgrade-scope-handling

## 概要

`marketplace.py upgrade` コマンドで、プロジェクトスコープ（local）でインストールされたプラグインが
`plugin update` に失敗する問題を修正する。スコープを保持したまま uninstall → install で更新する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR60/QA.md` |
| 済 | `.work/specs/` の仕様書を更新する | - `.work/specs/marketplace-upgrade.md` |
| 済 | プラグインのスコープ検出関数を実装する | - `tools/marketplace.py` |
| 済 | `cmd_upgrade` を uninstall+install 方式に変更する | - `tools/marketplace.py` |
| 済 | ルール・CLAUDE.md を整備する | - 不要 |

## 参考ドキュメント

- `.work/specs/marketplace-upgrade.md`: upgradeコマンドの仕様

## QA

なし
