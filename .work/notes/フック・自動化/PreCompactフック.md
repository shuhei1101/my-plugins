# PreCompact フック — conversation-to-claude 自動実行

## 概要

`/compact` 実行直前に `/work:conversation-to-claude` スキルを自動実行し、セッションの作業内容を
失う前にアーティファクトとして保存する。work プラグインの一部（スキル本体は
`スキル設計/会話キャプチャスキル.md` 参照）。

## 設計

### イベント

`PreCompact` — `/compact` 実行前に発火。`compaction_trigger: "manual" | "auto"` で起動種別を区別できる。

### ループ防止

`PreCompact` には `stop_hook_active` 相当のフラグがないため、セッション単位のフラグファイルで防止する
（`_common.py` の `already_dispatched_this_session`）。

- 初回: フラグ不在 → フラグ作成 → `decision: block` で Claude が conversation-to-claude を実行
- 2回目以降（スキル完了後の再 `/compact`）: フラグ存在 → `sys.exit(0)` で compact が通過

フラグ名: `{tempdir}/work-pre-compact-{session_id}`。フラグは消費しない（unlink しない）ため、
1セッションで最初の `/compact` のみスキルを起動する。

### トグル

`WORK_PRECOMPACT_CONV2CLAUDE`（デフォルト有効）。falsy でフック全体を無効化。

### プロンプトファイル

`plugins/work/hooks/prompts/pre-compact.md`（+ `.jp.md`）。内容: `/work:conversation-to-claude` を
実行してからもう一度 `/compact` を実行してください、という指示。

## ファイル構成

```
plugins/work/
  hooks/
    hooks.json                     ← PreCompact エントリ追加
    scripts/
      pre-compact.py               ← フックスクリプト（_common.py のヘルパー利用）
    prompts/
      pre-compact.md               ← 指示プロンプト
      pre-compact.jp.md            ← JP ミラー
```

## 変更履歴

| # | 日付 | 変更 |
|---|---|---|
| 1 | 2026-06-02 | claude-kit から work プラグインに移設して復活。インライン python を `pre-compact.py` に切り出し、`_common.py` のセッションフラグヘルパーを利用。トグル `WORK_PRECOMPACT_CONV2CLAUDE` (work v2.62.0) |
