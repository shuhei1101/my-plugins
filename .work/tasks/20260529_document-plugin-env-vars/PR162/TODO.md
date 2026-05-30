# PR162 — document-plugin-env-vars

## 概要

Claude Code プラグインで環境変数を使う方法（`settings.json` の `env` ブロックで設定 → フック/スクリプトが
`os.environ` で読む）を references に明文化する。実例は py-kit / claude-kit / next-kit の注入フックが既に
持つ `{PREFIX}_INJECTION_TTL` / `{PREFIX}_INJECTION_LANG`。

置き場所: env は settings.json で設定しフックが読む構成なので、オーサリングガイドとしては **hooks.md** が正本
（hooks.json / settings.json 編集時に注入される）。あわせて「プラグインは自分の env 変数を自身の CLAUDE.md に
記載する」慣習を plugin-structure.md に一言追記。

### 実施条件

即時実施可（PR161 マージ済み。claude-kit は現在 v3.32.0 = PR160 反映済み）。

### 関連PR

| PR番号 | 概要 |
|---|---|
| #159 | claude-kit を ref-inject 注入へ移行（references を整備した本拠） |
| #161 | mark-generated reference 化 + フック削減（references 整備の続き） |
| #160 | ref-inject 二層キャッシュ + claude-kit 同期（env `{PREFIX}_INJECTION_TTL` 等の実例元） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（無し） | - `PR162/QA.md` |
| 済 | env ガイドを専用 reference `environment.md`(+jp) に新設（impl-review でのユーザー指摘を反映。env は hooks 固有でなく共通の関心事＝実行コード hooks/scripts のみが使う）。index.yaml(+jp) 追加 + injection_rules で hooks.json/settings.json に紐付け | - `plugins/claude-kit/references/environment.md` (+jp), `index.yaml`(+jp), `injection_rules.yaml` |
| 済 | hooks.md(+jp) の env 節を environment.md への短いポインタに | - `plugins/claude-kit/references/hooks.md` (+jp) |
| 済 | plugin-structure.md(+jp) に「env 変数はプラグイン自身の CLAUDE.md に記載」慣習を追記（ポインタは environment.md） | - `plugins/claude-kit/references/plugin-structure.md` (+jp) |
| 済 | claude-kit 版バンプ(3.33.0) + marketplace 同期 + changelog | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `changelogs/v3.33.0.md` |
| 済 | environment.md を全 claude アーティファクトに共通注入（ユーザー指示）。hooks.json/settings.json は required、他の全 authoring パターンは optional（ポインタ）。matcher は既存の Edit/Write/MultiEdit/Read 維持 | - `plugins/claude-kit/references/injection_rules.yaml` |
| 済 | 検証（orphan/YAML/JSON/注入スモークテスト） | - |

## 参考ドキュメント

- `plugins/claude-kit/hooks/inject_references.py`: env 利用の実装例（`{PREFIX}_INJECTION_TTL` / `_INJECTION_LANG`）
- `plugins/ref-inject/CLAUDE.md`: env 上書きの記述（`settings.json` `env`）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {実装中に判明した課題があれば追記} | - | - |
