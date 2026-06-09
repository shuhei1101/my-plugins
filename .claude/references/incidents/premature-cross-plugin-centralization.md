<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# プラグイン横断の集約を先回りしすぎた（PR140）

## 何が起きたか

py-kit v2.0.0 を構築する途中、AI は先回りで **別プラグイン `refs-inject-kit` を切り出し、injection rules を集約**する設計を提案・実装した。`${plugin-name}/path/to/ref.md` プレースホルダ記法と、`~/.claude/plugins/cache/*/{plugin}/*/references/` を走査するパス解決ロジック、開発時用の env 変数フォールバックを含む大掛かりな構造。

ユーザーはレビュー後「ややこしすぎる」と却下：「py-kit や他のキットに普通に直接書いた方が良さそうやな / フックとか絶対そっちの方が楽」。`refs-inject-kit` プラグイン全体（5 コミット、~700 行）を撤回し、py-kit に hook / templates / `injection_rules.yaml` を直接持たせる構成に戻した。

## 根本原因

抽象化の動機は「将来 N 個のプラグインがこれを必要とするはず」だったが:

- 切り出し時点で consumer は py-kit のみ。next-kit は仮想的存在
- プレースホルダ記法 + クロスプラグインパス解決は非自明な複雑性を追加（`~/.claude/plugins/cache/` の glob、バージョン選択、env 変数フォールバック）
- 各プラグインが自前で hook を持つコストは ~50 行の重複で、集約機構のコストよりずっと安い

## 教訓

**「将来必要かも」だけでプラグイン横断の集約を作らない。** 閾値:

- **2 プラグイン** で同じ hook: 抽出を検討してもよいが、コピペでも十分
- **3 プラグイン以上** で本当に同一の hook: 抽出が割に合い始める
- **クロスプラグインプレースホルダ / パス解決 / バージョン選択**: 本当に避けられない時のみ

PR140 の正解は: `inject_references.py` + `templates/` + `injection_rules.yaml` を py-kit に置く。next-kit が同じニーズを持ったらコピー。3 番目の consumer か 3 回目のドリフト事故、どちらか先に来た時点で初めて抽出を検討する。

## 関連

- [[premature-abstraction]] / YAGNI 原則
- 撤回されたプラグイン: `plugins/refs-inject-kit/`（PR140 コミット 98f9617 → a09627b → 237c41a で revert）
