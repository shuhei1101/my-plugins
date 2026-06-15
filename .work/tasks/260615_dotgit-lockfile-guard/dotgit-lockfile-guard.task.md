# .git とロックファイルへの Edit/Write/削除を全面ブロック

> ブランチ: `feat/dotgit-lockfile-guard`

## 概要

work プラグインのガード強化。`.git/**` および主要パッケージマネージャの lock ファイルに対する
Claude からの編集・新規作成・削除を全面的にブロックする。

背景:
- `.git/**` は Git 内部状態であり、Claude が直接編集する正当な理由は存在しない。間違って書き換えると
  リポジトリが壊れる。読み取りのみ許可する。
- ロックファイル（`package-lock.json` 等）は本来パッケージマネージャ CLI が自動更新するもの。
  Claude が手で書き換えると依存解決の整合性が崩れる。

既存の `delete-guard.py` は `.git` / `.claude` 等への `rm` 系をブロック済だが、
- Edit / Write ツール経由の改変はガードされていない
- ロックファイルはガード対象に入っていない

ため、これらを補強する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | 未解決事項を `## QA` に記録する |
| 2 | - | `dotgit-lockfile-guard.py` を作成（PreToolUse Edit/Write 用） |
| 3 | - | `dotgit-lockfile-guard.md` を作成（ブロックメッセージ） |
| 4 | - | `delete-guard.py` にロックファイル名を追加（Bash 削除側） |
| 5 | - | `hooks.json` に新フックを登録 |
| 6 | - | バージョンアップ（plugin.json / marketplace.json） |
| 7 | - | `.work/notes/` の関連ノートを更新する |

## 仕様

ブロック対象パスは以下 2 系統。

`.git/**`:
- ワークツリー / メインリポジトリどちらの `.git` も対象
- Read は許可、Edit / Write / Bash 経由の削除は永久ブロック

ロックファイル（ファイル名末尾一致でマッチ）:

| No | ファイル名 | 由来 |
|---|---|---|
| 1 | `package-lock.json` | npm |
| 2 | `yarn.lock` | yarn |
| 3 | `pnpm-lock.yaml` | pnpm |
| 4 | `npm-shrinkwrap.json` | npm |
| 5 | `Cargo.lock` | cargo |
| 6 | `Gemfile.lock` | bundler |
| 7 | `Pipfile.lock` | pipenv |
| 8 | `poetry.lock` | poetry |
| 9 | `uv.lock` | uv |
| 10 | `composer.lock` | composer |
| 11 | `go.sum` | go modules |

ブロック方針: 永久ブロック（ワンタイムトークンなし）。
- env `WORK_GUARD=false` でも無効化しない（恒久ブロック）
- 既存 `delete-guard.py` と同じ方針を踏襲

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/hooks/dotgit-lockfile-guard.py` | 新規 | Edit / Write の対象パスを判定しブロック | |
| 2 | `plugins/work/hooks/dotgit-lockfile-guard.md` | 新規 | ブロック時のメッセージ本文 | |
| 3 | `plugins/work/hooks/delete-guard.py` | 編集 | ロックファイル名一覧をブロック対象に追加 | Bash `rm` 経路 |
| 4 | `plugins/work/hooks/hooks.json` | 編集 | 新フックを `Edit\|Write` matcher に登録 | |
| 5 | `plugins/work/.claude-plugin/plugin.json` | 編集 | version bump | |
| 6 | `.claude-plugin/marketplace.json` | 編集 | work エントリの version bump | |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `.git/HEAD` を Read できる | (未実施) | - |
| 2 | `.git/HEAD` を Edit するとブロック | (未実施) | - |
| 3 | 存在しない `.git/foo` を Write するとブロック | (未実施) | - |
| 4 | `package-lock.json` を Edit するとブロック | (未実施) | - |
| 5 | `uv.lock` を Write するとブロック | (未実施) | - |
| 6 | `Bash: rm package-lock.json` がブロックされる | (未実施) | - |
| 7 | 通常ファイル（`foo.py` 等）の Edit は通る | (未実施) | - |

## 参考リンク

- `plugins/work/hooks/delete-guard.py`: 既存削除ガード（同じ思想で実装する）
- `plugins/work/hooks/protected-branch-guard.py`: PreToolUse Edit/Write でブロックする既存例
- `plugins/work/hooks/hooks.json`: 登録先

## 関連ブランチ

| No | ブランチ | 概要 |
|---|---|---|
| 1 | `260614_削除ガードフック追加` 由来 | `.git`/`.claude` の Bash 削除ガードを最初に導入したタスク。今回はその拡張線。 |
