# ISSUE-197: ref-inject 配布テンプレートの inject_references.py が Path.home() を使用（ISSUE-164/183 の修正源に漏れ）

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/templates/hooks/scripts/inject_references.py`（配布テンプレート）が `pathlib.Path.home()` でトークンディレクトリを解決している。ISSUE-164（claude-kit 消費者）と ISSUE-183（dev-kit 消費者）は各消費者コピーの修正を対象としているが、**配布元テンプレート自体が修正対象に含まれていない**。テンプレートを修正しなければ、将来 `/ref-inject:apply` を実行した新規プラグインや再 apply 時に同じ問題が再生産される。

```python
token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
```

インシデント #22（`path-home-cross-env-mismatch`）の通り、WSL/Windows のクロス環境で `Path.home()` が誤ったパスを返し、TTL トークンが誤った場所に書かれて重複注入抑制が機能しない。

## 対応方針

テンプレートの当該行を `os.environ.get("HOME")` 優先に修正する（ISSUE-164 で合意した修正と同一）。ISSUE-164/183 の修正と同タスクで配布元テンプレートも修正すると漏れが生じない。`plugins/work/hooks/scripts/inject_references.py` も同一問題を持つため `/ref-inject:plugin-migrate` で一括伝播できる。

## 対象ファイル

- `plugins/ref-inject/templates/hooks/scripts/inject_references.py`: トークンディレクトリ解決を `HOME` 環境変数優先に変更

## QA

### QA-1: 修正のタイミング

A) ISSUE-164/183 の修正と同タスクでテンプレートも修正 / B) 独立イシューとして別タスクで修正

**推奨**: A — 同時修正で漏れを防ぐ

**回答**: <!-- A / B -->
