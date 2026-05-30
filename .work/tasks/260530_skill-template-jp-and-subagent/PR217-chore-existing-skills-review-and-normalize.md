# PR217 — existing-skills-review-and-normalize

## 概要

PR205 で `skills.jp.md` の JP テンプレートを日本語化し、サブエージェント委譲マーカー記法を確立した。
しかし、リポジトリ内の既存 `SKILL.jp.md` ファイルは旧来の英語セクション名（`Process`、`Tasks`、`Overview` など）
のままになっている。本 PR では全件を見直して新テンプレートに揃える。

**PR205 で決定した標準セクション名（JP ミラー）:**

| 英語（SKILL.md） | 日本語（SKILL.jp.md） |
|---|---|
| `## Overview` | `## 概要` |
| `## Tasks` | `## タスク` |
| `### Step N: <action>` | `### ステップ N: <アクション>` |
| `#### Condition` | `#### 条件` |
| `#### Input` | `#### 入力` |
| `#### Process` | `#### 処理` |
| `#### Output` | `#### 出力` |
| `#### Notes` | `#### 注意事項` |
| `##### Checklist` | `##### チェックリスト` |
| `##### Branching` | `##### 分岐` |
| `##### Prohibitions` | `##### 禁止事項` |
| `## References` | `## 参照` |
| `→ Proceed to Step N+1` | `→ ステップ N+1 へ` |

**サブエージェント委譲マーカー（PR205 で導入）:**
サブエージェントに委譲できる処理は以下のマーカーで明示する:
- `[サブエージェントで実行・完了を待つ]`
- `[サブエージェントで並列実行・完了を待つ]`
- `[サブエージェントで並列実行・完了を待たない]`（稀）

詳細は `plugins/claude-kit/references/subagents.jp.md` を参照。

### 実施条件

即時実施可（PR205 がマージ済み）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を `## QA` に記録する | このドキュメント |
| - | notes ドキュメントを更新する | `.work/notes/skill-template-standards.md` |
| - | 全 `SKILL.jp.md` を Glob してセクション名一覧を収集する | `plugins/**/skills/*/SKILL.jp.md` |
| - | 旧セクション名を新テンプレートに合わせて置換する | 各 `SKILL.jp.md` |
| - | サブエージェント委譲に向いている処理ステップを洗い出す | 各 `SKILL.jp.md` |
| - | 委譲候補ステップに `[サブエージェントで…]` マーカーを付ける | 各 `SKILL.jp.md` |
| - | バージョンバンプ（変更したプラグイン分） | `plugin.json` / `marketplace.json` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/**/skills/*/SKILL.jp.md` | 編集 | セクション名の日本語化・サブエージェントマーカー追加 | 全件 |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストなし | ドキュメント変更のみ |

## QA

QA なし

## 参考ドキュメント

- `plugins/claude-kit/references/skills.jp.md`: JP テンプレート標準（PR205 で更新済み）
- `plugins/claude-kit/references/subagents.jp.md`: サブエージェント委譲ガイド（PR205 で新規作成）
- `.work/notes/skill-template-standards.md`: テンプレート標準とサブエージェントガイドのノート（このノート）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #205 | skills.jp.md テンプレートの日本語化とサブエージェントガイド追加（本PRの前提） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
