# PR180 — split-hook-inline-python-to-scripts

## 概要

`hooks.json` 内にインラインで書かれた `python -c "..."` スクリプトを、各プラグインの `hooks/scripts/` フォルダ配下の `.py` ファイルに切り出す。**既存 `hooks/*.py` も含めて全プラグインを `hooks/scripts/` 配下に統一**（QA-001 解決）。共通処理（stdin 読み取り、env truthy 判定、`stop_hook_active` チェック、once-per-session トークン管理、`decision:block` JSON 出力）はプラグイン内に閉じた `hooks/scripts/_common.py` に集約（QA-002 解決）。ref-inject の templates 配下にも雛形を入れて、新規プラグインが最初から切り出し済み構造になるようにした（QA-003 解決）。

`master` 進行（PR168/PR171/PR178/PR181）の取り込みで:
- claude-kit の PreCompact フック・pre-compact プロンプト・conversation-to-claude スキルが PR181 で削除されたため、PR180 で作成していた `pre_compact.py` および hooks.json の PreCompact エントリは破棄
- `.claude/references/incidents/` と `.claude/rules/core/{glossary,incidents}.md` が PR168/171 で大規模整理され削除されたため、PR180 で追加していた split-hook-inline-python-to-scripts glossary エントリと incident 言及は受け入れ削除
- バージョン衝突: claude-kit を 3.36.0 → **3.40.0**、workspace を 2.44.0 → **2.46.0** に再バンプ
- changelogs/v3.36.0.md は master のプラグインオーサリングガイド変更で占有されていたため、私のものは v3.40.0.md に再作成

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | workspace `hooks/scripts/_common.py` を作成し共通関数を実装 | - `plugins/workspace/hooks/scripts/_common.py` |
| 済 | workspace `hooks/scripts/stop.py` を作成（インライン Stop フックを移行） | - `plugins/workspace/hooks/scripts/stop.py` |
| 済 | workspace `hooks/hooks.json` の Stop エントリを `scripts/stop.py` 呼び出しに変更 | - `plugins/workspace/hooks/hooks.json` |
| 済 | claude-kit `hooks/inject_references.py` を `hooks/scripts/` へ移動・parents[2] 化 | - `plugins/claude-kit/hooks/scripts/inject_references.py` |
| 済 | claude-kit `hooks/scripts/_common.py` を作成 | - `plugins/claude-kit/hooks/scripts/_common.py` |
| 済 | claude-kit `hooks/hooks.json` の全エントリパスを `hooks/scripts/...` に更新 | - `plugins/claude-kit/hooks/hooks.json` |
| 済 | dev-kit `hooks/inject_references.py` と `ts_check.py` を `hooks/scripts/` へ移動・parents[2] 化 | - `plugins/dev-kit/hooks/scripts/{inject_references,ts_check}.py` |
| 済 | dev-kit `hooks/scripts/_common.py` を作成 | - `plugins/dev-kit/hooks/scripts/_common.py` |
| 済 | dev-kit `hooks/scripts/yaml_skill_dispatch.py` を作成（インライン yaml-skill-dispatch を移行） | - `plugins/dev-kit/hooks/scripts/yaml_skill_dispatch.py` |
| 済 | dev-kit `hooks/hooks.json` の全エントリパスを `hooks/scripts/...` に更新 | - `plugins/dev-kit/hooks/hooks.json` |
| 済 | ref-inject `templates/hooks/inject_references.py` を `templates/hooks/scripts/` へ移動 | - `plugins/ref-inject/templates/hooks/scripts/inject_references.py` |
| 済 | ref-inject `templates/hooks/scripts/_common.py` 雛形を新規追加（プレースホルダ入り） | - `plugins/ref-inject/templates/hooks/scripts/_common.py` |
| 済 | ref-inject `templates/hooks/hooks.json` のパスを `hooks/scripts/...` に更新 | - `plugins/ref-inject/templates/hooks/hooks.json` |
| 済 | ref-inject `skills/apply/SKILL.md` (+ jp) の template→destination 表を更新 | - `plugins/ref-inject/skills/apply/SKILL.md`, `SKILL.jp.md` |
| 済 | `kit-hooks-index-sync` ルールの `paths:` と Related Files 表に `_common.py` を追加 | - `.claude/rules/feature/kit-hooks-index-sync.md`, `.claude/rules-jp/feature/kit-hooks-index-sync.md` |
| 済 | 各プラグインの CLAUDE.md / references の hooks パス記載を更新 | - `plugins/{claude-kit,dev-kit,ref-inject}/{CLAUDE,references/*}.{md,jp.md}` |
| 済 | master 取り込み：PR181 の PreCompact・conversation-to-claude 削除を反映、PR180 で作った pre_compact.py を破棄、CLAUDE.md/.jp.md を master 側の「single hook」記載に統合 | - `plugins/claude-kit/{CLAUDE.md,CLAUDE.jp.md,hooks/hooks.json}` |
| 済 | master 取り込み：incidents/ と core/{glossary,incidents}.md の削除を受け入れ | - `.claude/{references/incidents,rules/core,rules-jp/core}/*` |
| 済 | バージョン再バンプ（衝突解決後） | - claude-kit 3.40.0 / workspace 2.46.0 / dev-kit 4.1.0 / ref-inject 1.4.0 |
| 済 | changelog 整理（v3.36.0.md → v3.40.0.md / v2.44.0.md → v2.46.0.md） | - `plugins/{claude-kit,workspace}/changelogs/*` |
| 済 | PR180 ドキュメントを新形式（`{branch-hyphenated}.md` 1ファイル）に移行 | - `.work/tasks/20260530_split-hook-inline-python-to-scripts/PR180-refactor-split-hook-inline-python-to-scripts.md` |
| 済 | 孤児チェック・hooks.json JSON validity チェック・全 script import チェック | - 自動 |
| 済 | フック動作確認（`/reload-plugins` で 6 プラグイン・18 フック再ロード成功、Stop フックも本セッションで発火確認） | - 動作確認 |

## QA

すべて解決済み（PR180 ドキュメント新形式移行時に統合）。

### QA-001: フォルダ配置の統一範囲 ✅ 解決

**判断（2026-05-30 確定）**: 選択肢 B 採用 — 既存ファイル（`inject_references.py` / `ts_check.py`）も含めて全プラグイン `hooks/scripts/` 配下に統一する。

合わせて以下も更新:
- 各プラグインの `hooks/hooks.json` の `args` パスを `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/{name}.py` に変更
- `kit-hooks-index-sync` ルールの `paths:` グロブと Related Files 表
- 各プラグインの CLAUDE.md / references 内のパス記載
- `ref-inject/skills/apply/SKILL.md` の template→destination 表

歴史的記録（changelogs / incidents）は変更しない。

### QA-002: `_common.py` に切り出す関数の範囲 ✅ 解決

**判断（2026-05-30 確定）**: 選択肢 A 採用 — 5 パターン全部切り出し。

```python
def read_hook_input() -> dict: ...
def env_truthy(name: str, default: bool = True) -> bool: ...
def exit_if_stop_loop(input_data: dict) -> None: ...
def already_dispatched_this_session(tag: str, session_id: str) -> bool: ...
def emit_block_reason(prompt_path: Path) -> None: ...
```

各プラグイン内に閉じる（プラグイン間共通化はしない — インシデント `premature-cross-plugin-centralization`）。各プラグインの `_common.py` は意図的にコピーになる。

### QA-003: ref-inject templates 配下への対応 ✅ 解決

**判断（2026-05-30 確定）**: 選択肢 B 採用 — ref-inject の `templates/hooks/scripts/_common.py` に雛形を入れる（プレースホルダ `__ENV_PREFIX__` 入り）。合わせて `templates/hooks/inject_references.py` も `templates/hooks/scripts/inject_references.py` に移動。

## 参考ドキュメント

- `.work/notes/split-hook-inline-python-to-scripts.md`: 本 PR の設計メモ

## 関連PR

| PR番号 | 概要 |
|---|---|
| PR177 | add-protected-branches-env — workspace の Stop フックインライン Python の直前修正 |
| PR181 | remove-conversation-to-claude — claude-kit の PreCompact / conversation-to-claude 削除（master 取り込みで反映） |
| PR168 | refactor-task-doc-structure — PR ドキュメントを 1 ファイル形式に変更（master 取り込みで反映） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | （現時点で次PR候補なし） | - |
