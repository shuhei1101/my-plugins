# PR185 — ref-inject-plugin-update-skill

## 概要

ref-inject プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。本 PR では同じ規約を ref-inject にも適用する。

### 何をするか

- `plugins/ref-inject/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- ref-inject は `/ref-inject:apply` でターゲットプラグインに展開する templates（injection hook / 各種 references / hooks.json テンプレ等）を持つ。これらのターゲットプラグイン側コピーを最新の ref-inject バージョンに合わせて更新するロジックを提供する
- workspace の `plugin-update` SKILL.md (`plugins/workspace/skills/plugin-update/SKILL.md`) を参考実装として参照する
- ref-inject の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 留意点

ref-inject は「他プラグインに展開するためのテンプレート集」なので、`plugin-update` の責務が少し変わる。「自プロジェクト側の `.work/` を更新する」ではなく「`/ref-inject:apply` が以前展開した先のプラグインの注入関連ファイルを ref-inject の現在バージョンに揃える」という形になる可能性がある。スコープは PR 開始時に再確認する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | ref-inject のスコープ確認（apply 先プラグインへの再注入か、ref-inject 自身の静的成果物か） | - 設計検討 |
| - | `plugins/ref-inject/skills/plugin-update/SKILL.md` (+ jp) を作成（workspace 版を参考に） | - 新規 |
| - | ref-inject を MINOR bump | - `plugins/ref-inject/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | changelog を追加 | - `plugins/ref-inject/changelogs/v{X.Y.Z}.md` |
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

### QA-001: ref-inject の plugin-update が更新する対象

**背景**: workspace / dev-kit / claude-kit は自プロジェクトの `.work/` 等を更新する。ref-inject は他プラグインへ apply するテンプレートしか持っていない。

| 案 | 内容 |
|---|---|
| A | apply 先のプラグインの注入ファイル（hook script + references skeleton + templates）を ref-inject 現バージョンに揃える |
| B | ref-inject 自身が project に展開する静的ファイルはほぼ無いので、no-op スキルに近い形（参考実装の最小コピーのみ） |

**推奨方式**: 着手時にユーザーと相談して確定。A 案が筋として正しいが、再 apply の挙動と区別が必要。

**状態**: 未解決

**決定したら反映先**: SKILL.md 本文

## 参考ドキュメント

- `plugins/workspace/skills/plugin-update/SKILL.md` — 参考実装
- `plugins/claude-kit/references/plugin-structure.md` — `## Required skills` セクションで規定
- `plugins/ref-inject/skills/apply/SKILL.md` — ref-inject の本体スキル（plugin-update との責務分担を整理する材料）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | plugin authoring guide に `plugin-update` 必須化を追加（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
