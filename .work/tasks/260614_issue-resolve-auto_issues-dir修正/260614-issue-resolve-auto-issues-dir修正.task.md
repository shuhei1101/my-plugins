# issue-resolve-auto の issues_dir パス未指定バグ修正

> ブランチ: `fix/issue-resolve-auto-issues-dir`

## 概要

`issue-resolve-auto` スキル実行時に `.work/issues/progress/` 配下に `closed/` フォルダと `_index.archive.yaml` が誤作成されるバグを修正する。

原因は2つ：
1. SKILL.md Step 2 で `issue_close` MCPツールの `issues_dir` パスが未明記のため、エージェントが `progress/` フォルダのパスを渡してしまっていた
2. `protected-branch-guard.py` の `resolve_check_dir` で新規ファイルの親ディレクトリが未存在の場合 `cwd`（master）にフォールバックしてしまい、ワークツリー内でも新規フォルダ配下への Write がブロックされていた

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `SKILL.md` Step 2 の `issue_close` 呼び出しに `issues_dir` の絶対パス指定を明記 |
| 2 | 済 | `SKILL.md` Step 4 の `issue_set_status` の `issues_dir` にも絶対パス明記 |
| 3 | 済 | `protected-branch-guard.py` の `resolve_check_dir` を祖先辿りロジックに修正 |
| 4 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `plugins/work/skills/issue-resolve-auto/SKILL.md` | 編集 | Step 2・4 で `issues_dir` に絶対パスを指定するよう明記 |
| 2 | `plugins/work/hooks/protected-branch-guard.py` | 編集 | `resolve_check_dir` を親ディレクトリ未存在時に祖先を辿るロジックに変更 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | ワークツリー内で新規フォルダ配下へのファイル作成がブロックされないこと | task.md 作成成功 | ✅ |

## 参考リンク

- `plugins/work/skills/issue-resolve-auto/SKILL.md`: issue-resolve-auto スキル定義
- `plugins/work/hooks/protected-branch-guard.py`: 保護ブランチガードフック
