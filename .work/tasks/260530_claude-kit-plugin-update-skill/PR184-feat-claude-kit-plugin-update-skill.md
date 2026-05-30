# PR184 — claude-kit-plugin-update-skill

## 概要

claude-kit プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。本 PR では同じ規約を **claude-kit 自身** にも適用する（規約を作ったプラグイン自身が遵守していない状態を解消）。

### 何をするか

- `plugins/claude-kit/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- claude-kit がプロジェクトに展開する静的成果物（CLAUDE.md / rules / references / プロンプトテンプレ等）を、現在インストール済みの claude-kit バージョンに合わせて更新するロジック
- workspace の `plugin-update` SKILL.md (`plugins/workspace/skills/plugin-update/SKILL.md`) を参考実装として参照する
- claude-kit の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | claude-kit が展開する静的成果物を洗い出す | - claude-kit のソース全体 |
| - | `plugins/claude-kit/skills/plugin-update/SKILL.md` (+ jp) を作成（workspace 版を参考に） | - 新規 |
| - | claude-kit を MINOR bump | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | changelog を追加 | - `plugins/claude-kit/changelogs/v{X.Y.Z}.md` |
| - | glossary / CLAUDE.md を必要に応じて更新 | - 該当箇所 |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

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
