# ISSUE-196: ref-inject 配布テンプレートの injection.md.j2 / injection.jp.md.j2 に Pitfall 1 修正漏れ

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/templates/hooks/templates/injection.md.j2`（および `.jp.md.j2`）に Jinja2 Markdown Pitfall 1 の修正が適用されていない。`{% for ref in required %}` 直後に空行なしで `---` が来ている。

```jinja2
{% for ref in required %}
---           ← 空行なし（Pitfall 1）
```

`trim_blocks=True` により `%}` 直後の改行が除去されるため、2 回目以降のループイテレーションで前の `ref.body` 末尾と `---` が隣接し、setext-style 見出しとして誤解釈される。claude-kit の対応テンプレートは `{% for %}` ブロック内先頭に空行を置いて修正済み。

ここは消費者プラグインへ配布される**配布元テンプレート**であり、修正しなければ将来の `apply`/`plugin-migrate` で問題が再生産される。

## 対応方針

`{% for ref in required %}` の直後に空行を 1 行挿入する。EN・JP 両テンプレートとも修正。`/ref-inject:plugin-migrate` で消費者（dev-kit / work）に伝播する。dev-kit 側は ISSUE-180 でカバー済み。

## 対象ファイル

- `plugins/ref-inject/templates/hooks/templates/injection.md.j2`: `{% for %}` 内先頭に空行を挿入
- `plugins/ref-inject/templates/hooks/templates/injection.jp.md.j2`: 同上

## QA

### QA-1: ISSUE-143 への追記 vs 独立修正

A) ISSUE-143（claude-kit 配布元の Pitfall 2/3）の対応方針に Pitfall 1 を追記して一括対応 / B) 本イシューとして独立修正

**推奨**: A — 同一ファイル群への修正をまとめる方が効率的

**回答**: <!-- A / B -->

