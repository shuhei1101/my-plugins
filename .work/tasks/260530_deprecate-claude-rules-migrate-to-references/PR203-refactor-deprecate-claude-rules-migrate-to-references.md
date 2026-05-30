# PR203 — deprecate-claude-rules-migrate-to-references

## 概要

`.claude/rules/` 配下のルールファイルを全廃止し、内容を各プラグインの `references/` フォルダへ移行する。

**背景（PR197 からの引き継ぎ）:**
PR197 でプラグインの整合性チェックを追加する際、`.claude/rules/core/plugin-work.md`（ルールファイル）
ではなく `plugins/claude-kit/references/plugin-structure.md`（リファレンス）にのみ記載する方針を決定した。
その理由: ルールファイルは将来的に全廃止してプラグインリファレンスに統合する計画のため。
本 PR はその「全廃止 → リファレンスへ移行」を実施する。

**現在の `.claude/rules/` 構成:**

| ファイル | 内容 |
|---|---|
| `core/plugin-work.md` | プラグイン制作全般のルール |
| `feature/claude-md-jp-mirror-sync.md` | CLAUDE.md の JP ミラー同期 |
| `feature/debug-fab-template-sync.md` | debug-fab テンプレート同期 |
| `feature/hook-prompts-jp-mirror-sync.md` | フックプロンプト JP ミラー同期 |
| `feature/incidents-glossary-jp-mirror-sync.md` | インシデント・グロッサリー JP ミラー同期 |
| `feature/kit-hooks-index-sync.md` | kit フックインデックス同期 |
| `feature/references-jp-mirror-sync.md` | references JP ミラー同期 |
| `feature/skill-jp-mirror-sync.md` | スキル JP ミラー同期 |
| `feature/work-kit-stop-prompt-sync.md` | work-kit ストッププロンプト同期 |
| `feature/work-merge-skill-spec-sync.md` | work:merge スキル仕様同期 |
| `feature/work-start-worktree-link.md` | work:start ワークツリーリンク |
| `feature/work-todo-template-sync.md` | work TODO テンプレート同期 |

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `## QA` に未決定事項を記録する | - |
| - | `.work/notes/` のノートを更新 | - |
| x | 各ルールの移行先プラグインを決定する | - |
| x | `core/plugin-work.md` の内容を `claude-kit/references/` に統合 | PR197 で統合済み |
| x | `feature/` 配下の JP ミラー同期ルールを `claude-kit/references/` に統合 | claude-md.md / skills.md / hooks.md に追記、references-sync.md 新規作成 |
| x | `feature/kit-hooks-index-sync.md` を `claude-kit/references/` に統合 | kit-hooks-sync.md 新規作成 |
| x | `feature/debug-fab-template-sync.md` を `dev-kit/references/` に統合 | html/debug-fab-sync.md 新規作成 |
| x | `feature/` 配下の `work-*` ルールを `work/references/` に統合 | work/references/ 新規作成、注入インフラ追加 |
| x | `.claude/rules/` と `.claude/rules-jp/` フォルダを削除 | - |
| x | `_injection_rules.yaml` の paths: 設定をリファレンス注入方式に変換 | claude-kit/dev-kit の injection_rules.yaml 更新 |
| - | CLAUDE.md を更新 | 変更不要（CLAUDE.md はルールを参照していない） |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/claude-md.md` | 編集 | JP ミラー同期セクションを追加 | |
| `plugins/claude-kit/references/claude-md.jp.md` | 編集 | JP ミラー同期セクション（日本語）を追加 | |
| `plugins/claude-kit/references/skills.md` | 編集 | JP ミラー同期セクションを追加 | |
| `plugins/claude-kit/references/skills.jp.md` | 編集 | JP ミラー同期セクション（日本語）を追加 | |
| `plugins/claude-kit/references/hooks.md` | 編集 | フックプロンプト JP ミラー同期セクションを追加 | |
| `plugins/claude-kit/references/hooks.jp.md` | 編集 | フックプロンプト JP ミラー同期セクション（日本語）を追加 | |
| `plugins/claude-kit/references/references-sync.md` | 新規 | references-jp-mirror-sync.md から移行 | |
| `plugins/claude-kit/references/references-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/claude-kit/references/kit-hooks-sync.md` | 新規 | kit-hooks-index-sync.md から移行 | |
| `plugins/claude-kit/references/kit-hooks-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/claude-kit/references/_injection_rules.yaml` | 編集 | rules パターン削除、references-sync / kit-hooks-sync パターン追加 | |
| `plugins/claude-kit/references/_index.yaml` | 編集 | 新規リファレンス 2 件を追加 | |
| `plugins/claude-kit/references/_index.jp.yaml` | 編集 | 新規リファレンス 2 件（日本語）を追加 | |
| `plugins/dev-kit/references/html/debug-fab-sync.md` | 新規 | debug-fab-template-sync.md から移行 | |
| `plugins/dev-kit/references/html/debug-fab-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/dev-kit/references/_injection_rules.yaml` | 編集 | debug-fab パターンを追加 | |
| `plugins/dev-kit/references/_index.yaml` | 編集 | debug-fab-sync 追加 | |
| `plugins/dev-kit/references/_index.jp.yaml` | 編集 | debug-fab-sync（日本語）追加 | |
| `plugins/work/hooks/hooks.json` | 編集 | Edit/Write/MultiEdit/Read 注入フック追加 | |
| `plugins/work/hooks/scripts/inject_references.py` | 新規 | work 用リファレンス注入フックスクリプト | |
| `plugins/work/hooks/scripts/_common.py` | 編集 | ENV_PREFIX を WORKSPACE → WORK に更新 | |
| `plugins/work/hooks/templates/injection.md.j2` | 新規 | 注入テンプレート（英語） | |
| `plugins/work/hooks/templates/injection.jp.md.j2` | 新規 | 注入テンプレート（日本語） | |
| `plugins/work/references/CLAUDE.md` | 新規 | リファレンスフォルダのインデックス | |
| `plugins/work/references/CLAUDE.jp.md` | 新規 | JP ミラー | |
| `plugins/work/references/_injection_rules.yaml` | 新規 | work 用注入ルール定義 | |
| `plugins/work/references/_index.yaml` | 新規 | リファレンス一覧（英語） | |
| `plugins/work/references/_index.jp.yaml` | 新規 | リファレンス一覧（日本語） | |
| `plugins/work/references/work-stop-prompt-sync.md` | 新規 | stop.md / stop-no-merge.md 同期ルール | |
| `plugins/work/references/work-stop-prompt-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/work/references/work-merge-skill-sync.md` | 新規 | merge SKILL.md ↔ 仕様書同期ルール | |
| `plugins/work/references/work-merge-skill-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/work/references/work-start-skill-sync.md` | 新規 | work-start / worktree-create インターフェース同期ルール | |
| `plugins/work/references/work-start-skill-sync.jp.md` | 新規 | JP ミラー | |
| `plugins/work/references/work-todo-template-sync.md` | 新規 | TODO テンプレート ↔ work-start SKILL.md 同期ルール | |
| `plugins/work/references/work-todo-template-sync.jp.md` | 新規 | JP ミラー | |
| `.claude/rules/` | 削除 | 12 ファイル（全ルール）削除 | |
| `.claude/rules-jp/` | 削除 | 9 ファイル（全 JP ミラー）削除 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストなし | - |

## QA

なし

## 参考ドキュメント

- `.work/notes/deprecate-rules-migrate-to-references.md`: 廃止計画・移行マッピング
- `.work/notes/plugin-claude-md-standard.md`: プラグイン CLAUDE.md 標準セクション構成
- `plugins/claude-kit/references/plugin-structure.md`: プラグイン作成ガイド（移行先の参考）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #197 | plugin-structure.md に CLAUDE.md 更新チェックを追加（ルール廃止方針を決定） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
