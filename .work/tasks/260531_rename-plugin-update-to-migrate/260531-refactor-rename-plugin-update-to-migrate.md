# refactor/rename-plugin-update-to-migrate

> 内部 ID: 236（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`plugin-update` スキル（claude-kit / dev-kit / ref-inject / work の 4 プラグイン）を `plugin-migrate` にリネームし、依存する全参照を更新する。
スキルの用途は「プラグイン構造変更の横断適用（マイグレーション）」であり、update より migrate の方が意図を正確に表す。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録 |
| 2 | 済 | `.work/notes/` のノートを更新 |
| 3 | 済 | 4 プラグインの `skills/plugin-update/` ディレクトリを `skills/plugin-migrate/` にリネーム |
| 4 | 済 | SKILL.md / SKILL.jp.md 内の `plugin-update` 参照を `plugin-migrate` に更新 |
| 5 | 済 | 依存ファイル（CLAUDE.md / references/）の `plugin-update` 参照を `plugin-migrate` に更新 |
| 6 | 済 | rules / CLAUDE.md を確認（インシデントレポート内の過去 grep コマンドのみ — 変更不要） |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/skills/plugin-migrate/SKILL.md` | 編集 | ディレクトリリネーム + 内部参照更新 | 旧: plugin-update |
| 2 | 〃 `SKILL.jp.md` | 〃 | 〃 | - |
| 3 | `plugins/dev-kit/skills/plugin-migrate/SKILL.md` | 〃 | 〃 | 旧: plugin-update |
| 4 | 〃 `SKILL.jp.md` | 〃 | 〃 | - |
| 5 | `plugins/ref-inject/skills/plugin-migrate/SKILL.md` | 〃 | 〃 | 旧: plugin-update |
| 6 | 〃 `SKILL.jp.md` | 〃 | 〃 | - |
| 7 | `plugins/work/skills/plugin-migrate/SKILL.md` | 〃 | 〃 | 旧: plugin-update |
| 8 | 〃 `SKILL.jp.md` | 〃 | 〃 | - |
| 9 | `plugins/claude-kit/references/plugin/plugin-structure.md` | 編集 | `plugin-update` → `plugin-migrate` 参照更新 | - |
| 10 | 〃 `plugin-structure.jp.md` | 〃 | 〃 | - |
| 11 | `plugins/claude-kit/references/plugin/setup-wizard.md` | 編集 | 〃 | - |
| 12 | 〃 `setup-wizard.jp.md` | 〃 | 〃 | - |
| 13 | `plugins/dev-kit/CLAUDE.md` | 編集 | 〃 | - |
| 14 | `plugins/dev-kit/CLAUDE.jp.md` | 〃 | 〃 | - |
| 15 | `plugins/ref-inject/CLAUDE.md` | 編集 | 〃 | - |
| 16 | `plugins/ref-inject/CLAUDE.jp.md` | 〃 | 〃 | - |
| 17 | `plugins/work/CLAUDE.md` | 編集 | 〃 | - |
| 18 | `plugins/work/CLAUDE.jp.md` | 〃 | 〃 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

未解決の QA なし。

## 参考ドキュメント

- [`.work/notes/plugin-migrate-rename.md`](../../../notes/plugin-migrate-rename.md): リネーム作業ノート（本ブランチで作成）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | `chore/260530_claude-kit-plugin-update-skill` | claude-kit に plugin-update を追加した先行ブランチ |
| 2 | `chore/260530_dev-kit-plugin-update-skill` | dev-kit に plugin-update を追加した先行ブランチ |
| 3 | `chore/260530_ref-inject-plugin-update-skill` | ref-inject に plugin-update を追加した先行ブランチ |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
