# ISSUE-190: claude-kit/CLAUDE.md の説明文に「for explicit invocation」が二重記載

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/CLAUDE.md` の `## Authoring knowledge lives in references/` セクションに、以下の重複フレーズがある。

```
The wrappers remain for explicit invocation and for callers
for explicit invocation.
```

「for explicit invocation」が 2 回登場しており、2 行目は不完全なセンテンスになっている。JP ミラー（`CLAUDE.jp.md`）では「ラッパーは明示起動と呼び出し元のために残している」とまとめて 1 文で書かれており、重複はない。

## 対応方針

英語原文を意味の通る 1 文に修正する。例: `The wrappers remain for explicit invocation and for callers that depend on them.`

## 対象ファイル

- `plugins/claude-kit/CLAUDE.md`: 重複フレーズを修正

