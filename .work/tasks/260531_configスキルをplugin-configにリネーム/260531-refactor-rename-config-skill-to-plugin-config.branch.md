# refactor/rename-config-skill-to-plugin-config

> 内部 ID: 234（index.yaml 採番用 — クロスリファレンス目的）

## 概要

各プラグインの `config` スキルを `plugin-config` にリネームする。
現在 `work` と `dev-kit` の 2 プラグインに `config` スキルが存在し、それぞれ `work:config` / `dev-kit:config` として呼び出される。
これを `work:plugin-config` / `dev-kit:plugin-config` に統一する。
SKILL.md・SKILL.jp.md のフロントマター、ドキュメント内テキスト、plugin.json、marketplace.json も合わせて修正する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録する |
| 2 | 済 | ノートドキュメントを更新する |
| 3 | 済 | `plugins/work/skills/config/` を `plugin-config/` にリネーム |
| 4 | 済 | `plugins/dev-kit/skills/config/` を `plugin-config/` にリネーム |
| 5 | 済 | 各 SKILL.md / SKILL.jp.md のフロントマター `name` と本文内スキル名を修正 |
| 6 | 済 | `plugins/work/CLAUDE.md` のスキル名参照を修正 |
| 7 | 済 | `plugins/dev-kit/CLAUDE.md` のスキル名参照を修正 |
| 8 | 済 | `plugins/work/.claude-plugin/plugin.json` の description を修正 |
| 9 | 済 | `plugins/dev-kit/.claude-plugin/plugin.json` の description を修正 |
| 10 | 済 | `.claude-plugin/marketplace.json` の description を修正 |
| 11 | 済 | claude-kit references (plugin-config / plugin-structure / setup-wizard) を修正 |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/plugin-config/SKILL.md` | 新規（リネーム） | config → plugin-config | ディレクトリごとリネーム |
| 2 | `plugins/work/skills/plugin-config/SKILL.jp.md` | 新規（リネーム） | 〃 | - |
| 3 | `plugins/dev-kit/skills/plugin-config/SKILL.md` | 新規（リネーム） | 〃 | - |
| 4 | `plugins/dev-kit/skills/plugin-config/SKILL.jp.md` | 新規（リネーム） | 〃 | - |
| 5 | `plugins/work/CLAUDE.md` | 編集 | work:config → work:plugin-config | - |
| 6 | `plugins/dev-kit/CLAUDE.md` | 編集 | dev-kit:config → dev-kit:plugin-config | - |
| 7 | `plugins/work/.claude-plugin/plugin.json` | 編集 | description 内のスキル名修正 | - |
| 8 | `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 〃 | - |
| 9 | `.claude-plugin/marketplace.json` | 編集 | 〃 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テストなし | - |

## QA

未解決事項なし

## 参考ドキュメント

- `.work/notes/プラグイン設定スキル.md`: プラグイン設定スキル設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/migrate-existing-plugins-to-have-config-skill | config スキルを各プラグインに追加したブランチ |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
