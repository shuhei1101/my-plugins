# PR205 — skill-template-jp-and-subagent

## 概要

`skills.jp.md` の JP テンプレート雛形を日本語化し、サブエージェント使用ガイドを追加する。

現状では `SKILL.jp.md` を作成する際の雛形（ステップ構造・完全な骨格）のセクション名が英語のままになっており、
JP ミラーを見直したときに「Process」「Tasks」「Overview」などの名称が揃っていない。
JP テンプレートを日本語のセクション名で統一し、新規スキル作成時の一貫性を確保する。

また、ステップ内の処理をサブエージェントに委譲するケースについてのガイド・マーカー記法を追加する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | このドキュメント |
| 済 | notes ドキュメントを更新する | `.work/notes/` |
| 済 | ステップ構造テンプレート（コードブロック）のセクション名を日本語化 | `skills.jp.md` |
| 済 | 完全な SKILL.jp.md 骨格をテンプレートとして追加（日本語セクション名） | `skills.jp.md` |
| 済 | サブエージェント使用ガイドセクションを追加 | `skills.jp.md` |
| 済 | バージョンバンプ | `plugin.json` / `marketplace.json` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/skills.jp.md` | 編集 | テンプレート雛形の日本語化・サブエージェントガイド追加 | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | バージョンバンプ | PATCH |
| `.claude-plugin/marketplace.json` | 編集 | バージョンバンプ | PATCH |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストなし | ドキュメント変更のみ |

## QA

QA なし

## 参考ドキュメント

- `plugins/claude-kit/references/skills.md`: 英語原本（JP ミラーの参照元）
- `plugins/claude-kit/references/skills.jp.md`: 変更対象
- `.work/notes/skill-template-standards.md`: テンプレート標準とサブエージェントガイドのノート

## 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| existing-skills-review-and-normalize | 既存スキル全件見直し：JP ミラーのセクション名を新テンプレートに合わせて統一し、サブエージェント委譲候補を洗い出す | 「PR205 skill-template-jp-and-subagent」が完了したら |
