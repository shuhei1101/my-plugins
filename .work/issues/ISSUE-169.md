# ISSUE-169: html-mock の References に誤ったテンプレートパス（skills/mock/templates/）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/skills/html-mock/SKILL.md` の `References` セクション末尾が `{plugin_root}/skills/mock/templates/mock-skeleton.html` を参照しているが、実際のファイルは `{plugin_root}/skills/html-mock/templates/mock-skeleton.html` に存在する。

`SKILL.jp.md` も同様。

## 対応方針

`skills/mock/templates/` を `skills/html-mock/templates/` に修正する。

## 対象ファイル

- `plugins/dev-kit/skills/html-mock/SKILL.md`: References セクションのパスを修正
- `plugins/dev-kit/skills/html-mock/SKILL.jp.md`: 同上
