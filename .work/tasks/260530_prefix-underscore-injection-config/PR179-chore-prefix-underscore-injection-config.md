# PR179 — prefix-underscore-injection-config

## 概要

`ref-inject` / `dev-kit` / `claude-kit` の `references/` 配下にある `index.yaml` / `index.jp.yaml` / `injection_rules.yaml` を、それぞれ `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` にリネームする。アンダースコア接頭辞を付けることで、各 plugin の references ファイル一覧の最上部にこれらメタ系ファイルが固定され、視認性が上がる。

依存する Python フック（`hooks/scripts/inject_references.py`）、Jinja2 メッセージテンプレート、`ref-inject:apply` スキル、各プラグインの CLAUDE.md、claude-kit/references の `CLAUDE.md` / `hooks.md` / `environment.md`、`kit-hooks-index-sync` ルール、`workspace:issue-scan` スキルも追従。

合わせて、PR166 で `dev-kit` に統合されて存在しない `py-kit` / `next-kit` / `html-kit` を、現役の `*-kit` 例として並列に列挙していた箇所も `dev-kit` / `claude-kit` に整理。

**master 反映**: 実装後に master が PR168（タスクドキュメント単一ファイル化）／PR171（plugin CLAUDE.md 標準化）／PR178（markdown-table reference）／PR180（hooks/scripts/ 配置）／PR183（dev-kit ブレース展開）等で大幅に進行していたため、`git merge master` で取り込み、以下のように再適用:

- 旧 `PR179/TODO.md` + `QA.md` 構造 → 新単一ファイル構造（このファイル）へ移行
- `changelogs/v3.36.0.md` / `v4.1.0.md` / `v1.4.0.md` の add/add 衝突は master 版を保持し、自分の変更点は新バージョン番号（`v3.41.0.md` / `v4.2.0.md` / `v1.5.0.md`）で別ファイル化
- 各 plugin を master の最新バージョンより上に再 bump（claude-kit 3.40.0 → 3.41.0、dev-kit 4.1.0 → 4.2.0、ref-inject 1.4.0 → 1.5.0、workspace 2.46.0 → 2.46.1）
- master の `hooks/inject_references.py` → `hooks/scripts/inject_references.py` 移動（PR180）に追従し、内容衝突を統合解消

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `ref-inject/templates/references/` の 3 ファイルをリネーム | `plugins/ref-inject/templates/references/_{index,index.jp,injection_rules}.yaml` |
| 済 | `dev-kit/references/` の 3 ファイルをリネーム | `plugins/dev-kit/references/_{index,index.jp,injection_rules}.yaml` |
| 済 | `claude-kit/references/` の 3 ファイルをリネーム | `plugins/claude-kit/references/_{index,index.jp,injection_rules}.yaml` |
| 済 | 各 `inject_references.py` のファイル名参照を更新 | `plugins/{ref-inject/templates,dev-kit,claude-kit}/hooks/scripts/inject_references.py` |
| 済 | `injection.{md,jp.md}.j2` テンプレートのメッセージを更新 | `plugins/{ref-inject/templates,dev-kit,claude-kit}/hooks/templates/injection.*.j2` |
| 済 | `ref-inject:apply` スキルのファイル名参照を更新 | `plugins/ref-inject/skills/apply/SKILL.md` (+ `.jp.md`) |
| 済 | 各プラグインの `CLAUDE.md` の参照名を更新 | `plugins/{ref-inject,dev-kit,claude-kit}/CLAUDE.md` (+ `.jp.md`) |
| 済 | `claude-kit/references/{CLAUDE,hooks}.md` のドキュメント追従 | `plugins/claude-kit/references/{CLAUDE,hooks}.md` (+ `.jp.md`) |
| 済 | `kit-hooks-index-sync` ルールの `paths:` と本文を更新 | `.claude/rules/feature/kit-hooks-index-sync.md` (+ `rules-jp/`) |
| 済 | 旧 `py-kit` / `next-kit` / `html-kit` への並列言及を `dev-kit` / `claude-kit` に整理 | `plugins/claude-kit/CLAUDE.md` (+ JP), `claude-kit/references/{environment,hooks}.md` (+ JP), `plugins/ref-inject/CLAUDE.md` (+ JP), `plugins/workspace/skills/issue-scan/SKILL.md` (+ JP) |
| 済 | `workspace:issue-scan` の `injection_rules.yaml` 参照も `_injection_rules.yaml` に追従 | `plugins/workspace/skills/issue-scan/SKILL.md` (+ `.jp.md`) |
| 済 | バージョン bump + `marketplace.json` 同期 + changelog 作成 | `plugins/{ref-inject,dev-kit,claude-kit,workspace}/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `plugins/*/changelogs/v*.md` |
| 済 | スモークテスト: claude-kit / dev-kit のフックを実走（YAML パース確認） | - |
| 済 | `git merge master` で master 取り込み・衝突解消 | 各種 |
| 済 | 旧 task doc 構造 (`PR179/TODO.md` + `QA.md`) を新単一ファイル構造に移行 | このファイル |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/_index.yaml` | 編集（リネーム） | 旧 `index.yaml` から | アンダースコア接頭辞でファイル一覧の最上部に固定 |
| `plugins/claude-kit/references/_index.jp.yaml` | 編集（リネーム） | 旧 `index.jp.yaml` から | 同上 |
| `plugins/claude-kit/references/_injection_rules.yaml` | 編集（リネーム） | 旧 `injection_rules.yaml` から | 同上 |
| `plugins/dev-kit/references/_index.yaml` | 編集（リネーム） | 旧 `index.yaml` から | 同上 |
| `plugins/dev-kit/references/_index.jp.yaml` | 編集（リネーム） | 旧 `index.jp.yaml` から | 同上 |
| `plugins/dev-kit/references/_injection_rules.yaml` | 編集（リネーム） | 旧 `injection_rules.yaml` から | 同上 |
| `plugins/ref-inject/templates/references/_index.yaml` | 編集（リネーム） | 旧 `index.yaml` から | テンプレ |
| `plugins/ref-inject/templates/references/_index.jp.yaml` | 編集（リネーム） | 旧 `index.jp.yaml` から | テンプレ |
| `plugins/ref-inject/templates/references/_injection_rules.yaml` | 編集（リネーム） | 旧 `injection_rules.yaml` から | テンプレ |
| `plugins/claude-kit/hooks/scripts/inject_references.py` | 編集 | 参照ファイル名を `_*.yaml` に更新 | master の hooks/scripts/ 移動 (PR180) に追従 |
| `plugins/dev-kit/hooks/scripts/inject_references.py` | 編集 | 同上 | 同上 |
| `plugins/ref-inject/templates/hooks/scripts/inject_references.py` | 編集 | 同上 | 同上 |
| `plugins/claude-kit/hooks/templates/injection.{md,jp.md}.j2` | 編集 | 注入メッセージ内の参照名を更新 | - |
| `plugins/dev-kit/hooks/templates/injection.{md,jp.md}.j2` | 編集 | 同上 | - |
| `plugins/ref-inject/templates/hooks/templates/injection.{md,jp.md}.j2` | 編集 | 同上 | - |
| `plugins/ref-inject/skills/apply/SKILL.md` (+ `.jp.md`) | 編集 | ファイル一覧と手順記述を更新 | - |
| `plugins/ref-inject/CLAUDE.md` (+ `.jp.md`) | 編集 | テンプレートツリーの記述 + 並列 plugin 名を更新 | - |
| `plugins/ref-inject/templates/references/CLAUDE.md` (+ `.jp.md`) | 編集 | 参照名を更新 | - |
| `plugins/dev-kit/CLAUDE.md` (+ `.jp.md`) | 編集 | references ツリーの記述を更新 | - |
| `plugins/claude-kit/CLAUDE.md` (+ `.jp.md`) | 編集 | 参照名と並列 plugin 名を更新 | - |
| `plugins/claude-kit/references/CLAUDE.md` (+ `.jp.md`) | 編集 | 構造説明を更新 | - |
| `plugins/claude-kit/references/hooks.md` (+ `.jp.md`) | 編集 | ref-inject 仕様 + 代表的採用例の plugin 名を更新 | - |
| `plugins/claude-kit/references/environment.md` (+ `.jp.md`) | 編集 | 例示の plugin 名を更新 | - |
| `plugins/workspace/skills/issue-scan/SKILL.md` (+ `.jp.md`) | 編集 | 前提条件と `_injection_rules.yaml` 参照に追従 | - |
| `.claude/rules/feature/kit-hooks-index-sync.md` | 編集 | `paths:` と本文の参照名を更新 | - |
| `.claude/rules-jp/feature/kit-hooks-index-sync.md` | 編集 | 同上（JP ミラー） | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | 3.40.0 → 3.41.0 | - |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 4.1.0 → 4.2.0 | - |
| `plugins/ref-inject/.claude-plugin/plugin.json` | 編集 | 1.4.0 → 1.5.0 | - |
| `plugins/workspace/.claude-plugin/plugin.json` | 編集 | 2.46.0 → 2.46.1 | issue-scan ドキュメント修正のみ |
| `.claude-plugin/marketplace.json` | 編集 | 4 plugin のバージョン同期 | - |
| `plugins/claude-kit/changelogs/v3.41.0.md` | 新規 | PR179 変更点の changelog | - |
| `plugins/dev-kit/changelogs/v4.2.0.md` | 新規 | 同上 | - |
| `plugins/ref-inject/changelogs/v1.5.0.md` | 新規 | 同上 | - |
| `plugins/workspace/changelogs/v2.46.1.md` | 新規 | 同上 | - |

## テスト

このリファクタは Markdown / YAML / Python のファイル名変更とドキュメント追従が中心で、ランタイムの自動テストは追加していない。代わりに以下を手動で確認:

| ファイル名 | 内容 | 補足 |
|---|---|---|
| - | `python3 -c "import yaml; yaml.safe_load(open(f))"` で 9 個のリネーム後 YAML が全てパース成功 | - |
| - | `claude-kit` / `dev-kit` の `hooks/scripts/inject_references.py` をダミー stdin で起動し exit 0 を確認 | - |
| - | `git merge master` 後、conflict marker (`<<<<<<<` / `=======` / `>>>>>>>`) が全てのファイルから消えていることを `grep -rn` で確認 | - |

## QA

未決定事項なし。

## 参考ドキュメント

- `plugins/ref-inject/CLAUDE.md`: ref-inject の責務とテンプレ構成
- `plugins/claude-kit/references/hooks.md`: ref-inject 注入設計の仕様
- `.claude/rules/feature/kit-hooks-index-sync.md`: kit plugins の同期ルール

## 関連PR

| PR番号 | 概要 |
|---|---|
| #PR166 | merge-language-plugins-into-dev-kit（py-kit / next-kit / html-kit を dev-kit に統合） |
| #PR168 | refactor-task-doc-structure（タスク文書を単一ファイル化） |
| #PR171 | add-plugin-claude-md-standard（changelogs/ + plugin CLAUDE.md 標準化） |
| #PR180 | split-hook-inline-python-to-scripts（hooks/scripts/ 配置） |

## 次PR候補

なし
