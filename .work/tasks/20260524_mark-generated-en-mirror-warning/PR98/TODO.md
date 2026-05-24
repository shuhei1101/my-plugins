# PR98 — mark-generated に英語版ミラー警告を追加

## 概要

PR97 で `mark-generated` に `*.html` / `*.js` / `*.css` の記法を追加した。
ただし JP ミラー警告コメントは依然として `*.jp.md` のみに付与される非対称状態が残っている。

英語版ファイル（`SKILL.md` / `CLAUDE.md` / `.claude/rules/**/*.md` など AI が読むプロンプト系）にも
「このファイルは JP ミラーと同時管理されている」相互参照コメントを返すよう `mark-generated` を拡張する。

### 現状の問題

- `*.jp.md` には JP ミラー警告が冒頭に挿入される（PR94 で導入）
- 英語版オリジナルには相互参照コメントがなく、AI が SKILL.md を読んだだけでは JP ミラーの存在が分からない
- `skill-jp-mirror-sync.md` というリンクルールでだけ「JP ミラー必ず同期」が周知されている
- 「ファイル冒頭の警告」と「ルールによる強制」の役割重複があり整理が必要

### この PR で決めること

- 英語版ミラー警告の文言（例: `<!-- A Japanese mirror exists at SKILL.jp.md. When updating this file, update the mirror too. -->`）
- 適用対象ファイル種別（SKILL.md / CLAUDE.md / `.claude/rules/**/*.md`）
- 遡及適用の対象範囲（既存 JP/EN ペア全件）
- `skill-jp-mirror-sync.md` ルールとの関係整理（コメントへの一本化 / ルールは残すが軽量化 / 等）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/.../PR98/QA.md` |
| - | `.work/notes/generator-metadata.md` に EN ミラー警告の仕様を追記する | - `.work/notes/generator-metadata.md` |
| - | `mark-generated` SKILL.md / SKILL.jp.md に EN ミラー警告のロジック（Step 4 拡張）を追加 | - `plugins/claude-kit/skills/mark-generated/SKILL.md` `SKILL.jp.md` |
| - | 既存 JP/EN ペア（SKILL.md / CLAUDE.md / ルール）に EN 警告を遡及適用 | - `plugins/**/SKILL.md` `plugins/**/CLAUDE.md` `.claude/rules/**/*.md` |
| - | `skill-jp-mirror-sync.md` ルールと EN 警告コメントの役割整理（重複削減または役割明示） | - `.claude/rules/feature/skill-jp-mirror-sync.md` |
| - | claude-kit のバージョン bump (3.19.0 → 3.20.0) + changelogs エントリ | - `plugins/claude-kit/.claude-plugin/plugin.json` `changelogs/` |
| - | marketplace.json のバージョン同期 | - `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/generator-metadata.md`: PR94 で作られた mark-generated の仕様メモ
- `.claude/rules/feature/skill-jp-mirror-sync.md`: 既存の JP ミラー同期ルール（役割整理対象）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
