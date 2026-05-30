# docs/claude-kit-jinja2-authoring-rules

> 内部 ID: 222（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`plugins/claude-kit/references/jinja2/` フォルダを新設し、Jinja2 テンプレート
（`hooks/templates/*.j2` 等）を作成・編集する際の注意事項をリファレンスとして
ドキュメント化する。`_injection_rules.yaml` に `**/templates/*.j2` 等のパスマッチを
追加して、テンプレート編集時に自動注入されるようにする。

### 引き継ぎ背景（PR201 から）

PR201 で `injection.md.j2` / `injection.jp.md.j2` を編集した際に
**3 つの Markdown レンダリングバグ** に遭遇した：

1. **`{% if %}{% endif %}` + `trim_blocks=True` の改行消費**
   - `{% endif %}` 直後の `\n` が消され、heading と paragraph が密着して
     Markdown のスペーシングが壊れる
   - 対策: if ブロックの内側 / 外側に blank line を明示

2. **`{% if optional %}` 直後 `---` の setext heading バグ**
   - `{% endfor %}{% endif %}{% if optional %}` の連続タグが改行を全消費し、
     前コンテンツ直後に `---` が来て setext heading に化ける
   - 対策: optional ブロックの内側に blank line を追加

3. **`## {{ ref.path }} — {{ ref.description }}` のレンダラー混乱**
   - Handlebars 系レンダラーが `}}` を template 終端として誤認識し、
     後続コンテンツが壊れる
   - 対策: `}}` 末尾に `<!-- -->` を追加してパース連鎖を切る

これらは将来の Jinja2 テンプレート作成時に何度も踏みかねないため、
リファレンス化して **テンプレート編集時に自動注入** されるようにする。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する（該当なし） | - |
| 済 | `.work/notes/` の関連ノートを確認・更新する（既存ノートなし → 本 PR の changelog で代替） | - |
| 済 | `references/jinja2/templates.md` (英語) と `.jp.md` を作成し、上記3パターン + その他の注意事項を記述する | - `plugins/claude-kit/references/jinja2/templates.md`<br>- `plugins/claude-kit/references/jinja2/templates.jp.md` |
| 済 | `_index.yaml` / `_index.jp.yaml` に新リファレンスを登録する | - `plugins/claude-kit/references/_index.yaml`<br>- `plugins/claude-kit/references/_index.jp.yaml` |
| 済 | `_injection_rules.yaml` に `**/hooks/templates/*.j2` パスを追加し新リファレンスを紐付ける | - `plugins/claude-kit/references/_injection_rules.yaml` |
| 済 | バージョンをバンプする（3.44.0 → 3.45.0） | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | CLAUDE.md の Changelog を更新する／changelogs/v3.45.0.md を作成する | - `plugins/claude-kit/CLAUDE.md`<br>- `plugins/claude-kit/CLAUDE.jp.md`<br>- `plugins/claude-kit/changelogs/v3.45.0.md` |
| 済 | ルール・CLAUDE.md を更新する（変更なし — `.claude/rules/` 配下に該当無し） | - |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/jinja2/templates.md` | 新規 | Markdown を出力する Jinja2 テンプレートのオーサリングルール（trim_blocks、setext 見出しバグ、`}}` + Handlebars 衝突、チェックリスト） | EN 正本 |
| `plugins/claude-kit/references/jinja2/templates.jp.md` | 新規 | 上記の JP ミラー | - |
| `plugins/claude-kit/references/_index.yaml` | 編集 | `jinja2/templates.md` エントリ追加 | - |
| `plugins/claude-kit/references/_index.jp.yaml` | 編集 | 上記の JP ミラー | - |
| `plugins/claude-kit/references/_injection_rules.yaml` | 編集 | `**/hooks/templates/*.j2` → `jinja2/templates.md` ルール追加 | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | version 3.44.0 → 3.45.0 | - |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit version 3.44.0 → 3.45.0 | - |
| `plugins/claude-kit/CLAUDE.md` | 編集 | Changelog テーブルに 3.45.0 行を追加 | - |
| `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 上記の JP ミラー | - |
| `plugins/claude-kit/changelogs/v3.45.0.md` | 新規 | 3.45.0 の changelog 詳細 | - |

## テスト

上記実装に伴って追加・変更したテストファイル。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (テストなし) | - | - | - |

## QA

QA 事項なし。

## 参考ドキュメント

- `.work/notes/Jinja2テンプレート執筆ルール.md`: 本 PR の設計ノート（バグパターンの背景と対処）
- `plugins/claude-kit/hooks/templates/injection.md.j2`: PR201 で修正した実例
- `plugins/claude-kit/hooks/templates/injection.jp.md.j2`: 同上 JP 版
- `plugins/claude-kit/hooks/scripts/inject_references.py`: `trim_blocks=True`, `lstrip_blocks=True` の設定箇所
- `plugins/claude-kit/references/_injection_rules.yaml`: パスマッチ追加先

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| PR201 (merged) | テンプレートレンダリングバグを実装で修正した先行ブランチ |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
