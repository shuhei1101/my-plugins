# ISSUE-181: dev-kit inject_references.py が jp_mirror 変数をテンプレートに渡していない（claude-kit との drift）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/hooks/scripts/inject_references.py` の `tmpl.render()` 呼び出しに `jp_mirror` 変数を渡していない。claude-kit 側は `jp_mirror=jp_mirror` を渡しており、テンプレート内で `{% if not jp_mirror %}` ブロックを使って JP ミラースキップ時の注意書きを表示している。

dev-kit の現テンプレートは `jp_mirror` 変数を参照していないため現状は実害ゼロだが、キットフック同期ルール（`references/hook/キットフック同期.md`）が規定する「テンプレート変数は両キット間で一致させる」制約に違反している。将来 dev-kit テンプレートに `jp_mirror` ブロックを追加した際に `jp_mirror` が未定義のままだと `StrictUndefined` で実行時エラーになる。

加えて dev-kit の `inject_references.py` には `jp_mirror` を計算するコード自体が存在しない。

## 対応方針

1. `inject_references.py` に `jp_mirror` の計算ロジックを追加（claude-kit と同一実装）
2. `tmpl.render()` に `jp_mirror=jp_mirror` を追加
3. `DEV_KIT_JP_MIRROR` 環境変数を `plugins/dev-kit/CLAUDE.md` の env トグル表に追加

## 対象ファイル

- `plugins/dev-kit/hooks/scripts/inject_references.py`: `jp_mirror` 計算ロジックの追加 + `tmpl.render()` へ引数追加
- `plugins/dev-kit/CLAUDE.md`: `DEV_KIT_JP_MIRROR` を env 変数表に追加

