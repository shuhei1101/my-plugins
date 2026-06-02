# already_dispatched_this_session TOCTOU修正

> ブランチ: `fix/toctou-already-dispatched`

## 概要

`_common.py` の `already_dispatched_this_session()` が `exists()` 確認と `touch()` の間に TOCTOU 競合を持ち、並列実行時に「セッション 1 回だけ発火」の保証が破れる。`flag.open("x")` による排他的ファイル生成に置き換えることで原子的な判定を保証する。

対象は 4 つの `_common.py` コピー（テンプレート + 3 キット）。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | 未解決事項を `## QA` に記録する |
| 2 | - | `plugins/ref-inject/templates/hooks/scripts/_common.py` の `already_dispatched_this_session()` を原子的生成に修正 |
| 3 | - | `plugins/claude-kit/hooks/scripts/_common.py` を同様に修正 |
| 4 | - | `plugins/dev-kit/hooks/scripts/_common.py` を同様に修正 |
| 5 | - | `plugins/work/hooks/scripts/_common.py` を同様に修正 |
| 6 | - | 4 コピーの関数内容が一致することを確認 |
| 7 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/ref-inject/templates/hooks/scripts/_common.py` | 編集 | `already_dispatched_this_session()` を `open("x")` 排他生成に変更 | テンプレート（先に修正） |
| 2 | `plugins/claude-kit/hooks/scripts/_common.py` | 編集 | 同上 | キット版 |
| 3 | `plugins/dev-kit/hooks/scripts/_common.py` | 編集 | 同上 | キット版 |
| 4 | `plugins/work/hooks/scripts/_common.py` | 編集 | 同上 | キット版 |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | 4 コピーの `already_dispatched_this_session()` が `open("x")` を使用していること | (未実施) | - |
| 2 | 差分が `already_dispatched_this_session()` 関数のみに限定されていること | (未実施) | - |

## QA

（解決済み、記録なし）

## 参考ドキュメント

- （最終コミット時に追記）

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-094 | `already_dispatched_this_session()` の check-then-touch が TOCTOU 競合を持つ | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | fix/read-hook-input-fail-open | 同じ `_common.py` の `read_hook_input()` を修正（未マージ） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | git-guard/master-commit-guard TOCTOU修正 | ISSUE-096: git-guard.py / master-commit-guard.py の check-then-touch も同様に修正 | 即時実施可 |
