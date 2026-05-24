# PR90 — add-notes-to-claude-skill

## 概要

`notes/` フォルダの立ち位置説明を CLAUDE.md に追記し、
notes → ルール / CLAUDE.md 昇格スキル `work-kit:notes-to-claude` を新規作成する。

背景: PR88 で `.work/specs/` を `notes/` にリネームしたが、
「notes とは何か・何のために使うのか」が CLAUDE.md に記載されておらず Claude Code に伝わらない。
また notes の内容を恒久的な知識として昇格させる手順をスキル化したい。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `templates/.work/CLAUDE.jp.md` の `notes/` セクションに立ち位置説明を追記 | - `plugins/work-kit/templates/.work/CLAUDE.jp.md` |
| - | `templates/.work/CLAUDE.md` に同内容を英語で追記 | - `plugins/work-kit/templates/.work/CLAUDE.md` |
| - | `work-kit:notes-to-claude` スキルを作成（SKILL.md） | - `plugins/work-kit/skills/notes-to-claude/SKILL.md` |
| - | SKILL.jp.md を作成 | - `plugins/work-kit/skills/notes-to-claude/SKILL.jp.md` |
| - | plugin.json / marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- aituber PR426 TODO.md: notes → rule/references への昇格フロー参考

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
