# PR194 — translate-injection-rules-comments

## 概要

各プラグインの `references/injection_rules.yaml` 内のコメントが英語と日本語で混在しているため、すべて日本語コメントに統一する。プロジェクト全体の方針（CLAUDE.md / SKILL.md / 注入ルール）の説明は日本語でメンテナンスしているため、ルール定義ファイルのコメントもそれに揃える。

対象は ref-inject の注入機構を使っている各プラグイン:

- `plugins/claude-kit/references/injection_rules.yaml`
- `plugins/dev-kit/references/injection_rules.yaml`
- `plugins/ref-inject/templates/references/injection_rules.yaml`（新規プラグインに `/ref-inject:apply` で配布される雛形）

なお、ユーザの依頼にあった `plugins/workspace` には `injection_rules.yaml` は存在しないため対象外。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | claude-kit の injection_rules.yaml の英語コメントを日本語化 | - `plugins/claude-kit/references/injection_rules.yaml` |
| - | dev-kit の injection_rules.yaml の英語コメントを日本語化（コメント無しのため対象外） | - `plugins/dev-kit/references/injection_rules.yaml` |
| 済 | ref-inject のテンプレート injection_rules.yaml の英語コメントを日本語化 | - `plugins/ref-inject/templates/references/injection_rules.yaml` |
| 済 | 注入ルール構造（pattern / required / optional）の意味が日本語コメントから読み取れることを確認 | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/injection_rules.yaml` | 編集 | コメントを日本語化 | 構造・キー名は変更しない |
| `plugins/dev-kit/references/injection_rules.yaml` | 編集 | コメントを日本語化 | 構造・キー名は変更しない |
| `plugins/ref-inject/templates/references/injection_rules.yaml` | 編集 | テンプレート側コメントを日本語化 | `/ref-inject:apply` で配布される雛形 |

## テスト

このPRはコメントのみの変更でロジックを伴わないため、追加テストは無し。

## QA

未解決事項なし。

## 参考ドキュメント

- `plugins/ref-inject/templates/references/CLAUDE.md`: 注入ルールの仕組み解説
- `plugins/ref-inject/skills/apply/SKILL.md`: ref-inject 配布スキル

## 関連PR

| PR番号 | 概要 |
|---|---|
| #PR179 | injection 設定ファイル名にアンダースコアプレフィックスを付与 |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
