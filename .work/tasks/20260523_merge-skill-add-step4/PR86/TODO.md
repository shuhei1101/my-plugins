# PR86 — merge-skill-add-step4

## 概要

work-kit:merge スキルの Step 5（archive）が常に 0 件を返すバグを修正する。
原因: archive 実行前に `index.yaml` の `completed: true` フラグが立っていないため。
修正: `index-tool.py` に `set-completed` サブコマンドを追加し、merge SKILL.md に Step 4 として追加する。
併せて archive の書き込み先を worktree の `index.archive.yaml` に変更し、PR ブランチにコミットしてから --no-ff マージする設計を実現する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/.../PR86/QA.md` |
| - | `.work/specs/` に merge フロー仕様書を作成する | `.work/specs/work-kit-merge-flow.md` |
| - | `index-tool.py` に `set-completed --id N` サブコマンドを追加 | `plugins/work-kit/scripts/index-tool.py` |
| - | `merge/SKILL.md` に Step 4 を追加（set-completed 実行） | `plugins/work-kit/skills/merge/SKILL.md` |
| - | `merge/SKILL.md` の Step 5 を修正（archive 先を worktree に変更） | `plugins/work-kit/skills/merge/SKILL.md` |
| - | `merge/SKILL.jp.md` に同じ変更を反映 | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| - | `plugin.json` と `marketplace.json` のバージョンをバンプ | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/specs/work-kit-merge-flow.md`: merge フローの設計仕様

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
