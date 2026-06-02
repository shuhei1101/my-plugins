# ISSUE-198: ref-inject 配布テンプレートの inject_references.py の _save_token エラーメッセージが英語（消費者と不一致）

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/ref-inject/templates/hooks/scripts/inject_references.py` の `_save_token` 関数内のエラーメッセージ 1 件が英語のままで、同ファイル内の他のすべてのエラーメッセージ（およびすべての消費者コピー）と一致しない。

```python
_eprint(f"token write error ({path.name}): {e}")
```

同ファイル内の他の `_eprint` 呼び出しは日本語（`"トークンパースエラー"`、`"stdin パースエラー"` など）。消費者コピー（claude-kit・dev-kit・work）はすべて `"トークン書き込みエラー"` に変更済み。`/ref-inject:plugin-migrate` はテンプレート → 消費者方向のみ伝播するため、消費者側の変更がテンプレートに逆流していない。

## 対応方針

テンプレートの当該行を日本語に統一する。

```python
_eprint(f"トークン書き込みエラー ({path.name}): {e}")
```

## 対象ファイル

- `plugins/ref-inject/templates/hooks/scripts/inject_references.py`: `_save_token` のエラーメッセージを日本語化

