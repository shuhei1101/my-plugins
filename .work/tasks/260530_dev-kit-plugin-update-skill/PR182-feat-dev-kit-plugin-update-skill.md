# PR182 — dev-kit-plugin-update-skill

## 概要

dev-kit プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。workspace は PR168 で本体実装を済ませている。本 PR では同じ規約を dev-kit にも適用する。

### 何をするか

- `plugins/dev-kit/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- dev-kit がプロジェクトに展開する静的成果物（references / hooks 系テンプレ / 各言語の共通ルール用テンプレ等）を、現在インストール済みの dev-kit バージョンに合わせて更新するロジック
- workspace の `plugin-update` SKILL.md (`plugins/workspace/skills/plugin-update/SKILL.md`) を参考実装として参照する
- dev-kit の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | dev-kit が展開する静的成果物を洗い出す | - dev-kit のソース全体 |
| 済 | `plugins/dev-kit/skills/plugin-update/SKILL.md` (+ jp) を作成（workspace 版を参考に） | - 新規 |
| 済 | dev-kit を MINOR bump (4.0.0 → 4.1.0) | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | changelog を CLAUDE.md の `## Changelog` 表に追記 (PR171 で `changelogs/` 廃止のため) | - `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 済 | Skills 表に `plugin-update` 行を追加 | - `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 済 | コミット | - 70069d9 |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/skills/plugin-update/SKILL.md` | 新規 | dev-kit:plugin-update スキル本体（英語） | workspace 版を参考に dev-kit の同期対象（html-implement / html-debug-fab）に差し替え |
| `plugins/dev-kit/skills/plugin-update/SKILL.jp.md` | 新規 | JP ミラー | 先に jp を書いて英語版を生成 |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | version 4.0.0 → 4.1.0 | MINOR bump（新スキル追加） |
| `.claude-plugin/marketplace.json` | 編集 | dev-kit エントリ version 4.0.0 → 4.1.0 | 3 箇所同期維持 |
| `plugins/dev-kit/CLAUDE.md` | 編集 | Skills 表に `plugin-update` 行追加 / `## Changelog` 表を新設し v4.1.0 + v4.0.0 を追記 | PR171 で `changelogs/` ディレクトリ廃止のため表形式に移行 |
| `plugins/dev-kit/CLAUDE.jp.md` | 編集 | 同上の日本語ミラー | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証） | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/workspace/skills/plugin-update/SKILL.md` — 参考実装
- `plugins/claude-kit/references/plugin-structure.md` — `## Required skills` セクションで規定

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | plugin authoring guide に `plugin-update` 必須化を追加（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
