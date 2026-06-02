# ISSUE-095: `inject_references.py` が全フック発火ごとに `~/.claude/tokens/` を全件スキャンする

**作成日**: 2026-05-31

## 概要

`inject_references.py` の `_cleanup_expired()` がフック発火のたびに無条件で実行され、トークンディレクトリ全件の read/parse/write が走るため、体感レイテンシの原因になりうる。

## 背景

このフックは `PreToolUse(Edit | Write | MultiEdit | Read)` で発火するため、作業中に Claude が編集・読み込みを行うたびに毎回スキャンが動く。特に WSL2 上の Windows ファイルシステム（`/mnt/c/...`）では I/O が著しく遅く、コストが直接レイテンシとして現れる。

## 現状

`inject_references.py`（work / claude-kit / dev-kit / ref-inject テンプレート）の `_cleanup_expired()` は、**フックが発火するたびに毎回**呼ばれる:

```python
now = time.time()
_cleanup_expired(token_dir, now, yaml)  # ← 無条件に全セッションのトークンを走査
```

`_cleanup_expired()` の内部では `token_dir.glob("*.yaml")` で全セッションファイルを列挙し、各ファイルを読み込んでパース・書き直している。長期利用ユーザーのトークンディレクトリに多数のセッションファイルが蓄積した場合、フックごとに複数の YAML ファイルの read/parse/write が走り、体感できるレイテンシが発生する可能性がある。同じ問題が claude-kit / dev-kit / work / ref-inject テンプレートの全 `inject_references.py` に存在する。

| No | ファイル |
|---|---|
| 1 | `plugins/work/hooks/scripts/inject_references.py` |
| 2 | `plugins/claude-kit/hooks/scripts/inject_references.py` |
| 3 | `plugins/dev-kit/hooks/scripts/inject_references.py` |
| 4 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` |

## 原因

クリーンアップ処理が、緊急性が低いにもかかわらずフック発火ごとに無条件で全件スキャンしている。

## 期待される状態

クリーンアップの実行頻度が下がり、頻繁に発火する PreToolUse フックのレイテンシが改善される。期限切れトークンが最大 TTL 間残留しても機能には影響しない。修正が全 `inject_references.py` コピーに反映されている。

## 対応案

クリーンアップの頻度を下げる。

| 案 | 内容 | メリット | デメリット |
|---|---|---|---|
| A | 確率的サンプリング（`random.random() < 0.1` 等、一定確率でのみ実行） | 実装が最小（数行）、状態ファイル不要 | 実行タイミングが非決定的、最悪ケースでスキップが偏りうる |
| B | 最終クリーンアップ時刻を `.last_cleanup` 等に記録し `now - last_cleanup > TTL/4` でのみ実行 | 実行間隔が決定的で予測可能 | 状態ファイルの read/write が増える、実装がやや複雑 |

```python
# 案 A
import random

# 10 回に 1 回だけ cleanup を実行（クリーンアップ自体はそれほど緊急でない）
if random.random() < 0.1:
    _cleanup_expired(token_dir, now, yaml)
```

どちらのアプローチでも、期限切れエントリが最大 TTL 間だけ残留する可能性があるが、トークンファイルの存在は機能的に重要ではなく（セッション終了で自然消滅する）、遅延クリーンアップで問題は生じない。修正は `ref-inject/templates/` を先に行い、各キット版へ同期する。

**推奨: 案A**

## 横展開

WSL2 環境（`/mnt/c/` のような Windows ファイルシステムマウント）では通常の Linux ファイルシステムより I/O が著しく遅い。頻繁に発火する PreToolUse フックではファイルアクセスのコストが直接レイテンシとして現れる。新規フック設計時は「毎回フルスキャン」パターンを避けること。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない

## QA

### QA-1: クリーンアップ頻度低減の方式

A) 確率的サンプリング（最小実装・非決定的） / B) タイムスタンプファイルによる間隔制御（決定的・やや複雑）

**推奨**: A — 実装が最小で副作用が少なく、クリーンアップ自体の緊急性が低いため非決定性は許容できる。

**回答**: A / B
