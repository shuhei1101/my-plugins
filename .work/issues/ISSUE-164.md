# ISSUE-164: inject_references.py の Path.home() でトークンディレクトリを解決 — WSL/Windows cross-env mismatch リスク

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`inject_references.py` がセッション単位のトークンファイルを `~/.claude/tokens/claude-kit/` に置く際、`pathlib.Path.home()` でホームディレクトリを解決している。インシデント #22 (`path-home-cross-env-mismatch`) が指摘するとおり、Claude Code がネイティブ Windows 上で動作し Python が WSL 環境で動作する場合（またはその逆）、`Path.home()` が返すパスは Claude Code が実際に参照するホームとは別のディレクトリになる。結果として TTL トークンが黙って別の場所に書かれ、重複注入抑制が機能しない。

## 現状

`plugins/claude-kit/hooks/scripts/inject_references.py`:

```python
token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
```

## 対応方針

`os.environ.get("HOME")` を優先し、未設定時のみ `Path.home()` にフォールバックする。

```python
home = pathlib.Path(os.environ["HOME"]) if os.environ.get("HOME") else pathlib.Path.home()
token_dir = home / ".claude" / "tokens" / PLUGIN_NAME
```

`dev-kit/hooks/scripts/inject_references.py` にも同様の修正が必要（`*-kit` フック同期構造のため）。

## 対象ファイル

- `plugins/claude-kit/hooks/scripts/inject_references.py`: `Path.home()` を `HOME` 環境変数優先に変更

## QA

### QA-1: どの案で進めるか

A) `os.environ.get("HOME")` を優先しフォールバックに `Path.home()` / B) `CLAUDE_PROJECT_DIR` 直下に置く / C) 現状維持

**推奨**: A — 最小変更

**回答**: <!-- A / B / C -->
