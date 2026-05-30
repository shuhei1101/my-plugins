# PR200 — dev-kit-html-rules-to-injection

## 概要

`html-implement` がプロジェクトの `.claude/rules/` に静的コピーしている HTML ルールテンプレ
`css-js-link.md` / `common-component-first.md` を廃止し、ref-inject と同じ injection hook 方式に
切り替える。

### 背景（PR182 から引き継ぎ）

PR182 で dev-kit:plugin-update スキルを追加したが、レビュー中にユーザーから:

- ルールテンプレを `.claude/rules/` に静的配布するのは正しくない
- これらは「CSS と JS のリンクを保つ」「共通コンポーネント先読み」という規約であり、
  プロジェクトファイルを Read/Edit したときに自動注入されるべき
- ref-inject の inject_references.py + injection_rules.yaml と同じ仕組みに乗せられる

との指摘があり、本 PR で対応する。

### 調査結果（PR182 セッションで実施済み）

- `dev-kit/references/_injection_rules.yaml`（PR179 でリネーム済）には既に `**/*.html` / `*.css` / `*.js`
  パターンで `html/principles.md` を `required` 注入するルールが存在する
- 同じパターンの `required` に `css-js-link.md` と `common-component-first.md` を追記するだけで移行可能
- `templates/html/rules/` ディレクトリは丸ごと不要になる

### 何をするか

1. `plugins/dev-kit/templates/html/rules/css-js-link.md`（+ `.jp.md`）を
   `plugins/dev-kit/references/html/css-js-link.md`（+ `.jp.md`）に移動
2. `plugins/dev-kit/templates/html/rules/common-component-first.md`（+ `.jp.md`）を
   `plugins/dev-kit/references/html/common-component-first.md`（+ `.jp.md`）に移動
3. `plugins/dev-kit/references/_index.yaml` / `_index.jp.yaml` に 2 ファイルを追加
4. `plugins/dev-kit/references/_injection_rules.yaml` の既存 html パターン 3 件
   （`**/*.html` / `**/*.css` / `**/*.js`）の `required` に 2 ファイルを追記
5. `plugins/dev-kit/templates/html/rules/` ディレクトリを削除
6. `plugins/dev-kit/skills/html-implement/SKILL.md`（+ `.jp.md`）からルールコピー手順（Step 7 付近）を削除
7. `plugins/dev-kit/skills/plugin-update/SKILL.md`（+ `.jp.md`）のステップ2（html-implement ルールテンプレ再コピー）を削除し、ステップ番号を繰り上げ
8. `plugins/dev-kit` を MINOR bump（v4.3.0 → v4.4.0）
9. `plugins/dev-kit/CLAUDE.md`（+ `.jp.md`）の Changelog 表に v4.4.0 行を追加

### 実施条件

即時実施可（PR182 マージ済）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| x | 2 ルールファイルを templates/html/rules → references/html へ移動 | - `plugins/dev-kit/references/html/css-js-link.md`(+ jp)<br>- `plugins/dev-kit/references/html/common-component-first.md`(+ jp) |
| x | references/_index.yaml と _index.jp.yaml にエントリ追加 | - `plugins/dev-kit/references/_index.yaml`<br>- `plugins/dev-kit/references/_index.jp.yaml` |
| x | references/_injection_rules.yaml の html パターン 3 件に required 追記 | - `plugins/dev-kit/references/_injection_rules.yaml` |
| x | templates/html/rules/ ディレクトリを削除 | - `plugins/dev-kit/templates/html/rules/`（削除） |
| x | html-implement SKILL からルールコピー手順を削除 | - `plugins/dev-kit/skills/html-implement/SKILL.md`(+ jp) |
| x | plugin-update SKILL のステップ2 を削除しステップ番号を繰り上げ | - `plugins/dev-kit/skills/plugin-update/SKILL.md`(+ jp) |
| x | dev-kit を MINOR bump | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| x | CLAUDE.md Changelog 表に v4.4.0 追記 | - `plugins/dev-kit/CLAUDE.md`(+ jp) |
| x | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証: 既存 .html/.css/.js ファイルを Read してルール内容が注入されることを目視確認） | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/ref-inject/skills/apply/SKILL.md` — injection hook 機構の参照
- `plugins/dev-kit/references/_injection_rules.yaml` — 既存 html パターン定義
- `plugins/dev-kit/hooks/scripts/inject_references.py` — injection フック実装

## 関連PR

| PR番号 | 概要 |
|---|---|
| #182 | dev-kit:plugin-update スキル追加（本 PR の発端） |
| #179 | references/ メタ YAML のアンダースコア接頭辞リネーム（本 PR が触る `_injection_rules.yaml` の名前変更元） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
