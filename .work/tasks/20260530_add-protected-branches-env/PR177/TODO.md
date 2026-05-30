# PR177 — add-protected-branches-env

## 概要

`workspace/hooks/scripts/master-commit-guard.py` の保護ブランチハードコード（`PROTECTED_BRANCHES = ("master", "main", "develop")`）を env var `WORKSPACE_PROTECTED_BRANCHES`（カンマ区切り、例: `master,main,develop`）で上書き可能にする。

### 背景（PR169 からの引き継ぎ）

- PR169 で `guard-kit` を `workspace` に統合し、push/merge 検出ガード（`git-guard`）を `WORKSPACE_GUARD` env トグルで起動可否切替できるようにした
- ユーザーから「ガード対象ブランチ名も env で指定したい。配列みたいに、カンマ区切りで」との依頼。`master` だけ守りたい人もいれば `release/*` を追加したい人もいる
- これは `workspace` 内のもう 1 つの保護フック `master-commit-guard`（保護ブランチ上での直接コミット阻止）の話で、`git-guard`（push/merge 阻止）の話ではない
- 同じ「env で挙動を切替可能にする」パターン（PR163 `WORKSPACE_USE_WORKTREE` / PR164 各種 / PR169 `WORKSPACE_GUARD`）の続編

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR169 | guard-kit を workspace に統合し `WORKSPACE_GUARD` 追加（本 PR の動機元） |
| #PR164 | 常時発火フック/ステップに env トグル一覧を追加（同パターン） |
| #PR163 | `WORKSPACE_USE_WORKTREE` env トグル（同パターン） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（未決定事項なし） | - `.work/tasks/.../PR177/QA.md` |
| 済 | `.work/notes/add-protected-branches-env.md` を作成（pr-handoff で作成済み） | - `.work/notes/add-protected-branches-env.md` |
| 済 | `master-commit-guard.py` で `os.environ.get('WORKSPACE_PROTECTED_BRANCHES', 'master,main,develop')` をカンマ区切りでパースして `PROTECTED_BRANCHES` を構築するように変更（空文字除去・前後 strip） | - `plugins/workspace/hooks/scripts/master-commit-guard.py` |
| 済 | `plugin.json` / `marketplace.json` のバージョン bump（2.40.0 → 2.41.0） | - `plugins/workspace/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |
| 済 | description に `WORKSPACE_PROTECTED_BRANCHES` を追記 | - 同上 |
| 済 | changelog 追加 | - `plugins/workspace/changelogs/v2.41.0.md` |
| 済 | `glossary.md` に `WORKSPACE_PROTECTED_BRANCHES` エントリ追加、`env トグル一覧 (PR164)` に追記 | - `.claude/rules/core/glossary.md` |
| 済 | JP ミラー同期（rules-jp/core/glossary.md） | - `.claude/rules-jp/core/glossary.md` |
| 済 | パース動作確認（default/single/spaces/empty/weird の 5 パターン全 OK） | - 手動確認 |

## 参考ドキュメント

- `.work/notes/add-protected-branches-env.md`: 設計メモ（パース仕様・末尾空文字の扱い等）
- `.work/notes/integrate-guard-kit-into-workspace.md`: PR169 の env トグル設計（同パターン）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
