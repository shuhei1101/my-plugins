# PR213 — existing-inter-plugin-dependency-audit-and-zero-out

## 概要

全プラグインの `skills/`・`hooks/`・`references/` を一括 grep し、他プラグインのスキル・コマンド・スクリプトパスを呼び出している箇所をリストアップ。ユーザーへのレビュー提示後、可能なものから順次「プラグイン内自己完結」へ書き換え、最終的にプラグイン間依存件数ゼロを目指す。

### 背景（PR210 から引き継ぎ）

PR210 で `plugins/claude-kit/references/plugin-structure.md`（+ jp）に `## Zero inter-plugin dependency principle` セクションを追加し、**全プラグインの判断軸**として整備した。本 PR はその原則に照らした棚卸しの実施 PR。

PR210 で定義した「許容される例外」:
- 同プラグイン内のスキル同士の呼び出し
- `ref-inject:apply` による静的テンプレ展開（配布先で閉じる）
- `claude-kit` の references injection 機構（opt-in 型）

上記以外に他プラグインへ参照している箇所は、今 PR で「プラグイン内自己完結」に書き換える。

### 実施条件

即時実施可（PR210 マージ済）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - 本ドキュメント |
| 済 | `.work/notes/` の関連ノートを更新する | - `zero-plugin-dependency.md` |
| 済 | grep で他プラグイン呼び出しを全件リストアップしユーザーに提示 | - `plugins/**/skills/**`<br>- `plugins/**/hooks/**`<br>- `plugins/**/references/**` |
| 済 | 許容例外に該当するか判定し、違反箇所を確定する | - 各ファイル |
| 済 | `notes-to-claude` スキルを削除（違反解消の方針として選択） | - `plugins/work/skills/notes-to-claude/SKILL.md`<br>- `plugins/work/skills/notes-to-claude/SKILL.jp.md` |
| 済 | 削除に伴う参照箇所を更新 | - `plugins/work/templates/.work/CLAUDE.md`<br>- `plugins/work/templates/.work/CLAUDE.jp.md`<br>- `plugins/claude-kit/CLAUDE.md`<br>- `plugins/claude-kit/CLAUDE.jp.md`<br>- claude-kit スキル3ファイル |
| 済 | バージョンバンプ（MINOR/PATCH） | - 対象プラグインの `plugin.json`・`marketplace.json` |
| 済 | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/skills/notes-to-claude/SKILL.md` | 削除 | claude-kit 依存のスキルを削除 | |
| `plugins/work/skills/notes-to-claude/SKILL.jp.md` | 削除 | 〃 | |
| `plugins/work/templates/.work/CLAUDE.md` | 編集 | notes-to-claude の参照を削除 | |
| `plugins/work/templates/.work/CLAUDE.jp.md` | 編集 | 〃 | |
| `plugins/work/.claude-plugin/plugin.json` | 編集 | v2.48.0 にバンプ | |
| `plugins/claude-kit/CLAUDE.md` | 編集 | notes-to-claude の例示を削除 | |
| `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 〃 | |
| `plugins/claude-kit/skills/claude-creator/SKILL.jp.md` | 編集 | 〃 | |
| `plugins/claude-kit/skills/rule-creator/SKILL.jp.md` | 編集 | 〃 | |
| `plugins/claude-kit/skills/skill-creator/SKILL.jp.md` | 編集 | 〃 | |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | v3.43.3 にバンプ | |
| `.claude-plugin/marketplace.json` | 編集 | work・claude-kit のバージョンを更新 | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md` — プラグイン間依存ゼロ原則（判断軸）
- `.work/notes/zero-plugin-dependency.md` — 棚卸し作業ノート（新規作成予定）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #210 | claude-kit plugin-structure にプラグイン間依存ゼロ原則セクション追加（本 PR の判断軸） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
