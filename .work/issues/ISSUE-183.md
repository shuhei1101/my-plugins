# ISSUE-183: dev-kit inject_references.py の Path.home() でトークンパスがクロス環境ミスマッチ（ISSUE-164 横展開）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/hooks/scripts/inject_references.py` が `pathlib.Path.home()` でトークンディレクトリを解決している。これはインシデント #22（`path-home-cross-env-mismatch`）および ISSUE-164（claude-kit 側の同一問題）の横展開。

```python
token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
```

WSL 環境で Claude Code がネイティブ Windows として動作し、フックスクリプトが WSL Python で実行される場合（またはその逆）、`Path.home()` が返すパスが異なる。結果として TTL トークンが正しいパスに書かれず、重複注入抑制が機能しない（毎回フルインジェクションが発生する）。

## 対応方針

`os.environ.get("HOME")` を優先し、未設定時のみ `Path.home()` にフォールバックする。ISSUE-164（claude-kit）と同一の修正を適用し、両キット同期を保つ。

## 対象ファイル

- `plugins/dev-kit/hooks/scripts/inject_references.py`: トークンディレクトリ解決を `HOME` 環境変数優先に変更

