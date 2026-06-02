# ISSUE-188: ref-inject/CLAUDE.jp.md の構造ツリーに「└── templates/」行が欠落

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/CLAUDE.jp.md` の `## 構成` コードブロックで、英語版（`CLAUDE.md`）にある `└── templates/   # the injection files...` の行が丸ごと欠落している。その結果、`├── hooks/` 以下のツリーが `skills/plugin-migrate/SKILL.md` の子ノードであるかのように誤ったインデントで表示されている。

```
# 正しい姿（EN）
├── skills/plugin-migrate/SKILL.md (+ .jp.md)  # ...
└── templates/                           # 注入ファイル群
    ├── hooks/
    ...
```

## 対応方針

`└── templates/` 行を正しい位置（`skills/plugin-migrate/...` 行の直後、`hooks/` の親として）に追加し、JP 訳のコメントを付ける。

## 対象ファイル

- `plugins/ref-inject/CLAUDE.jp.md`: 構造ツリーに `└── templates/` 行を挿入

