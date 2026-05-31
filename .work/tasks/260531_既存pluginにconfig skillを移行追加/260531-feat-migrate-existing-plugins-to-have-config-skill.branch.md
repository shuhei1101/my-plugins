# feat/migrate-existing-plugins-to-have-config-skill

> 内部 ID: 219（index.yaml 採番用 — クロスリファレンス目的）

## 概要

PR167 で work-kit に `config` スキルが追加された。`plugin-config.md` リファレンス（PR175）では「ユーザー向け env トグルを持つプラグインには config スキルを必ず追加する」という規約が整備された。

現在 `dev-kit` には `DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT` / `DEV_KIT_MARKDOWN`（言語 opt-in）と `DEV_KIT_NEXT_TS_CHECK` / `DEV_KIT_MARKDOWN_CHECK`（デフォルト ON）の計 6 つのユーザー向けトグルがあるが、config スキルが存在しない。

また、`work:config` は `NEXT_KIT_TS_CHECK`（旧名、dev-kit merge 後 `DEV_KIT_NEXT_TS_CHECK` に変更済み）と、ポリシー上除外すべき `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` を誤って管理していた。

このブランチでは `dev-kit:config` を新規追加し、`work:config` の誤ったエントリを除去した。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | 済 | ブランチドキュメントを記入する | - `.work/tasks/260531_migrate-existing-plugins-to-have-config-skill/feat-migrate-existing-plugins-to-have-config-skill.md` |
| 2 | 済 | `dev-kit:config` スキルを新規作成（SKILL.md + SKILL.jp.md） | - `plugins/dev-kit/skills/config/SKILL.md`<br>- `plugins/dev-kit/skills/config/SKILL.jp.md` |
| 3 | 済 | `work:config` から `NEXT_KIT_TS_CHECK` / `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` を除去 | - `plugins/work/skills/config/SKILL.md`<br>- `plugins/work/skills/config/SKILL.jp.md` |
| 4 | 済 | dev-kit バージョンバンプ（4.7.0 → 4.8.0）+ changelog | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 5 | 済 | work バージョンバンプ（2.47.0 → 2.48.0）+ changelog | - `plugins/work/.claude-plugin/plugin.json`<br>- `plugins/work/changelogs/v2.48.0.md` |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/dev-kit/skills/config/SKILL.md` | 新規 | dev-kit の env トグル 6 つをインタラクティブに設定するスキル | opt-in と normal polarity の 2 種類 |
| 2 | `plugins/dev-kit/skills/config/SKILL.jp.md` | 新規 | 〃 の日本語ミラー | - |
| 3 | `plugins/work/skills/config/SKILL.md` | 編集 | `NEXT_KIT_TS_CHECK` / `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` を除去、Step 2 を番号リスト方式に変更 | - |
| 4 | `plugins/work/skills/config/SKILL.jp.md` | 編集 | 〃 の日本語ミラーを同期 | - |
| 5 | `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | version → 4.8.0 | - |
| 6 | `plugins/dev-kit/CLAUDE.md` | 編集 | changelog に 4.8.0 エントリを追加 | - |
| 7 | `plugins/dev-kit/CLAUDE.jp.md` | 編集 | 〃 の日本語ミラーを同期 | - |
| 8 | `plugins/work/.claude-plugin/plugin.json` | 編集 | version → 2.48.0 | - |
| 9 | `plugins/work/changelogs/v2.48.0.md` | 新規 | v2.48.0 changelog を追加 | - |
| 10 | `.claude-plugin/marketplace.json` | 編集 | dev-kit 4.8.0 / work 2.48.0 にバンプ | - |

## テスト

なし

## QA

なし

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-config.md`: config スキル設計ガイド
- `plugins/work/skills/config/SKILL.md`: 参照実装

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-219 | migrate-existing-plugins-to-have-config-skill | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/add-plugin-config-skill（PR167） | work-kit に config スキルを追加 |
| 2 | feat/claude-kit-plugin-config-reference（PR175） | plugin-config.md リファレンスを claude-kit に追加 |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | migrate-claude-kit-to-have-config-skill | claude-kit に config スキルを追加（INJECTION_LANG / TTL が対象候補） | 即時実施可 |
