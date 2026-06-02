# ISSUE-166: injection.md.j2 / injection.jp.md.j2 に Pitfall 3 — {% if not jp_mirror %} 直後に空行なしのブロッククォート

**作成日**: 2026-06-02

## 問題

`plugins/claude-kit/hooks/templates/injection.md.j2` と `injection.jp.md.j2` の `{% if not jp_mirror %}` ブロックが、Jinja2 テンプレート執筆ガイド（`references/hook/jinja2/テンプレート注意点.md` Pitfall 3）で定義した「ブロックタグ直後に空行なしのブロックレベル要素」アンチパターンに該当している。

`trim_blocks=True` により `{% if %}` タグ後の改行が削除され、ブロッククォートが先行コンテンツに付着する可能性がある。

```jinja2
{% if not jp_mirror %}
> `CLAUDE_KIT_JP_MIRROR=false` — ...   ← 空行なし（Pitfall 3）
```

## 対応方針

`{% if not jp_mirror %}` の直後に空行を1行追加する：

```jinja2
{% if not jp_mirror %}

> `CLAUDE_KIT_JP_MIRROR=false` — ...
```

`dev-kit/hooks/templates/` にも同構造のテンプレートが存在する場合は同様に修正する。

## 対象ファイル

- `plugins/claude-kit/hooks/templates/injection.md.j2`: `{% if not jp_mirror %}` の直後に空行を追加
- `plugins/claude-kit/hooks/templates/injection.jp.md.j2`: 同上

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
