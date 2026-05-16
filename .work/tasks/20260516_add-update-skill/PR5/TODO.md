# PR5 — add-update-skill

## 概要

work-kit のテンプレートを `plugins/work-kit/skills/setup/templates/` から `plugins/work-kit/templates/` に移動し、
setup スキルの参照パスを更新した上で、既存プロジェクトの `.work/` を最新テンプレートに同期する新規 `update` スキルを追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | テンプレートを共有パスに移動する | `plugins/work-kit/templates/` (新規)<br>`plugins/work-kit/skills/setup/templates/` (削除) |
| 済 | setup.py のテンプレートパスを更新する | `plugins/work-kit/skills/setup/scripts/setup.py` |
| 済 | update スキルを作成する（SKILL.md + SKILL.jp.md） | `plugins/work-kit/skills/update/SKILL.md`<br>`plugins/work-kit/skills/update/SKILL.jp.md` |
| 済 | plugin.json / marketplace.json バージョンバンプ | `plugins/work-kit/.claude-plugin/plugin.json`<br>`.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/setup/SKILL.md`: 既存 setup スキル定義
- `plugins/work-kit/skills/setup/scripts/setup.py`: テンプレート展開スクリプト
