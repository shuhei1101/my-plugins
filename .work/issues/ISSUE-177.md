# ISSUE-177: git-guard.py のトークンがセッション全体で共有され、確認していない別操作が無確認で通過する

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`git-guard.py` のトークンはセッション単位で 1 つ（`workspace-git-guard-{session_id}`）しか存在しない。`git push` でブロックされてトークンが作成された後、Claude が**別の操作**（例: `git merge other-branch`）を実行すると、そのトークンが消費されて無確認で通過してしまう。

ガードの意図は「ユーザーが確認した操作の直後リトライのみ許可」だが、トークンがコマンド種別に紐づいていないため、確認していない別の push/merge 操作でトークンを消費できる。

シナリオ：
1. `git push origin feature` → ブロック（トークン作成）
2. `git merge other-branch` を実行
3. トークンが存在 → 削除 → **無確認で通過**

```python
# plugins/work/hooks/scripts/git-guard.py
token = pathlib.Path(tempfile.gettempdir()) / f"workspace-git-guard-{session_id}"
if token.exists():
    token.unlink()
    return           # ← どの push/merge コマンドでも通過
token.touch()
```

## 対応方針

トークンをコマンド種別（push / merge）またはコマンド文字列のハッシュごとに分け、確認したコマンドと同じものだけを素通りさせる。

## 対象ファイル

- `plugins/work/hooks/scripts/git-guard.py`: トークンファイル名にコマンド種別/ハッシュを含める

## QA

### QA-1: どの案で進めるか

A) コマンド文字列のハッシュをトークン名に含める（完全一致リトライのみ許可） / B) push/merge 種別をトークン名に含める / C) 現状維持・設計許容範囲として文書化

**推奨**: B — 実装がシンプルで、最も多い誤通過ケース（push確認→merge素通り）を防げる

**回答**: <!-- A / B / C -->

