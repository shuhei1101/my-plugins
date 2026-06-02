---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-095: `inject_references.py` が全フック発火ごとに `~/.claude/tokens/` を全件スキャンする

**作成日**: 2026-05-31

## 問題

`inject_references.py`（work / claude-kit / dev-kit / ref-inject テンプレート）の `_cleanup_expired()` は、**フックが発火するたびに毎回**呼ばれる:

```python
now = time.time()
_cleanup_expired(token_dir, now, yaml)  # ← 無条件に全セッションのトークンを走査
```

`_cleanup_expired()` の内部では `token_dir.glob("*.yaml")` で全セッションファイルを列挙し、各ファイルを読み込んでパース・書き直している。このフックは `PreToolUse(Edit | Write | MultiEdit | Read)` で発火するため、作業中に Claude が編集・読み込みを行うたびに毎回このスキャンが動く。

長期利用ユーザーのトークンディレクトリに多数のセッションファイルが蓄積した場合、フックごとに複数の YAML ファイルの read/parse/write が走り、体感できるレイテンシが発生する可能性がある。特に低速ストレージ（WSL2 上の Windows ファイルシステム `/mnt/c/...`）では顕著になる。同じ問題が claude-kit / dev-kit / work / ref-inject テンプレートの全 `inject_references.py` に存在する。

| No | ファイル |
|---|---|
| 1 | `plugins/work/hooks/scripts/inject_references.py` |
| 2 | `plugins/claude-kit/hooks/scripts/inject_references.py` |
| 3 | `plugins/dev-kit/hooks/scripts/inject_references.py` |
| 4 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` |

## 修正案

クリーンアップの頻度を下げる。例えば、確率的サンプリング（一定確率でのみ実行）や、最終クリーンアップ時刻をトークンファイル内またはセパレートなタイムスタンプファイルに記録して一定間隔（例: TTL / 10）でのみ実行する方式が考えられる:

```python
import random

# 10 回に 1 回だけ cleanup を実行（クリーンアップ自体はそれほど緊急でない）
if random.random() < 0.1:
    _cleanup_expired(token_dir, now, yaml)
```

または、最後のクリーンアップ時刻を `~/.claude/tokens/{plugin}/.last_cleanup` に記録し、`now - last_cleanup > TTL / 4` の場合のみ実行する。

どちらのアプローチでも、期限切れエントリが最大 TTL 間だけ残留する可能性があるが、トークンファイルの存在は機能的に重要ではなく（セッション終了で自然消滅する）、遅延クリーンアップで問題は生じない。

修正は `ref-inject/templates/` を先に行い、各キット版へ同期する。

## 水平展開

WSL2 環境（`/mnt/c/` のような Windows ファイルシステムマウント）では通常の Linux ファイルシステムより I/O が著しく遅い。頻繁に発火する PreToolUse フックではファイルアクセスのコストが直接レイテンシとして現れる。新規フック設計時は「毎回フルスキャン」パターンを避けること。
