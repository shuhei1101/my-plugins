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
| - | 各ルールの移行先プラグインを決定する | - |
| - | `core/plugin-work.md` の内容を `claude-kit/references/` に統合 | - |
| - | `feature/` 配下の JP ミラー同期ルールを `claude-kit/references/` に統合 | - |
| - | `feature/` 配下の `work-*` ルールを `work/references/` に統合 | - |
| - | `.claude/rules/` と `.claude/rules-jp/` フォルダを削除 | - |
| - | `_injection_rules.yaml` の paths: 設定をリファレンス注入方式に変換 | - |
| - | CLAUDE.md を更新 | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| （実装開始後に記入） | - | - | - |

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
