# PR88 — rename-specs-to-notes

## 概要

`.work/specs/` フォルダ名を `notes/` にリネームする。
`specs` は「プロジェクト仕様書」のニュアンスが強く AIに自動読み込みされないため古くなりやすい。
実態は一時的な検討メモ・設計ノートなので `notes` の方が実態に合っている。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | テンプレートフォルダを `specs/` → `notes/` にリネーム | - `plugins/work-kit/templates/.work/specs/` |
| 済 | テンプレートファイル `spec.md` を `note.md` にリネーム | - `plugins/work-kit/templates/spec.md` |
| 済 | `.work/CLAUDE.md` の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/templates/.work/CLAUDE.md` |
| 済 | `.work/CLAUDE.jp.md` の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/templates/.work/CLAUDE.jp.md` |
| 済 | work-start SKILL.md の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | work-start SKILL.jp.md の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | setup SKILL.md の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/skills/setup/SKILL.md` |
| 済 | setup SKILL.jp.md の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/skills/setup/SKILL.jp.md` |
| 済 | stop フック prompts の `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/hooks/prompts/stop.md` / `stop.jp.md` |
| 済 | TODO テンプレートの `specs/` 参照を `notes/` に更新 | - `plugins/work-kit/templates/TODO.md` |
| 済 | plugin.json / marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |

## 参考ドキュメント

なし（単純なリネーム作業）

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |

## QA

なし
